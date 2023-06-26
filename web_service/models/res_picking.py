

from odoo import models, fields


class InvoicePicking(models.Model):
    _inherit = 'stock.picking'

    app_user = fields.Many2one('res.app.users')
    transaction_id = fields.Char()
    full_receive = fields.Boolean(default=False,copy=False)

