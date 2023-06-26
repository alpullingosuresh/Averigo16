from odoo import fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'mail.thread', 'mail.activity.mixin']
    _description = "Customer/Vendor"

    name = fields.Char(index=True, size=120)
    kam = fields.Many2one('hr.employee', string="Primary Accounts Manager")
    is_customer = fields.Boolean(string="Is Customer")
    open_order_count = fields.Integer(string="Open Orders")
    code = fields.Char(string='Customer #', copy=False)
    operator_id = fields.Many2one('res.company', string="Operator",
                                  default=lambda self: self.env.company.id)
    address = fields.Char()
    county = fields.Char()
    zip = fields.Char(string="ZIP", size=5)
    ship_via = fields.Many2one('ship.via', string='Ship Via')
    nick_name = fields.Char(string="Nickname", size=120)
    parent_partner_id = fields.Many2one('res.partner', string="Parent")
    parent_id = fields.Many2one('res.partner',
                                domain=[('is_customer', '=', True)])
    division = fields.Many2one('res.division')
    price_category = fields.Selection(
        [('list_price_1', 'List Price 1'), ('list_price_2', 'List Price 2'),
         ('list_price_3', 'List Price 3')])
    is_taxable = fields.Boolean(string="Taxable Customer")
    customer_type = fields.Many2many('res.customer.type',
                                     string="Customer Type")
    in_service_date = fields.Date(default=fields.Date.today)
    out_service_date = fields.Date()
    monthly_statement = fields.Boolean()
    master_invoice = fields.Boolean()
    group_master_invoice = fields.Selection(
        [('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    fuel_charge = fields.Boolean()
    hazard_fee = fields.Boolean()
    out_reason = fields.Text(string="Out Service Reason")
    special_notes = fields.Text(string="Special Notes")

    contract_id = fields.Many2one('customer.contract', string="Contract")

    contract_warning = fields.Boolean(string='Contract Warning', store=True,
                                      groups="hr.group_hr_user")
    contracts_count = fields.Integer(string="Contract Count")
    is_primary = fields.Boolean(string="Primary Contact", default=False)
    duplicate_primary = fields.Boolean(string="Primary Contact Set")
    subsidy = fields.Boolean('Subsidy')
    subsidy_amount = fields.Float('Subsidy Amount')
    subsidy_percentage = fields.Float('Subsidy %')
    po_check = fields.Boolean()
    po_no = fields.Char()
    activities_count = fields.Integer()
    nick_name_view = fields.Char()
    primary_contact_id = fields.Many2one('res.partner')

    _sql_constraints = [("code_uniq", "unique(code, operator_id)",
                         "Customer # should be unique!")]


class ShippingVia(models.Model):
    _name = 'ship.via'
    _description = "Ship Via"

    name = fields.Char(string='Name', required=True)
    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id)
