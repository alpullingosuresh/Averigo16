from odoo import fields, models


class UpdateOrder(models.TransientModel):
    _name = 'update.order'
    _description = "Update Order"

    new_order_line_ids = fields.One2many('update.order.line', 'update_order',
                                         String="Order Line")
    delivery_date = fields.Datetime('Delivery Date')
    promise_date = fields.Date('Promise Date')
    sale_order_ids = fields.Many2many('sale.order', 'sale_order_update_rel',
                                      string='Sale Orders')
    update_all = fields.Boolean(default=True)


class UpdateOrderLine(models.TransientModel):
    _name = 'update.order.line'
    _description = "Update Order Line"

    update_order = fields.Many2one('update.order')
    promise_date = fields.Date(string='Promise Date')
    commitment_date = fields.Datetime('Delivery Date')
    order_id = fields.Many2one('sale.order', string='Order Number')
