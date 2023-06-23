from datetime import datetime, timedelta

from odoo import fields, models


class FeaturedProducts(models.Model):
    _name = 'featured.products'
    _rec_name = 'market_id'
    _description = 'Featured Products'

    image = fields.Binary(string='Image', required=True, copy=False)
    image_notification = fields.Image(string='Notification Image', copy=False)
    product_id = fields.Many2one('product.product', string="Product",
                                 copy=False)
    product_ids = fields.Many2many('product.product', string="Product",
                                   copy=False)
    active = fields.Boolean(string="Active", default=True)
    operator_id = fields.Many2one(
        'res.company', 'Operator', required=True, index=True,
        default=lambda self: self.env.company)
    location = fields.Many2many('res.partner',
                                'featured_products_res_partner_rel',
                                'product_id', 'partner_id',
                                domain="[('id', 'in', customer_ids)]")
    customer_ids = fields.Many2many('res.partner','featured_products_res_partner_rel2')
    micro_market_id = fields.Many2many('stock.warehouse',
                                       'featured_product_stock_warehouse_rel',
                                       'product_id',
                                       'warehouse_id')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="Stop Date")
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="Stop Time")
    mm_ids = fields.Many2many('stock.warehouse',
                              'featured_products_stock_warehouse_rel2',
                              'product_id2',
                              'warehouse_id2', copy=False)
    banner_text = fields.Char("Banner Text")
    product_line = fields.One2many('product.discount', 'special_id')
    market_id = fields.Many2one('stock.warehouse', string='Micro Market')
    categ_id = fields.Many2one('product.category', string='Category')
    categ_ids = fields.Many2many('product.category')
    market_ids = fields.Many2many('stock.warehouse')
    discount_percentage = fields.Float('Discount %')
    send_notification = fields.Boolean(default=False)
    notification = fields.Boolean('Notification', default=False)
    send_title = fields.Text(string="Notification Title")
    update_date = fields.Date(string="Update Date")
    category_ids = fields.Many2many('product.category',
                                    'av_product_category_rel',
                                    string="Category",
                                    copy=False)


class ProductFeatured(models.Model):
    _name = 'product.discount'

    special_id = fields.Many2one('featured.products', 'product_line',
                                 index=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    price = fields.Float('Price')
    discount_percentage = fields.Float('Discount %')
    discount_amount = fields.Float('Discount Amount')
    sale_price = fields.Float('Discounted Price')
    categ_id = fields.Many2one('product.category', string='Category',
                               related='product_id.categ_id')
    mm_ids = fields.Many2one('product.micro.market')
