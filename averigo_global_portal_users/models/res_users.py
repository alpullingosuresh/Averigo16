from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_global_user = fields.Boolean(string="Is Global portal user")

    name = fields.Char(string="Name")
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        string='Allowed Micromarkets',
                                        domain="[('location_type', '=', 'micro_market')]")
    group_ids = fields.Many2many('customer.fees', string="Groups")
    operator_report_ids = fields.Many2many('ir.actions.report',
                                           string="Available Reports")
    count_of_mm = fields.Char(string="There are", readonly=True)
    count_of_company_ids = fields.Char(readonly="1")


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    global_report = fields.Boolean()
