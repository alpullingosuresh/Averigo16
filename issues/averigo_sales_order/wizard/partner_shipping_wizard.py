from odoo import models, fields


class ShipAddressWizard(models.TransientModel):
    _name = 'ship.address.wizard'

    partner_shipping_id = fields.Many2one('res.partner',
                                          string='Shipping Address')
    so_id = fields.Many2one('sale.order', string='sale order')
    invoice_id = fields.Many2one('account.move', string='Invoice')
