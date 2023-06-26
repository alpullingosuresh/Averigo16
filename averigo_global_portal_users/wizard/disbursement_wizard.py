"""Creating new wizard and lines for Disbursement report"""
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class DisbursementReportLine(models.TransientModel):
    """"""
    _name = 'global.disbursement.report.line'

    report_id = fields.Many2one('global.disbursement.report')
    branch_id = fields.Many2one('res.division', 'Operator Branch',
                                related='micro_market.division_id', store=1)
    micro_market = fields.Many2one('stock.warehouse')
    micro_market_name = fields.Char(string='Micromarket Name',
                                    related='micro_market.name', store=1)
    operator_id = fields.Many2one('res.company', 'Operator',
                                  related='micro_market.company_id', store=1)
    payment_method = fields.Char()
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
    net_sales = fields.Float()
    stored_fund_cc_fees = fields.Float()
    stored_fund_percentage = fields.Float()
    app_cc_fees = fields.Float()
    app_cc_percentage = fields.Float()
    terminal_cc_fees = fields.Float()
    terminal_cc_percentage = fields.Float()
    room_cc = fields.Float()
    room_cc_percentage = fields.Float()
    total_cc_fees = fields.Float()
    brand_fees = fields.Float()
    brand_percentage = fields.Float()
    brand_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    management_fees = fields.Float()
    management_percentage = fields.Float()
    management_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    platform_fees = fields.Float()
    platform_percentage = fields.Float()
    fixed_platform = fields.Boolean()
    other_fees = fields.Float()
    product_cost = fields.Float()
    spoilage_cost = fields.Float()
    theft_cost = fields.Float()
    overage_cost = fields.Float()
    refund = fields.Float()
    margin = fields.Float()
    commission = fields.Float()
    commission_percentage = fields.Float()
    group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    additional_fees1 = fields.Float()
    additional_fees1_percentage = fields.Float()
    additional_group1_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')])
    operator_share = fields.Float()
    customer_deposit = fields.Float()
    operator_deposit = fields.Float()
    enable_front_desk = fields.Boolean()
    beer_and_wine = fields.Boolean()
    customer_own_alcohol = fields.Boolean()
    category = fields.Selection(
        [('location_total', 'Location Total'), ('beer_wine', 'Beer&Wine'),
         ('beer_wine_customer', ' Customer Own Beer&Wine')])


class DisbursementReport(models.TransientModel):
    _name = 'global.disbursement.report'
    _description = "Disbursement Report"
    _rec_name = 'name'

    readonly = fields.Boolean(default=False)
    name = fields.Char(default=lambda self: "Disbursement Report ")
    branch_id = fields.Many2one('res.division', 'Operator Branch')
    mm_dom_ids = fields.Many2many('stock.warehouse')
    micro_markets = fields.Many2many('stock.warehouse', domain=[
        ('location_type', '=', 'micro_market')])
    start_date = fields.Date()
    end_date = fields.Date()
    report_lines = fields.One2many('global.disbursement.report.line',
                                   'report_id', ondelete="cascade")
    report_length = fields.Integer()
    operator_id = fields.Many2many('res.company',
                                   default=lambda self: self.env.company)
    show_operator_column = fields.Boolean()
    show_warning = fields.Boolean()
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id.id)
    customer_id = fields.Many2many('res.partner',
                                   domain="[('id', 'in', partner_ids)]")
    partner_ids = fields.Many2many('res.partner')
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail')], default='detail')
    excel_type = fields.Selection(
        [('vertical', 'Vertical'), ('horizontal', 'Horizontal')],
        default='horizontal')
