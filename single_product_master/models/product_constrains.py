from odoo import models, api, fields


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    enable_product_code = fields.Boolean()
