

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_quick_update = fields.Boolean(string="Quick Update",
                                        default=True)

