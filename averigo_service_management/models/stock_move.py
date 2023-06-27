from odoo import fields, models


class CaseStockMove(models.Model):
    _inherit = "stock.move"

    case_id = fields.Many2one('case.management')
