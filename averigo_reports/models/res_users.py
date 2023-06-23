from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    operator_report_ids = fields.Many2many('ir.actions.report',
                                           string='Allowed Reports')
