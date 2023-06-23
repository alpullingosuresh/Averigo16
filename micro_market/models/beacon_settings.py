from odoo import models, fields


class BeaconSettings(models.Model):
    _name = 'uuid.uuid'
    _description = 'Beacon Settings'
    """Beacon Settings"""

    name = fields.Char()
    beacon_major = fields.Char(required=True, tracking=True, copy=False)
    beacon_minor = fields.Char(required=True, tracking=True, copy=False)
    merchant_id = fields.Char('Merchant ID', tracking=True, copy=False)
    terminal_id = fields.Char('Terminal ID', tracking=True, copy=False)
    apriva_client_id = fields.Char('Apriva Client ID', tracking=True,
                                   copy=False)
    secret_key = fields.Char(copy=False)
    secret_key_masked = fields.Char(copy=False)
    micro_market_id = fields.Many2one('stock.warehouse', domain=[
        ('location_type', '=', 'micro_market')])
    operator_id = fields.Many2one('res.company', string='Operator',
                                  related='micro_market_id.company_id')
    partner_id = fields.Many2one('res.partner', string='Operator',
                                 related='micro_market_id.partner_id')
    mask_secret_key = fields.Boolean()
