from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    exclude_from_sale = fields.Boolean(
        string='Exclude from VMS Sales',
    )
