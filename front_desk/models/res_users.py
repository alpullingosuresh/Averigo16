

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_front_desk = fields.Boolean(string="Front Desk",
                                      default=True)

