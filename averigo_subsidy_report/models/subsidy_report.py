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
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError
from odoo.tools import date_utils

from odoo import models, fields, api, _


class ProductSales(models.TransientModel):
    _name = 'subsidy.report'
    _description = 'Subsidy Report'
    """Subsidy Report"""

    _transient_max_count = 1

    name = fields.Char(default='Subsidy Report')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    partner_ids = fields.Many2many('res.partner', 'partner_subsidy_rel',
                                   string='Customer',
                                   domain="[('id', 'in', customer_ids)]")
    customer_ids = fields.Many2many('res.partner', 'customer_subsidy_rel')
    mm_dom_ids = fields.Many2many('stock.warehouse', 'mom_dom_subsidy_rel')
    micro_market_ids = fields.Many2many(
        'stock.warehouse', 'micro_market_subsidy_rel',
        domain="[('location_type', '=', 'micro_market')]")
    start_date = fields.Date()
    end_date = fields.Date()
    categ_ids = fields.Many2many('product.category', 'categ_subsidy_rel',
                                 domain="[('id', 'in', categ_dom_ids)]")
    categ_dom_ids = fields.Many2many('product.category',
                                     'categ_dom_subsidy_rel')
    line_ids = fields.One2many('subsidy.report.line', 'report_id')
    report_length = fields.Integer()
    report_type = fields.Selection(
        [('product', 'By Product'), ('category', 'By Category')],
        'Report Type', default='product')


class ProductSalesReport(models.TransientModel):
    _name = 'subsidy.report.line'
    _description = 'Subsidy Report Line'
    """Subsidy Report Line"""

    name = fields.Char(store=True, related='product_id.name')
    report_id = fields.Many2one('subsidy.report')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    market_product = fields.Many2one('product.micro.market')
    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.product')
    product_code = fields.Char(store=True, related='product_id.default_code')
    categ_id = fields.Many2one('product.category', 'Category')
    subsidy = fields.Float()
    total_subsidy = fields.Float()
    list_price = fields.Float('Selling Price')
    total_sold = fields.Integer()
