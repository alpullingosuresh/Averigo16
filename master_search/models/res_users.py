

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_search = fields.Boolean(string="Search",
                                  default=True)

