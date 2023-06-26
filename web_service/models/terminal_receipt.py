from odoo import api, fields, models


class SendReceipt(models.TransientModel):
    _name = 'send.receipt'

    user_session = fields.Many2one('user.session.history')
    user_id = fields.Many2one('res.users')
    to_email = fields.Char()

