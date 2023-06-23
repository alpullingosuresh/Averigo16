
from odoo import fields, models

class PutAwayRule(models.Model):
    _inherit = 'stock.putaway.rule'

    warehouse_id = fields.Many2one('stock.warehouse', 'When product arrives in')

