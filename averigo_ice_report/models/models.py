from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    legacy = fields.Char(string="Legacy System #",
                         help="Number from the legacy system")
    primary_upc2 = fields.Char(readonly=False)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    legacy = fields.Char(string="Legacy System #",
                         help="Number from the legacy system",
                         related='product_tmpl_id.legacy', store=True)


class MicroMarket(models.Model):
    _inherit = 'stock.warehouse'

    store_no = fields.Char(string="Store #", help="Store Number")
