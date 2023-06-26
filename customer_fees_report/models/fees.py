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
from datetime import date, datetime

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class FeesDistribution(models.Model):
    _name = 'fees.distribution'
    _inherit = 'mail.thread'
    _description = "Fees Distribution"

    name = fields.Char(required=1, tracking=True)
    operator_ids = fields.Many2many('res.company')
    update_mm = fields.Boolean()
    dom_mm_ids = fields.Many2many('stock.warehouse', 'dom_mm_rel')
    micro_market_ids = fields.Many2many('stock.warehouse', 'micro_market_rel',
                                        domain="[('location_type', '=', 'micro_market')]",
                                        tracking=True, copy=False)
    group_id = fields.Many2one('customer.fees', tracking=True)
    group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    group_fees_percentage = fields.Float(tracking=True)
    brand_id = fields.Many2one('customer.fees', tracking=True)
    brand_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    brand_fees_percentage = fields.Float(tracking=True)
    management_id = fields.Many2one('customer.fees', tracking=True)
    management_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    management_fees_percentage = fields.Float(tracking=True)
    purchasing_group_id = fields.Many2one('customer.fees', tracking=True)
    purchasing_group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    purchasing_group_fees_percentage = fields.Float(tracking=True)
    national_sales_team_id = fields.Many2one('customer.fees', tracking=True)
    national_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    national_sales_fees_percentage = fields.Float(tracking=True)
    local_sales_team_id = fields.Many2one('customer.fees', tracking=True)
    local_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    local_sales_fees_percentage = fields.Float(tracking=True)
    additional_group1_id = fields.Many2one('customer.fees', tracking=True)
    additional_group1_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    additional_group1_fees_percentage = fields.Float(tracking=True)
    additional_group2_id = fields.Many2one('customer.fees', tracking=True)
    additional_group2_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    additional_group2_fees_percentage = fields.Float(tracking=True)
    additional_group3_id = fields.Many2one('customer.fees', tracking=True)
    additional_group3_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    additional_group3_fees_percentage = fields.Float(tracking=True)
    cc_fees = fields.Float(tracking=True)
    app_fees = fields.Float(tracking=True)
    stored_fund_fees = fields.Float(tracking=True)
    platform_fees = fields.Float(tracking=True)
    platform_fees_type = fields.Selection(
        [('percentage', 'Percentage'), ('fixed', 'Fixed')], required=True,
        tracking=True, default='percentage')
    platform_fees_per_day = fields.Float(store=1)
    commission_percentage = fields.Float(tracking=True)
    room_cc = fields.Float('Hotel CC', tracking=True)
    cash_adj = fields.Float(tracking=True)
