from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    open_case_count = fields.Integer(string="Count")
