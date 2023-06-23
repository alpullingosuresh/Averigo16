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

from PIL import Image
from odoo import models, fields, api
from odoo.tools import date_utils, profile


# try:
#     from odoo.tools.misc import xlsxwriter
# except ImportError:
#     import xlsxwriter


class StockValueReport(models.TransientModel):
    _name = 'stock.value.report'
    _description = 'Stock Value Report'
    """Stock Value Report"""

    name = fields.Char()
    mm_dom_ids = fields.Many2many('stock.warehouse', 'mom_dom_stock_rel')
    micro_market_id = fields.Many2many('stock.warehouse',
                                       'micro_market_stock_rel')
    categ_id = fields.Many2many('product.category')
    as_on_date = fields.Datetime(string='As On Date', required=True,
                                 default=fields.Datetime.now)
    stock_value_line = fields.Many2many('stock.value.line')
    partner_id = fields.Many2many('res.partner', 'partner_stock_rel',
                                  string='Customer',
                                  domain="[('id', 'in', customer_ids)]")
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail'),
         ('cat_wise', 'Category Wise')],
        string='Report Type',
        default='summary')
    cat_check = fields.Boolean(default=True)
    check = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', 'Operator',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    total_qty = fields.Integer(string="Total Stock On Hand")
    total_cost = fields.Monetary(string="Total Amount",
                                 currency_field="currency_id", )
    customer_ids = fields.Many2many('res.partner', 'customer_stock_rel')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')
    record_count = fields.Integer("Records Found")


class StockValueLine(models.TransientModel):
    _name = 'stock.value.line'
    _description = 'Stock Value Report Line'
    """Stock Value Report Line"""

    item = fields.Char('Item #')
    item_desc = fields.Char('Item Description')
    micro_market_id = fields.Many2one('stock.warehouse', string='Micro Market',
                                      domain="[('location_type', '=', 'micro_market')]")
    categ_id = fields.Many2one('product.category', string='Category')
    stock_on_hand = fields.Float('Stock On Hand',
                                 digits='Product Unit of Measure')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    cost_price = fields.Monetary(string="Cost", default=0,
                                 currency_field="currency_id")
    amount = fields.Monetary(string="Amount", default=0,
                             currency_field="currency_id")
    cat_id = fields.Many2one('product.category', string='Category Name')
    cat_code = fields.Char('Category Code')
