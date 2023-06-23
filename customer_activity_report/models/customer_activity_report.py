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
from datetime import datetime, date
from odoo.exceptions import UserError

from PIL import Image
from odoo.tools import date_utils

from odoo import models, fields, api, _


class CustomerActivityReport(models.TransientModel):
    _name = 'customer.activity.report'
    _description = 'Customer Activity Report'
    """Customer Activity Report"""

    name = fields.Char()
    customer_activity_line = fields.Many2many('customer.activity.line')
    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    partner_ids = fields.Many2many('res.partner')
    customer_type_ids = fields.Many2many('res.customer.type',
                                         string='Customer Type')
    inactive_days = fields.Integer('Inactive Days')
    # sort_by = fields.Selection([('kam', 'Account Manager'), ('customer', 'Customer #'), ('cus_name', 'Customer Name')],
    #                            string='Sort By', default='customer')
    record_count = fields.Integer("Records Found")


class CustomerDetailsLine(models.TransientModel):
    _name = 'customer.activity.line'
    _description = 'Customer Activity Report Line'
    """Customer Activity Report Line"""

    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    partner_code = fields.Char(string='Customer #')
    partner_id = fields.Many2one('res.partner', string='Customer')
    bill_to_address = fields.Char('Bill To Address')
    bill_to_city = fields.Char('Bill To City')
    bill_to_state = fields.Char('Bill To State')
    bill_to_zip = fields.Char('Bill To Zip')
    last_sale_order = fields.Date('Last Sale Order Date')
    inactive_days = fields.Char('Inactive Days')
