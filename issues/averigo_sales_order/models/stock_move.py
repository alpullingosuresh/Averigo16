from odoo import fields, models


class SaleStockMove(models.Model):
    _inherit = 'stock.move'

    order_qty = fields.Integer('Ordered Qty', inverse='_inverse_order_qty')
    qty_undelivered = fields.Integer(string="Undelivered")
    pick_invoice_check = fields.Boolean(related='picking_id.invoice_check',
                                        help="This is a direct invoice move")
    sale_move_check = fields.Boolean(default=True,
                                     help="This is used to check whether the move is created by adding product from sale order. If True then it is")
