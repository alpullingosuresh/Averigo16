"""Creating new wizard and lines for transaction list report"""
import io
import json
import logging
from datetime import datetime, timedelta

import xlsxwriter

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.tools import date_utils, UserError

_logger = logging.getLogger(__name__)


class TransactionReportLine(models.TransientModel):
    """"""
    _name = 'global.transaction.list.line'

    beacon_id = fields.Char()
    app_user = fields.Many2one('res.app.users')
    created_date = fields.Char()
    micro_market = fields.Many2one('stock.warehouse')
    first_name = fields.Char()
    averigo_login = fields.Char()
    invoice_no = fields.Char()
    payment_method = fields.Char()
    total_trans_amount = fields.Float()
    total_crv_amount = fields.Float()
    total_sales_amount = fields.Float()
    report_id = fields.Many2one('global.transaction.list.report')
    product_id = fields.Many2one('product.product')
    qty = fields.Integer()
    product_uom_id = fields.Many2one('uom.uom')
    price = fields.Float()
    net_price = fields.Float()
    tax_amount = fields.Float()
    crv_tax = fields.Float()
    additional_tax_amount_1 = fields.Float()
    additional_tax_amount_2 = fields.Float()
    additional_tax_amount_3 = fields.Float()
    other_tax = fields.Float()
    total_sales = fields.Float()
    list_price = fields.Float()
    sold_price = fields.Float()
    total_price = fields.Float()
    item_no = fields.Char()
    item_desc = fields.Char()
    created_time = fields.Char()
    cart_total = fields.Float()
    product_category = fields.Char()
    subsidy = fields.Float(digits='Product Price')
    mm_name = fields.Char(string="Micromarket")
    customer = fields.Many2one('res.partner')
    room_no = fields.Char()
    account_nickname = fields.Char(string="Account Nickname")


class TransactionReport(models.TransientModel):
    _name = 'global.transaction.list.report'
    _description = "MM Transaction List Report"
    _rec_name = 'name'

    readonly = fields.Boolean(default=False)
    name = fields.Char(default=lambda self: "G-Transaction List ")
    mm_dom_ids = fields.Many2many('stock.warehouse')
    micro_markets = fields.Many2one('stock.warehouse', 'Micro Markets',
                                    domain=[('location_type', '=',
                                             'micro_market')])
    start_date = fields.Date()
    end_date = fields.Date()
    category = fields.Many2one('product.category')
    payment_method = fields.Selection(
        [('Apriva', 'Apriva'), ('Apriva-PT', 'Apriva-PT'),
         ('Stored Funds', 'Stored Funds'),
         ('Company Credit', 'Company Credit'), ('Card', 'Card'),
         ('Cash', 'Cash'), ('Room', 'Room'),
         ('Credit', 'Credit'),
         ('Payroll deduction', 'Payroll Deduction'), ('Comp', 'Comp'),
         ('Member Reward', 'Member Reward')])
    report_lines = fields.One2many('global.transaction.list.line', 'report_id',
                                   ondelete="cascade")
    report_length = fields.Integer()
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
    show_warning = fields.Boolean()
    total_amount = fields.Monetary()
    total_tax = fields.Monetary()
    total_container = fields.Monetary()
    total_other_tax = fields.Monetary()
    total_apriva = fields.Monetary()
    total_apriva_pt = fields.Monetary()
    total_card = fields.Monetary()
    total_cash = fields.Monetary()
    total_room = fields.Monetary()
    total_credit = fields.Monetary()
    total_payroll = fields.Monetary()
    total_company_credit = fields.Monetary()
    total_comp = fields.Monetary()
    total_membership = fields.Monetary()
    total_stored = fields.Monetary()
    total_qty = fields.Integer()
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id.id)
    customer_id = fields.Many2one('res.partner',
                                  domain="[('id', 'in', partner_ids)]")
    partner_ids = fields.Many2many('res.partner')
    time_from = fields.Float()
    time_to = fields.Float()
    show_time_warn = fields.Boolean()
