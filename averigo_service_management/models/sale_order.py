from odoo import fields, models


class CaseSaleOrder(models.Model):
    _inherit = "sale.order"

    case_id = fields.Many2one('case.management')
