import calendar
import logging
from datetime import date
from functools import reduce
from sys import exc_info
from traceback import format_exception

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class AccountAsset(models.Model):
    _name = "account.asset"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Equipment"
    _check_company_auto = True
    _order = "date_start desc, code, name"

    account_move_line_ids = fields.One2many(comodel_name="account.move.line",
                                            inverse_name="asset_id",
                                            string="Entries", readonly=True,
                                            copy=False, )
    move_line_check = fields.Boolean(string="Has accounting entries")
    name = fields.Char(string="Asset Name", required=True, readonly=True,
                       states={"draft": [("readonly", False)]}, )
    code = fields.Char(string="Reference", size=32,
                       default=lambda self: _('New'), readonly=True)
    purchase_value = fields.Monetary(string="Purchase Value", readonly=True,
                                     states={"draft": [("readonly", False)]},
                                     help="This amount represent the initial value of the asset."
                                          "\nThe Depreciation Base is calculated as follows:"
                                          "\nPurchase Value - Salvage Value.",
                                     currency_field='company_currency_id')
    salvage_value = fields.Monetary(string="Salvage Value", digits="Account",
                                    readonly=True,
                                    states={"draft": [("readonly", False)]},
                                    help="The estimated value that an asset will realize upon "
                                         "its sale at the end of its useful life.\n"
                                         "This value is used to determine the depreciation amounts.")
    depreciation_base = fields.Monetary(digits="Account",
                                        string="Depreciation Base", store=True,
                                        help="This amount represent the depreciation base "
                                             "of the asset (Purchase Value - Salvage Value.", )
    value_residual = fields.Monetary(digits="Account",
                                     string="Residual Value",
                                     store=True)
    value_depreciated = fields.Monetary(digits="Account",
                                        string="Depreciated Value",
                                        store=True, )
    note = fields.Text("Note")
    profile_id = fields.Many2one(comodel_name="account.asset.profile",
                                 string="Asset Profile",
                                 change_default=True,
                                 states={"draft": [("readonly", False)]})
    group_ids = fields.Many2many(comodel_name="account.asset.group",
                                 relation="account_asset_group_rel",
                                 column1="asset_id", column2="group_id",
                                 string="Asset Groups", )
    date_start = fields.Date(string="Asset Start Date", readonly=True,
                             required=True, default=fields.Date.today,
                             states={"draft": [("readonly", False)]},
                             help="You should manually add depreciation lines "
                                  "with the depreciations of previous fiscal years "
                                  "if the Depreciation Start Date is different from the date "
                                  "for which accounting entries need to be generated.", )
    date_remove = fields.Date(string="Asset Removal Date", readonly=True)
    state = fields.Selection(
        selection=[("draft", "Active"), ("open", "In Service"),
                   ("removed", "Inactive"), ], string="Status",
        required=True, default="draft", copy=False,
        help="When an Equipment is created, the status is 'Active'.\n"
             "If the Equipment is Transfer to customer location the status will be 'In Service'.\n"
             "If the Equipment is Retire the status will be 'In Active' \n", )
    active = fields.Boolean(default=True)
    partner_id = fields.Char(string="Partner", readonly=True,
                             states={"draft": [("readonly", False)]})
    method = fields.Selection(selection=lambda self: self.env[
        "account.asset.profile"]._selection_method(),
                              string="Computation Method", required=True,
                              readonly=True,
                              states={"draft": [("readonly", False)]},
                              default="linear",
                              help="Choose the method to use to compute "
                                   "the amount of depreciation lines.\n"
                                   "  * Linear: Calculated on basis of: "
                                   "Gross Value / Number of Depreciations\n"
                                   "  * Degressive: Calculated on basis of: "
                                   "Residual Value * Degressive Factor"
                                   "  * Degressive-Linear (only for Time Method = Year): "
                                   "Degressive becomes linear when the annual linear "
                                   "depreciation exceeds the annual degressive depreciation")
    method_number = fields.Integer(string="Number of Years", readonly=True,
                                   default=5,
                                   states={"draft": [("readonly", False)]},
                                   help="The number of years needed to depreciate your asset", )
    method_period = fields.Selection(
        selection=lambda self: self.env[
            "account.asset.profile"]._selection_method_period(),
        string="Period Length", required=True, readonly=True, default="year",
        states={"draft": [("readonly", False)]},
        help="Period length for the depreciation accounting entries")
    method_end = fields.Date(string="Ending Date", readonly=True,
                             states={"draft": [("readonly", False)]})
    method_progress_factor = fields.Float(string="Degressive Factor",
                                          readonly=True,
                                          states={
                                              "draft": [("readonly", False)]},
                                          default=0.3, )
    method_time = fields.Selection(selection=lambda self: self.env[
        "account.asset.profile"]._selection_method_time(),
                                   string="Time Method", required=True,
                                   readonly=True, default="year",
                                   states={"draft": [("readonly", False)]},
                                   help="Choose the method to use to compute the dates and "
                                        "number of depreciation lines.\n"
                                        "  * Number of Years: Specify the number of years "
                                        "for the depreciation.\n"
                                   # "  * Number of Depreciations: Fix the number of "
                                   # "depreciation lines and the time between 2 depreciations.\n"
                                   # "  * Ending Date: Choose the time between 2 depreciations "
                                   # "and the date the depreciations won't go beyond."
                                   )
    days_calc = fields.Boolean(string="Calculate by days", default=False,
                               help="Use number of days to calculate depreciation amount", )
    use_leap_years = fields.Boolean(string="Use leap years", default=False,
                                    help="If not set, the system will distribute evenly the amount to "
                                         "amortize across the years, based on the number of years. "
                                         "So the amount per year will be the "
                                         "depreciation base / number of years.\n "
                                         "If set, the system will consider if the current year "
                                         "is a leap year. The amount to depreciate per year will be "
                                         "calculated as depreciation base / (depreciation end date - "
                                         "start date + 1) * days in the current year.")
    prorata = fields.Boolean(string="Prorata Temporis", readonly=True,
                             states={"draft": [("readonly", False)]},
                             help="Indicates that the first depreciation entry for this asset "
                                  "have to be done from the depreciation start date instead "
                                  "of the first day of the fiscal year.", )
    depreciation_line_ids = fields.One2many(comodel_name="account.asset.line",
                                            inverse_name="asset_id",
                                            string="Depreciation Lines",
                                            copy=False, readonly=True,
                                            states={"draft": [
                                                ("readonly", False)]})
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 required=True, readonly=True,
                                 default=lambda
                                     self: self._default_company_id())
    company_currency_id = fields.Many2one(comodel_name="res.currency",
                                          related="company_id.currency_id",
                                          string="Company Currency",
                                          store=True, readonly=True, )
    account_analytic_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic account")
    asset_no = fields.Char('Asset No')
    manufacture = fields.Char('Manufacture')
    model_no = fields.Char('Model No')
    warranty = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    route_id = fields.Many2one('route.route', string="Route",
                               related='machine_location_id.warehouse_id.route')
    commission = fields.Float('Relative Commission Rate')
    meter_reading = fields.Char('Initial Meeter Reading')
    vandalism = fields.Float('Vandalism Escrow %')
    management_fee = fields.Float('Management Fee %')
    marketing_fee = fields.Float('Marketing Fee %')
    fuel_surcharge = fields.Float('Fuel Surcharge %')
    model = fields.Char('Model')
    model_redable = fields.Boolean('Model Readable', default=False)

    serial_no = fields.Char('Serial No', copy=False, required=True)
    serial_readable = fields.Boolean('Serial Readable', default=False)
    effective_date = fields.Date('Effective Date',
                                 default=fields.Date.context_today,
                                 required=True,
                                 help="Date at which the Equipment became effective. This date will be used to compute "
                                      "the Mean Time Between Failure.")
    warranty_date = fields.Date('Warranty Expiration Date')
    color = fields.Integer(string='Color Index', default=1)
    scrap_date = fields.Date('Scrap Date')
    machine_type_id = fields.Many2one('account.asset.type',
                                      string="Equipment Type",
                                      ondelete='restrict')
    vending_type = fields.Selection(
        [('machine_style', 'Def. Equipment Style')],
        string="Vending/Non Vending TYpe")
    management_style = fields.Selection(
        [('machine_style', 'Def. Equipment Style'),
         ('non_commerce', 'Non Commerce')],
        string="Equipment Style", default='machine_style')
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    location_type = fields.Selection(
        [('micro_market', 'Micromarket'), ('order', 'Order')],
        string='Location Type',
        default="micro_market", readonly=True,
        states={'draft': [('readonly', False)]})
    micro_market_id = fields.Many2one('stock.warehouse', domain=[
        ('location_type', '=', 'micro_market')], readonly=True,
                                      states={'draft': [('readonly', False)]})
    warehouse_id = fields.Many2one('stock.warehouse',
                                   domain=[('location_type', '=', 'view')],
                                   readonly=True,
                                   states={'draft': [('readonly', False)]})
    location_partner_id = fields.Many2one('res.partner', string="Customer",
                                          domain="[('is_customer', '=', True),('parent_id', '=', False),('type', '=', 'contact')]")
    activity_type = fields.Selection(
        [('install', 'Install'), ('remove', 'Remove'),
         ('exchange', 'Exchange'), ('retire', 'Retire')],
        string="Activity Type", default='install')

    machine_location_id = fields.Many2one('stock.location',
                                          string="Equipment Location",
                                          ondelete='restrict')
    machine_location_ids = fields.Many2many('stock.location',
                                            'machine_locations_stock_location_rel')
    attachment_number = fields.Integer('Number of Attachments')
    finance_type = fields.Selection(
        [('own', 'Own'), ('loan', 'Loan'), ('lease', 'Lease')], default='own')
    loan_year = fields.Integer(string="Number of Years", readonly=True,
                               default=1,
                               states={"draft": [("readonly", False)]})
    loan_period = fields.Selection(
        selection=lambda self: self.env[
            "account.asset.profile"]._selection_method_period(),
        string="Period Length", readonly=True, default="year",
        states={"draft": [("readonly", False)]},
        help="Period length for the loan accounting entries")
    loan_line_ids = fields.One2many(comodel_name="account.loan.line",
                                    inverse_name="asset_id",
                                    string="Loan Lines", copy=False,
                                    readonly=True,
                                    states={"draft": [("readonly", False)]})
    loan_base = fields.Float(digits="Account", string="Loan Base",
                             readonly=True,
                             states={"draft": [("readonly", False)]},
                             help="This amount represent the loan base "
                                  "of the Equipment")
    account_loan_id = fields.Many2one(comodel_name="account.account",
                                      string="Loan Account",
                                      domain="[('internal_type', '=', 'payable'),('deprecated', '=', False)]")
    journal_id = fields.Many2one(comodel_name="account.journal",
                                 domain=[('type', '=', 'general')],
                                 string="Journal")
    loan_paid = fields.Float(digits="Account",
                             string="Loan Paid", store=True)
    loan_to_pay = fields.Float(digits="Account",
                               string="Loan To Pay", store=True)
    loan_prorata = fields.Boolean(string="Prorata Temporis", readonly=True,
                                  states={"draft": [("readonly", False)]},
                                  default=True,
                                  help="Indicates that the first depreciation entry for this asset "
                                       "have to be done from the depreciation start date instead "
                                       "of the first day of the fiscal year.")
    installed_date = fields.Date(string="Installed Date", readonly=1)
    last_transfer_date = fields.Date(string="Last Transfer Date", readonly=1)
    removed_date = fields.Date(string="Removal Date", readonly=1)
    move_id = fields.Many2one('account.move')
    parts_line_ids = fields.One2many('parts.line', 'machine_id',
                                     string="Parts", ondelete='cascade')
    serviced_by = fields.Selection(
        [('branch', 'Branch'), ('operator', 'Operator')],
        string='Serviced By', )

    service_date = fields.Date(string="Service Date")
    out_service_date = fields.Date(string="Out Service Date")
    disposition_date = fields.Date(string="Disposition Date")
    disposition_reason = fields.Char(string="Disposition Reason")

    machine_age = fields.Char(string="Equipment Age")
    opt_health = fields.Integer(string="OPT Healthy %", default=0)
    is_inventory = fields.Boolean(string="Inventory", default=False)
    is_telemetry = fields.Boolean(string="Telemetry", default=False)
    is_credit_Card_reader = fields.Boolean(string="Credit Card Reader",
                                           default=False)
    is_energy_star = fields.Boolean(string="Energy Star", default=False)
    is_healt_wellness = fields.Boolean(string="Health & Wellness",
                                       default=False)
    machine_frontage = fields.Selection(
        [('stack', 'Stack'), ('glass_front', 'Glass Front')],
        string="Equipment Frontage")

    area_or_pos = fields.Char(string="Area/POS")
    access_type = fields.Char(string="Access Type")

    first_reported_period = fields.Char(string="First Reported Period")
    last_reported_period = fields.Char(string="Last Reported Period")

    contract_expiration = fields.Date(string="Contract Expiration")

    full_address = fields.Char(string="Full Address", store=True)
    asset_message_ids = fields.One2many('machine.notes', 'asset_id', 'Message')

    operator_locations_ids = fields.Many2many('stock.location',
                                              'operator_locations_stock_location_rel',
                                              store=True)
    operator_location_id = fields.Many2one('stock.location',
                                           string="Operator Location",
                                           domain="[('id', 'in',operator_locations_ids)]")
    is_customer_location = fields.Boolean(string="Is Customer Location")
    equipment_trasfer_ids = fields.Many2many('account.asset.transfer',
                                             string='Equipment Location History')

    _sql_constraints = [
        ('serial_no', 'unique(serial_no)',
         "Another machine already exists with this serial number!"),
    ]


class AccountAssetType(models.Model):
    _name = 'account.asset.type'

    name = fields.Char('Equipment Type', required=True)
    beverage = fields.Boolean()
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company,
                                 ondelete='cascade')
