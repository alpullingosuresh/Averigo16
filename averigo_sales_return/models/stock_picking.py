from odoo import models, fields, api, _


class SalesReturnPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_date = fields.Date('Invoice Date',
                               related='account_move_id.invoice_date')
    return_from = fields.Selection(
        [('customer', 'Customer'), ('truck', 'Truck')], default='customer')
    returned_invoice_ids = fields.Many2many('account.move')


class SalesReturnStockMove(models.Model):
    _inherit = 'stock.move'

    destination_location_filter = fields.Many2many('stock.location')
    qty_undelivered_return = fields.Integer('Undelivered Qty')
