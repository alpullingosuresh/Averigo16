from odoo import fields, models


class PriceChange(models.TransientModel):
    _name = 'price.change'
    _description = 'Price Change in Product Catalog and associated Micro Market'

    catalog_product_id = fields.Many2one('product.product.catalog')
    select_micro_market = fields.Selection(
        [('all', 'All'), ('select', 'Select Micro Markets')], default='select')
    # select_micro_market = fields.Boolean('Select Micro Market')
    micro_market_id = fields.Many2many('stock.warehouse')
    list_micro_market_id = fields.Many2many('stock.warehouse', 'catalog_rel')
    catalog_product_ids = fields.Many2many('product.product.catalog')
