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

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ProductSales(models.TransientModel):
    _name = 'where.sold.report'
    _description = 'Where Sold Report'
    """Where Sold Report"""

    _transient_max_count = 1

    name = fields.Char()
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    where_sold_line_ids = fields.Many2many('where.sold.line')
    product_id = fields.Many2one('product.product', string='Product')
    start_date = fields.Date()
    end_date = fields.Date()
    report_length = fields.Integer()


class ProductSalesReport(models.TransientModel):
    _name = 'where.sold.line'
    _description = 'Where Sold Report Line'
    """Where Sold Report Line"""

    cust_name = fields.Many2one('res.partner')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    product_id = fields.Many2one('product.product')
    product_code = fields.Char('Product Code')
    categ_id = fields.Many2one('product.category', 'Category')
    uom_id = fields.Many2one('uom.uom')
    quantity = fields.Integer()
    sold = fields.Float()
