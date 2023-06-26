from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# <-----------> Workflow Equipment Activity <--------->
#
# -----------------------> install <---------------------------------
# Equipment  -----initial ---> Warehouse ---install---> Customer location. (Micromarket/Order)
#
# ----------------------> Remove <-----------------------------------
# Equipment --initial --> warehouse |--install--->|Customer location
#                                   |<---Remove---|
#
# -------------------------> Retire <--------------------------------
# Equipment --initial --> warehouse |--install--->|Customer location
#                            |      |<---Remove---|
#                            |
#                     |---Retire----|
#
# ----------------------> Exchange <---------------------------------
#                                         [1]
# Equipment --initial --> warehouse |--install--->|Customer location
#                             |           [2]
#                             |     |<---Remove---|
#                             |           [3]
# New Equipment --initial --> |---->|--install--->|Customer location


class EquipemtActivityType(models.Model):
    _name = 'equipment.activity.type'

    name = fields.Char(string="Type name")


class AccountAssetTransfer(models.Model):
    _name = "account.asset.transfer"
    _description = "Equipment Transfer"
    _inherit = ['mail.thread']
    _order = 'start_date desc,id desc'

    name = fields.Char(string="Name", required=True, copy=False, default='New',
                       readonly=True)
    transferred_asset_id = fields.Many2one('account.asset',
                                           string="Equipment to be Transferred",
                                           required=True,
                                           states={
                                               'done': [('readonly', True)]})

    transferred_asset_serial_no = fields.Char('Serial No', copy=False,
                                              required=True,
                                              related='transferred_asset_id.serial_no')

    transferred_asset_name = fields.Char(string="Equipment Name",
                                         related="transferred_asset_id.name")
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.user.company_id,
                                 states={'done': [('readonly', True)]},
                                 required=True)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related="company_id.currency_id",
                                  states={'done': [('readonly', True)]})
    purchase_price = fields.Monetary(string="Purchase Price",
                                     related="transferred_asset_id.purchase_value",
                                     store=True)
    residual_value = fields.Monetary(string="Residual Value",
                                     related="transferred_asset_id.value_residual",
                                     store=True)
    source_location_id = fields.Many2one('stock.location',
                                         string="Source Location",
                                         states={'done': [('readonly', True)]})
    destination_location_id = fields.Many2one('stock.location',
                                              string="Destination Location", )
    destination_location_id_mm = fields.Many2one('stock.location',
                                                 string="Destination Location",
                                                 store=True,
                                                 states={'done': [
                                                     ('readonly', True)]})

    @api.depends('transfer_micro_market_id', 'transfer_location_type',
                 'transferred_asset_id')
    def _compute_destination_location_mm(self):
        """Function compute the location of micromarket"""
        if self.transfer_location_type == 'micro_market' and self.transfer_micro_market_id:
            locations = self.env['stock.location'].search(
                [('warehouse_id', '=', self.transfer_micro_market_id.id),
                 ('is_bin_location', '=', True),
                 ('company_id', '=', self.env.company.id)]).id
            self.destination_location_id_mm = locations
        else:
            self.destination_location_id_mm = False

    user_id = fields.Many2one('res.users', string="Responsible Person",
                              states={'done': [('readonly', True)]})
    asset_operation_type_id = fields.Many2one('asset.transfer.type',
                                              string="Operation Type",
                                              states={'done': [
                                                  ('readonly', True)]})
    asset_transfer_type = fields.Selection(
        [('wtl', 'Warehouse to Location'), ('wtw', 'Warehouse to Warehouse'),
         ('ltw', 'Location to Warehouse'),
         ('ltl', 'Location to Location'), ], 'Transfer Type',
        states={'done': [('readonly', True)]})
    reason = fields.Text(string="Reason For Transfer",
                         states={'done': [('readonly', True)]})
    analytic_account_id = fields.Many2one('account.analytic.account',
                                          string="Analytic Account",
                                          states={
                                              'done': [('readonly', True)]})
    state = fields.Selection(selection=[('draft', 'Draft'), ('done', 'Done'),
                                        ('cancelled', 'Cancelled'), ],
                             string="Status", default='draft',
                             track_visibility="onchange")
    create_date = fields.Datetime(string="Create Date",
                                  default=fields.Datetime.now, readonly=True, )
    transferred_date = fields.Date(string="Transferred Date",
                                   states={'done': [('readonly', True)]})
    #        default=fields.Date.today(),
    transfer_user_id = fields.Many2one('res.users', 'Transfer By',
                                       readonly=True)
    asset_sequence_number = fields.Char(string="Equipment Sequence Number",
                                        related="transferred_asset_id.code", )
    asset_description = fields.Text(string="Asset Discription",
                                    related="transferred_asset_id.note")
    asset_date_purchased = fields.Date(string="Asset Date Purchased",
                                       related="transferred_asset_id.effective_date")
    asset_purchase_cost = fields.Monetary(string="Asset Purchase Cost",
                                          related="transferred_asset_id.value_residual")
    internal_note = fields.Text(string="Internal Note",
                                states={'done': [('readonly', True)]})
    transfer_location_type = fields.Selection(
        [('micro_market', 'Micro market'), ('order', 'Order')],
        string='Location Type',
        readonly=True,
        states={'draft': [('readonly', False)]})
    transfer_micro_market_id = fields.Many2one('stock.warehouse', domain=[
        ('location_type', '=', 'micro_market')],
                                               readonly=True,
                                               states={'draft': [
                                                   ('readonly', False)]})
    transfer_warehouse_id = fields.Many2one('stock.warehouse', domain=[
        ('location_type', '=', 'view')],
                                            readonly=True, states={
            'draft': [('readonly', False)]})
    transfer_machine_location_ids = fields.Many2many('stock.location',
                                                     'transfer_location_rel',
                                                     store="true")
    transfer_machine_location_ids_mm = fields.Many2many('stock.location',
                                                        'transfer_location_rel_mm',
                                                        store="true")
    type = fields.Many2one('case.management.type', string="Type",
                           states={'done': [('readonly', True)]})
    transfer_location_partner_id = fields.Many2one('res.partner',
                                                   string="Customer",
                                                   states={'done': [
                                                       ('readonly', True)]},
                                                   domain="[('operator_id', '=', company_id),('is_customer','=',True),('type','=','contact'),('parent_id','=',False)]")
    customer_ids = fields.Many2many('res.partner',
                                    store="true")
    mm_ids = fields.Many2many('stock.warehouse',
                              store="true")
    area = fields.Char(string="Area of the machine")
    equipment_state = fields.Selection(
        selection=[("draft", "Active"), ("open", "In Service"),
                   ("removed", "InActive"), ], string="Status", )
    disable_transfer = fields.Boolean(string="Disable the transfer button")
    equipment_warehouse = fields.Many2one('stock.location')
    operator_locations_ids = fields.Many2many('stock.location',
                                              'operator_location_rel',
                                              related='transferred_asset_id.operator_locations_ids')

    # Exchange section
    new_equipment = fields.Many2one('account.asset',
                                    string="Equipment No/Name")
    new_equipment_serial_no = fields.Char('Serial No', copy=False,
                                          required=True,
                                          related='new_equipment.serial_no')
    new_location_type = fields.Selection(
        [('micro_market', 'Micromarket'), ('order', 'Order')],
        string='Location Type',
        default="micro_market", readonly=True,
        states={'draft': [('readonly', False)]})
    new_transfer_micro_market_id = fields.Many2one('stock.warehouse', domain=[
        ('location_type', '=', 'micro_market')],
                                                   readonly=True, store=True,
                                                   states={'draft': [
                                                       ('readonly', False)]})
    new_transfer_machine_location_ids = fields.Many2many('stock.location',
                                                         'rel_new_transfer_machine_location_ids_stock_location',
                                                         store=True
                                                         )
    new_transfer_machine_location_ids_mm = fields.Many2many('stock.location',
                                                            'rel_new_transfer_machine_location_ids_mm_stock_location',
                                                            'transfer_location_stock_location_rel',
                                                            store=True)
    new_start = fields.Datetime(string="Start Date",
                                default=fields.Datetime.now)
    new_equipment_warehouse_id = fields.Many2one('stock.location',
                                                 string="New Equipment Warehouse")
    new_destination_location_id = fields.Many2one('stock.location',
                                                  string="Destination Location Area", )
    new_destination_location_id_mm = fields.Many2one('stock.location',
                                                     string="Destination Location Miro Market",
                                                     store=True,
                                                     states={'done': [
                                                         ('readonly', True)]})
    new_initial_meter_reading = fields.Float(string="Initial Meter Reading")
    new_relative_commission_rate = fields.Float(
        string="Relative Commission Rate")
    destination_location = fields.Char('Location/ Area')
    customer_name = fields.Char('Customer Name')

    activity_type = fields.Selection(
        [('install', 'Install'), ('remove', 'Remove'),
         ('exchange', 'Exchange'), ('retire', 'Retire')],
        string="Activity Type", default='install')

    start_date = fields.Datetime(string="Start Date",
                                 default=fields.Datetime.now)
    initial_meter_reading = fields.Float(String="Initial Meter Reading")
    relative_commission_rate = fields.Float(String="Relative Commission Rate")
    disposition_date = fields.Date(string="Disposition Date",
                                   default=fields.Date.today)
    retired_reason = fields.Selection(
        [('damage', 'Damage'), ('junk', 'Junk'), ('scrap', 'Scrap'),
         ('sold', 'Sold')],
        string="Retired Date")


class AssetTransferType(models.Model):
    _name = "asset.transfer.type"
    _rec_name = "name"

    sequence_code = fields.Char(string="Code", required=True)
    code = fields.Selection([('incoming', 'Receipt'), ('outgoing', 'Delivery'),
                             ('internal', 'Internal Transfer')],
                            'Type of Operation', required=True)
    name = fields.Text(string="Name", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company)


class CaseManagementType(models.Model):
    _name = "case.management.type"
    _description = "Case Management Type"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company)
    install = fields.Boolean('Install')
    removal = fields.Boolean('Removal')
    is_preventive = fields.Boolean('Preventive', copy=False)
