
from odoo import  fields, models

class TerminalAdd(models.Model):
    _name = 'server.error'
    _rec_name = 'rec'

    rec = fields.Text(default='Server Maintenance')
    server_flag = fields.Selection(
        [('server_down', 'Server Down'), ('server_up', 'Server Up')],
        string="Server Availability", tracking=True)
    server_details = fields.Selection(
        [('payment_server', 'Payment Server'), ('odoo_server', 'Odoo Server')],
        string="Server Nmae", tracking=True)
    error_message = fields.Text(default='Notification Text')

