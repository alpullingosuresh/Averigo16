from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    opening_entry = fields.Boolean(string="Opening Entry")

