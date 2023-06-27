from odoo import models, fields


class AverigoRecurring(models.Model):
    _inherit = 'transaction.recurring'

    is_maintenance = fields.Boolean(copy=False)
    machine_id = fields.Many2one('account.asset', string="Equipment")
