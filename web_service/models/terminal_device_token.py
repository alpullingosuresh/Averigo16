from odoo import fields, models


class TerminalAdd(models.Model):
    _name = 'terminal.token'

    market_id = fields.Many2one('stock.warehouse')
    app_user = fields.Many2one('res.app.users')
    device_token = fields.Char()
