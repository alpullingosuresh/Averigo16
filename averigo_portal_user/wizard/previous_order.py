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

from odoo import api, fields, models


class PreviousOrder(models.TransientModel):
    _name = 'previous.order'
    _description = "Previous Order"

    new_order_line_ids = fields.One2many('previous.order.line',
                                         'previous_order', String="Order Line")
    previous_check = fields.Boolean(default=False)
    partner_id = fields.Many2one('res.partner')


class PreviousOrderLine(models.TransientModel):
    _name = 'previous.order.line'
    _description = "Previous Order Line"

    previous_order = fields.Many2one('previous.order')
    select = fields.Boolean()
    order_no = fields.Char('PO #')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    state = fields.Selection([('draft', 'Order'),
                              ('sent', 'Order Sent'),
                              ('sale', 'Purchase Order'),
                              ('done', 'Locked'),
                              ('cancel', 'Cancelled')], readonly=True)
    date = fields.Datetime('Order Date')
    ordered_by = fields.Char(string='Ordered By')
