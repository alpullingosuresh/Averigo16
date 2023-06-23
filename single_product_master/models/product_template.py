from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = "Product"

    subsidy_check = fields.Boolean(default=False)
    fuel_check = fields.Boolean(default=False)
    hazard_check = fields.Boolean(default=False)
