from odoo import fields, models


class PackingSlipDelivery(models.TransientModel):
    _name = 'packing.slip.delivery'

    picking_ids = fields.Many2many('stock.picking', string='Picking')
    stock_move_line = fields.One2many('packing.slip.delivery.line',
                                      'picking_slip_delivery',
                                      string='Move Line')
    packing_slip_check = fields.Boolean()


class PackingSlipDeliveryLine(models.TransientModel):
    _name = 'packing.slip.delivery.line'

    picking_slip_delivery = fields.Many2one('packing.slip.delivery')
    product_id = fields.Many2one('product.product', string='product')
    picking_id = fields.Many2one('stock.picking', string='Picking')
    deliver_qty = fields.Integer('Deliver')
    order_no = fields.Char('Order #')
