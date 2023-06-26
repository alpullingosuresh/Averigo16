from odoo import models, fields


class MailServerDetailsExtend(models.Model):
    _inherit = 'res.mail.config'

    notification_type = fields.Selection(
        [('terminal_offline', 'Terminal Offline/Online Notification'),
         ('feedback', 'Shopper Feedback'), ('barcode', 'Barcode Scan Failure'),
         ('inventory', 'Inventory Report'), ('weekly', 'Weekly Report'),
         ('monthly', 'Monthly Report')],
        string="Email Type", default='feedback', tracking=True)
    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")
    micro_market_ids = fields.Many2many('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")