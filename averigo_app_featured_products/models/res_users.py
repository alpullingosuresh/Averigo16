
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_featured_product = fields.Boolean(string="Featured Product",
                                            default=True)
