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
from odoo import models, fields


class CustomerDetailsReport(models.TransientModel):
    _name = 'customer.details.report'
    _description = 'Customer Details Report'
    """Customer Details Report"""

    name = fields.Char()
    customer_details_line = fields.Many2many('customer.details.line')
    include_all = fields.Boolean('Include All', default=True)
    kam = fields.Boolean('Accounts Manager')
    city = fields.Boolean('City')
    state = fields.Boolean('State')
    customer = fields.Boolean('Customer')
    county = fields.Boolean('county')
    zip = fields.Boolean('Zip Code')
    cus_type_bol = fields.Boolean('Customer Type')
    cus_status_bol = fields.Boolean('Customer Status')
    customer_type = fields.Many2many('res.customer.type',
                                     string='Customer Type')
    customer_status = fields.Selection(
        [('active', 'Active'), ('archive', 'Archive')],
        string='Customer Status',
        default='active')
    status_check = fields.Boolean(default=True)
    type = fields.Selection(
        [('contact', 'Contact'), ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'), ("private", "Private Address")],
        string='Address Type',
        default='contact')
    sort_by = fields.Selection(
        [('customer', 'Customer #'), ('cus_name', 'Customer Name'),
         ('kam', 'Account Manager'),
         ('cus_city', 'Customer City'), ("cus_state", "Customer State"),
         ("cus_county", "Customer County"), ("cus_zip", "Customer Zip Code")],
        string='Sort By',
        default='customer')
    sort_asc = fields.Boolean('Ascending')
    sort_des = fields.Boolean('Descending')
    record_count = fields.Integer("Records Found")
    states = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                              default='draft')


class CustomerDetailsLine(models.TransientModel):
    _name = 'customer.details.line'
    _description = 'Customer Details Report Line'
    """Customer Details Report Line"""

    partner_code = fields.Char(string='Customer #')
    cus_name = fields.Char('Customer')
    cus_name_id = fields.Many2one('res.partner', string='Customer')
    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    customer_type = fields.Char(string='Customer Type')
    status = fields.Char('Status')
    contact = fields.Char('Contact Name')
    email = fields.Char('Email')
    address = fields.Char('Address')
    city = fields.Char('City')
    state = fields.Char('State')
    county = fields.Char('county')
    zip = fields.Char('Zip Code')
    phone = fields.Char('Phone #')
