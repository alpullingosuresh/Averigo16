from odoo import api, fields, models
import odoo.addons.decimal_precision as dp
from datetime import datetime


class ConvertPurchaseOrder(models.TransientModel):
    _name = 'convert.order'
    _description = "Convert Purchase Order"

    new_order_line_ids = fields.One2many('convert.order.line', 'convert_order',
                                         String="Order Line")
    order_id = fields.Many2one('sale.order', string='Order', required=True,
                               ondelete='cascade', index=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True)
    date_order = fields.Date(string='Order Date', required=True, copy=False,
                             default=fields.Date.today())
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    po_id = fields.Many2one('purchase.order', domain=[('state', '=', 'draft')])
    po_filter_ids = fields.Many2many('purchase.order',
                                     'convert_purchase_order_rel')


class ConvertOrderLine(models.TransientModel):
    _name = 'convert.order.line'
    _description = "Convert Purchase Order Line"

    convert_order = fields.Many2one('convert.order')
    product_id = fields.Many2one('product.product', string="Product",
                                 required=True)
    name = fields.Char(string="Description")
    product_qty = fields.Integer(string='Quantity', required=True)
    date_planned = fields.Datetime(string='Scheduled Date',
                                   default=datetime.today())
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')
    item_cost = fields.Float(string='Item Cost', required=True,
                             digits=dp.get_precision('Product Price'))
    product_subtotal = fields.Float(string="Sub Total")
