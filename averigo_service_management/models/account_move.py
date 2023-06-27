from odoo import fields, models


class CaseAccountMove(models.Model):
    _inherit = "account.move"

    case_id = fields.Many2one('case.management')
