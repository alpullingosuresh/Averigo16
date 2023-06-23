
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_payroll_credit = fields.Boolean(string="Payroll",
                                          default=True)

