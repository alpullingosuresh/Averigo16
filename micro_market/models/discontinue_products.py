from odoo import fields, models


class DiscontinueProducts(models.TransientModel):
    _name = 'product.discontinue'
    _description = 'Product Discontinue Wizard'
    """Used to make the micro market products Discontinued"""

    partner_ids = fields.Many2many('res.partner', string='Customer/Location',
                                   domain="[('id', 'in', partner_ids)]")
    partner_dom_ids = fields.Many2many('res.partner', 'rel_discontinue')
    micro_market_ids = fields.Many2many('stock.warehouse', domain=[
        ('location_type', '=', 'micro_market')])
    product_ids = fields.Many2many('product.product', string='Products')
    total_markets = fields.Integer()
    total_products = fields.Integer()


class ReverseDiscontinueProducts(models.TransientModel):
    _name = 'product.reverse.discontinue'
    _description = 'Reverse Product Discontinue Wizard'
    """Used to reverse the micro market products Discontinued"""

    product_id = fields.Many2one('product.micro.market', string='Products')
