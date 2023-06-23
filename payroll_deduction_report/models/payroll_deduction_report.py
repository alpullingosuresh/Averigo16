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


import base64
import io
import json
from collections import defaultdict

from PIL import Image
from dateutil.relativedelta import relativedelta

from odoo.fields import Date
from datetime import date, datetime
from odoo.tools import date_utils

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PayrollDeductionReport(models.TransientModel):
    _name = 'payroll.deduction.report'
    _description = "Payroll Deduction Report"
    _rec_name = "name"

    name = fields.Char(default="Payroll Deduction Report")
    partner_ids = fields.Many2many('res.partner', 'multi_partner_ids',
                                   string="Customer",
                                   domain="[('id', 'in', customer_ids)]")
    customer_ids = fields.Many2many('res.partner', 'micro_market_partner_ids')

    search_string = fields.Char(string='Item Search')
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')

    record_count = fields.Integer("Records Found")
    mm_ids = fields.Many2many('stock.warehouse', string='Micro Markets',
                              domain="[('id', 'in', micro_market_ids)]")
    micro_market_ids = fields.Many2many('stock.warehouse')
    line_ids = fields.One2many('payroll.deduction.report.lines', 'report_id',
                               string="Invoice")
    is_consolidated = fields.Boolean(default=True)
    product = fields.Boolean('Item')
    quantity = fields.Boolean('Quantity')
    price_total = fields.Float(string='Total', store=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')


class PayrollDeductionReportLines(models.TransientModel):
    _name = 'payroll.deduction.report.lines'
    _description = "Payroll Deduction Report Lines"

    user_session_history_id = fields.Many2one("user.session.history",
                                              string="Session")
    session_product_list = fields.Many2one("session.product.list",
                                           string="Session")
    product_id = fields.Many2one("product.product", string="Item",
                                 related='session_product_list.product_id')
    session_number = fields.Char(string="Session Number",
                                 related='user_session_history_id.sequence')
    date = fields.Date(string="Date")
    price_total = fields.Float(string='Total', store=True)
    total_sales_amount = fields.Float(string='Sales Amount', store=True)
    user_total = fields.Monetary(string='Total', store=True, default=0.0)
    micro_market_id = fields.Many2one('stock.warehouse', string="Micro Market",
                                      store=True)
    app_user = fields.Many2one('res.app.users', string="User")
    app_user_name = fields.Char(string="User", related='app_user.name')
    email = fields.Char(string="Email", related='app_user.email')
    quantity = fields.Integer(string='Quantity',
                              help="The optional quantity expressed by this "
                                   "line, eg: number of product sold. "
                                   "The quantity is not a legal requirement "
                                   "but is very useful for some reports.",
                              related='session_product_list.qty')
    report_id = fields.Many2one('payroll.deduction.report')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
