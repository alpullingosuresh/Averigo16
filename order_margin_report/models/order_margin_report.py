# -*- coding: utf-8 -*-
######################################################################################
#
# Cybrosys Technologies Pvt. Ltd.
#
# Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
# Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>))
#
# This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
########################################################################################
import base64
import io
import json
from datetime import datetime
import calendar

from PIL import Image
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError
from odoo.tools import date_utils

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class OrderMarginReport(models.TransientModel):
    _name = 'order.margin.report'
    _description = 'Order Margin Report'
    """Order Margin Report"""

    _transient_max_count = 1

    name = fields.Char()
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    partner_ids = fields.Many2many('res.partner', string='Customer')
    order_margin_line_ids = fields.Many2many('order.margin.line')
    start_date = fields.Date()
    end_date = fields.Date()
    report_length = fields.Integer()
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail')], string='Report Type',
        required=True,
        default='summary')
    below_margin = fields.Float('Show Below Margin %', default=100)
    show_cp_code = fields.Boolean()


class OrderMarginReportLine(models.TransientModel):
    _name = 'order.margin.line'
    _description = 'Order Margin Report Line'
    """Order Margin Report Line"""

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    partner_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Order No')
    order_date = fields.Char('Order Date')
    order_day = fields.Char('Order Day')
    total_qty = fields.Integer('Total Qty')
    selling_price = fields.Float('Selling Price')
    order_amt = fields.Float('Order Amount')
    sales_tax = fields.Float('Sales Tax')
    crv_tax = fields.Float('CRV Tax')
    discount = fields.Float('Discount')
    shipping_handling = fields.Float('S & H')
    insurance = fields.Float('Insurance')
    subtotal = fields.Float('Subtotal')
    product_cost = fields.Float('Product Cost')
    total_cost = fields.Float('Total Cost')
    margin = fields.Float('Margin')
    margin_percentage = fields.Float('Margin %')
    product_no = fields.Char('Product No')
    product = fields.Many2one('product.product', string='Product')
    cp_code = fields.Char(string="CP Code", size=60)
