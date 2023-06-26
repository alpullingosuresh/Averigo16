from odoo import fields, models


class ProductAdd(models.TransientModel):
    _name = 'product.add'
    _description = 'Product Add in Product Catalog and associated Micro Market'

    catalog_product_ids = fields.Many2many('product.product')
    catalog_id = fields.Many2one('product.catalog')
    select_micro_market = fields.Selection(
        [('all', 'All'), ('select', 'Select Micro Markets')], default='select')
    micro_market_ids = fields.Many2many('stock.warehouse')
    list_micro_market_id = fields.Many2many('stock.warehouse',
                                            'catalog_product_rel')
