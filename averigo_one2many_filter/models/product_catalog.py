from odoo import models, fields


class ProductCatalog(models.Model):
    _inherit = 'product.catalog'

    sow_indication_note = fields.Char(string="Warning")
    show_message = fields.Boolean()
    category_selection_ids = fields.Many2many('product.category',
                                              'rel_product_category_catalog',
                                              string='Category')
