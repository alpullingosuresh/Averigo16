# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>))
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
from datetime import date
import datetime

from odoo import models, fields, api, _


class SaleOrderPortal(models.Model):
    _inherit = 'sale.order'

    customer_user_id = fields.Many2one('res.users')
    portal_state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Submitted'),
        ('sale', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, store=True, index=True,
        tracking=3, default='draft')
    product_assoc_ids = fields.Many2many('product.product',
                                         'customer_portal_product_rel',
                                         string='Customer Products')
    order_type = fields.Many2many('order.type', 'order_type_product_rel',
                                  string='Order Types')
    order_type_ids = fields.Many2many('order.type',
                                      'order_type_ids_product_rel')
    customer_product_filter_ids = fields.Many2many('product.product',
                                                   'customer_product_filter_rel')
    price_check = fields.Boolean('Portal Price Check')
    invoice_check = fields.Boolean('Portal Invoice Check')
    image_check = fields.Boolean('Portal Image Check')
    order_type_product_ids = fields.One2many('order.type.product',
                                             'sale_order')
    select_order_type_products = fields.Boolean('Select All', default=True)
    product_type_length = fields.Integer(string="Count")
    customer_product_id = fields.Many2many('customer.product',
                                           'customer_product_sale_rel',
                                           string='Customer Products')
    order_no = fields.Char('PO #')
    order_no_check = fields.Boolean()
    ordered_by = fields.Char('Ordered By')
    login_by = fields.Many2one('res.partner', string='Login By',
                               default=lambda self: self.env.user.partner_id)
    confirmed_by = fields.Char('Confirmed By')
    order_form_check = fields.Boolean(default=True)
    total_item = fields.Integer('Total Item')
    order_line_ids = fields.One2many('sale.order.line', 'order_id',
                                     string='Order Lines',
                                     states={'cancel': [('readonly', True)],
                                             'done': [('readonly', True)]},
                                     copy=False,
                                     auto_join=True)
    po_date = fields.Date('PO Date', default=date.today(), readonly=True)
    year = fields.Char(string='Year', required=True,
                       default=lambda x: str(datetime.datetime.now().year))

    notification_count = fields.Integer()
    parent_partner_id = fields.Many2one('res.partner',
                                        related='partner_id.parent_id')
    product_qty = fields.Integer(string='Ordered Qty', store=True)
    product_delivered_qty = fields.Integer(string='Delivered Qty',
                                           store=True)
    undelivered_qty = fields.Integer(string='Undelivered Qty',
                                     store=True)


class OrderTypeProduct(models.Model):
    _name = 'order.type.product'
    _description = 'Order Type Product in Customer'
    """Product from Selected Order Type"""

    sale_order = fields.Many2one('sale.order')
    order_type = fields.Many2one('order.type')
    product_id = fields.Many2one('product.product')
    select_product = fields.Boolean('Add', default=True)
    product_code = fields.Char('Product code')
    name = fields.Char('Description')
    uom_id = fields.Many2one('uom.uom')
    unit_price = fields.Float('Unit Price')


class SaleOrderLineDate(models.Model):
    _inherit = 'sale.order.line'

    order_date = fields.Datetime(related='order_id.date_order', store=True)
    last_order_qty = fields.Integer('Last Ordered Quantity')
    order_type = fields.Many2one('order.type', string='Order Types')
    image_portal = fields.Image(max_width=32, max_height=32,
                                related='product_id.image_1920')
