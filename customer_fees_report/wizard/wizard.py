import io
import json
import logging
from datetime import datetime, timedelta

import xlsxwriter
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.tools import date_utils, UserError
from odoo.exceptions import MissingError, UserError, ValidationError, \
    AccessError

_logger = logging.getLogger(__name__)


class CustomerFeesReportLine(models.TransientModel):
    """"""
    _name = 'customer.fees.line'

    micro_market = fields.Many2one('stock.warehouse')
    street = fields.Char('Address', related='micro_market.street', store=1)
    zip = fields.Char('Zip', related='micro_market.zip', store=1)
    city = fields.Char('City', related='micro_market.city', store=1)
    state_id = fields.Many2one('res.country.state', string="State",
                               related='micro_market.state_id', store=1)
    operator_id = fields.Many2one('res.company',
                                  related='micro_market.company_id', store=1)
    report_id = fields.Many2one('customer.fees.report')
    net_sales = fields.Float()
    customer = fields.Many2one('res.partner')
    company_name_id = fields.Many2one('customer.fees')
    group_id = fields.Many2one('customer.fees')
    brand_id = fields.Many2one('customer.fees')
    management_id = fields.Many2one('customer.fees')
    purchasing_group_id = fields.Many2one('customer.fees')
    national_sales_team_id = fields.Many2one('customer.fees')
    local_sales_team_id = fields.Many2one('customer.fees')
    group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    brand_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    management_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    purchasing_group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')])
    national_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    local_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    group_fees_percentage = fields.Float()
    group_fees = fields.Float()
    brand_percentage = fields.Float()
    brand_fees = fields.Float()
    management_percentage = fields.Float()
    management_fees = fields.Float()
    purchasing_group_fees_percentage = fields.Float()
    purchasing_group_fees = fields.Float()
    national_sales_fees_percentage = fields.Float()
    national_sales_fees = fields.Float()
    local_sales_fees_percentage = fields.Float()
    local_sales_fees = fields.Float()
    fees_commission = fields.Float()
    terminal_sales = fields.Float()
    app_sales = fields.Float()
    stored_funds = fields.Float()
    room = fields.Float()
    cash = fields.Float()
    comp = fields.Float()
    credit = fields.Float()
    company_credit = fields.Float()
    payroll = fields.Float()
    member_reward = fields.Float()
    virtual_money = fields.Float()
    gross_sales = fields.Float()
    sales_tax = fields.Float()
    additional_tax_amount_1 = fields.Float()
    additional_tax_amount_2 = fields.Float()
    additional_tax_amount_3 = fields.Float()
    other_tax = fields.Float()
    crv_tax = fields.Float()
    total_tax = fields.Float()
    stored_fund_cc_fees = fields.Float()
    stored_fund_percentage = fields.Float()
    app_cc_fees = fields.Float()
    app_cc_percentage = fields.Float()
    terminal_cc_fees = fields.Float()
    terminal_cc_percentage = fields.Float()
    total_cc_fees = fields.Float()
    platform_fees = fields.Float()
    platform_percentage = fields.Float()
    fixed_platform = fields.Boolean()
    room_cc = fields.Float()
    room_cc_percentage = fields.Float()
    cash_adj = fields.Float()
    additional_fees1 = fields.Float()
    additional_fees2 = fields.Float()
    additional_fees3 = fields.Float()
    other_fees = fields.Float()
    product_cost = fields.Float()
    spoilage_cost = fields.Float()
    theft_cost = fields.Float()
    overage_cost = fields.Float()
    refund = fields.Float()
    margin = fields.Float()
    commission = fields.Float()
    commission_percentage = fields.Float()
    operator_share = fields.Float()
    customer_deposit = fields.Float()
    operator_deposit = fields.Float()
    beer_and_wine = fields.Boolean()
    customer_own_alcohol = fields.Boolean()


class CustomerFeesReport(models.TransientModel):
    _name = 'customer.fees.report'
    _description = "Commission Report"
    _rec_name = 'name'

    readonly = fields.Boolean(default=False)
    name = fields.Char(default=lambda self: "Commission Report ")
    start_date = fields.Date()
    end_date = fields.Date()
    commission_type_id = fields.Many2one('customer.fees.type')
    dom_customer_fees_ids = fields.Many2many('customer.fees',
                                             'dom_customer_fees_rel')
    customer_fees_ids = fields.Many2many('customer.fees', 'customer_fees_rel',
                                         string='Company Name')
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail')], default='detail')
    report_lines = fields.One2many('customer.fees.line', 'report_id',
                                   ondelete="cascade")
    report_length = fields.Integer()
    operator_ids = fields.Many2many('res.company')
    show_warning = fields.Boolean()
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id.id)
    show_margin = fields.Boolean()
    show_net_sales = fields.Boolean()
    show_gross_sales = fields.Boolean()
    show_platform_fees = fields.Boolean()
    onchange_show_margin = fields.Boolean()
    onchange_show_net_sales = fields.Boolean()
    onchange_show_gross_sales = fields.Boolean()
    onchange_show_platform_fees = fields.Boolean()
