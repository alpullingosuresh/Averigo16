from odoo import models, fields


class SessionProductList(models.Model):
    _inherit = 'session.product.list'

    discount_applied = fields.Float(compute='compute_discount_applied',
                                    store=True)
