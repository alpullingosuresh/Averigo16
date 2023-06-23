from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_location = fields.Boolean(string="Location", default=True)
    group_vending = fields.Boolean(string="Vending", default=True)
    group_store_order = fields.Boolean(string="Store Order", default=True)
    group_store_order_approval = fields.Boolean(string="Store Order Approval",
                                                default=True)
