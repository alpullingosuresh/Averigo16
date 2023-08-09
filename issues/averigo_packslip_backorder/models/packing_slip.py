from odoo import fields, models


class PackingSlipBatch(models.Model):
    _inherit = 'stock.picking.batch'
    _description = "Packing Slip Batch"

    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In progress'), ('done', 'Done'),
         ('cancel', 'Cancelled')], default='draft', copy=False, tracking=True,
        required=True, readonly=True, store=1)
