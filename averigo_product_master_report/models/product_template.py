from odoo import fields, models


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_onhand = fields.Float(store=True)
