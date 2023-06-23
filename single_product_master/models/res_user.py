from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    upc_code_multi = fields.Boolean(string="Featured Product",
                                    default=True)
