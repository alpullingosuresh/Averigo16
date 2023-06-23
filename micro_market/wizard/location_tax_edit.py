from odoo import fields, models


class ProductTaxChange(models.TransientModel):
    _name = 'tax.edit'
    _description = 'Edit Tax of Location'

    micro_market_id = fields.Many2one('stock.warehouse')
    tax_amount = fields.Float()
