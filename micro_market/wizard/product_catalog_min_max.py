from odoo import fields, models


class ProductMinimumChange(models.TransientModel):
    _name = 'catalog.min.change'
    _description = 'Edit Minimum Quantity of Products in Catalog'

    catalog_id = fields.Many2one('product.catalog')
    product_id = fields.Many2one('product.product.catalog', string='Product')
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.product.catalog',
                                   string='Selected Products')


class ProductMaximumChange(models.TransientModel):
    _name = 'catalog.max.change'
    _description = 'Edit Maximum Quantity of Products in Catalog'

    catalog_id = fields.Many2one('product.catalog')
    product_id = fields.Many2one('product.product.catalog', string='Product')
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.product.catalog',
                                   string='Selected Products')
