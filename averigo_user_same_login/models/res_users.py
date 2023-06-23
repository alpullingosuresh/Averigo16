from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    username = fields.Char(required=True, string="Username")
