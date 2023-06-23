from odoo import fields, models


class ProductTaxChange(models.TransientModel):
    _name = 'product.tax.change'
    _description = 'Edit Tax of Products in Micro Market'

    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.micro.market', string='Product')
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.micro.market',
                                   string='Selected Products')


class ProductUnitChange(models.TransientModel):
    _name = 'product.unit.change'
    _description = 'Edit Unit of Products in Micro Market'

    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.micro.market', string='Product')
    uom_category = fields.Integer()
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.micro.market',
                                   string='Selected Products')


class ProductPriceChange(models.TransientModel):
    _name = 'product.price.change'
    _description = 'Edit Price of Products in Micro Market'

    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.micro.market', string='Product')
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.micro.market',
                                   string='Selected Products')


class ProductMinimumChange(models.TransientModel):
    _name = 'product.min.change'
    _description = 'Edit Minimum Quantity of Products in Micro Market'

    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.micro.market', string='Product')
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.micro.market',
                                   string='Selected Products')


class ProductMaximumChange(models.TransientModel):
    _name = 'product.max.change'
    _description = 'Edit Maximum Quantity of Products in Micro Market'

    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.micro.market', string='Product')
    # select_products = fields.Boolean('Select Products')
    product_ids = fields.Many2many('product.micro.market',
                                   string='Selected Products')
