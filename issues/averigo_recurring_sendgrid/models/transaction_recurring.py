from odoo import models, fields


class TransactionRecurring(models.Model):
    _inherit = 'transaction.recurring'

    last_send_status = fields.Char("Last send Status")
