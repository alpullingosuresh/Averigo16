from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(
        'Product Code', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
