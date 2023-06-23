from odoo import models, fields


class BackorderReason(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    reason_note = fields.Text()
