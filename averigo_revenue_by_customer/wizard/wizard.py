"""Creating new wizard and lines for revenue by customer report"""
import io
import json
import logging
from datetime import datetime, timedelta

import xlsxwriter
from PIL import Image
import base64
from odoo import models, fields, api, _
from odoo.tools import date_utils, UserError

_logger = logging.getLogger(__name__)


class TransactionReportLine(models.TransientModel):
    """"""
    _name = 'revenue.by.customer.line'

    report_id = fields.Many2one('revenue.by.customer')
    partner_id = fields.Many2one('res.partner')
    code = fields.Char(string="Customer #")
    name = fields.Char(sring="Customer")
    nick_name = fields.Char(sring="Nick Name")
    quantity = fields.Integer(string="Current Year Quantity")
    prev_quantity = fields.Integer(string="Previous Year Quantity")
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id)
    amount = fields.Float(string="Current Year Amount",
                          currency_field='currency_id')
    prev_amount = fields.Float(string="Previous Year Amount",
                               currency_field='currency_id')
    revenue_type = fields.Char()
    jan = fields.Float(string="January", currency_field='currency_id')
    feb = fields.Float(string="February", currency_field='currency_id')
    mar = fields.Float(string="March", currency_field='currency_id')
    apr = fields.Float(string="April", currency_field='currency_id')
    may = fields.Float(string="May", currency_field='currency_id')
    jun = fields.Float(string="June", currency_field='currency_id')
    jul = fields.Float(string="July", currency_field='currency_id')
    aug = fields.Float(string="August", currency_field='currency_id')
    sep = fields.Float(string="September", currency_field='currency_id')
    oct = fields.Float(string="October", currency_field='currency_id')
    nov = fields.Float(string="November", currency_field='currency_id')
    dec = fields.Float(string="December", currency_field='currency_id')
    prev_jan = fields.Float(string="Previous January",
                            currency_field='currency_id')
    prev_feb = fields.Float(string="Previous February",
                            currency_field='currency_id')
    prev_mar = fields.Float(string="Previous March",
                            currency_field='currency_id')
    prev_apr = fields.Float(string="Previous April",
                            currency_field='currency_id')
    prev_may = fields.Float(string="Previous May",
                            currency_field='currency_id')
    prev_jun = fields.Float(string="Previous June",
                            currency_field='currency_id')
    prev_jul = fields.Float(string="Previous July",
                            currency_field='currency_id')
    prev_aug = fields.Float(string="Previous August",
                            currency_field='currency_id')
    prev_sep = fields.Float(string="Previous September",
                            currency_field='currency_id')
    prev_oct = fields.Float(string="Previous October",
                            currency_field='currency_id')
    prev_nov = fields.Float(string="Previous November",
                            currency_field='currency_id')
    prev_dec = fields.Float(string="Previous December",
                            currency_field='currency_id')


class TransactionReport(models.TransientModel):
    _name = 'revenue.by.customer'
    _description = "Revenue By Customer"
    # _rec_name = 'name'

    name = fields.Char(default="Revenue By Customer")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    date_from = fields.Date()
    previous_date_from = fields.Date()
    date_to = fields.Date()
    previous_date_to = fields.Date()
    customer_ids = fields.Many2many('res.partner',
                                    domain=[('is_customer', '=', True),
                                            ('parent_id', '=', False)])
    division_ids = fields.Many2many('res.division')
    period = fields.Selection([('monthly', 'Monthly'), ('yearly', 'Yearly')],
                              string="Monthly/Yearly")
    report_lines = fields.One2many('revenue.by.customer.line', 'report_id')
    report_length = fields.Integer()
    show_month_wise = fields.Boolean()
    previous_year_comparison = fields.Boolean()
    months = fields.Many2many("res.months")
    show_jan = fields.Boolean()
    show_feb = fields.Boolean()
    show_mar = fields.Boolean()
    show_apr = fields.Boolean()
    show_may = fields.Boolean()
    show_jun = fields.Boolean()
    show_jul = fields.Boolean()
    show_aug = fields.Boolean()
    show_sep = fields.Boolean()
    show_oct = fields.Boolean()
    show_nov = fields.Boolean()
    show_dec = fields.Boolean()
    show_jan_prev = fields.Boolean()
    show_feb_prev = fields.Boolean()
    show_mar_prev = fields.Boolean()
    show_apr_prev = fields.Boolean()
    show_may_prev = fields.Boolean()
    show_jun_prev = fields.Boolean()
    show_jul_prev = fields.Boolean()
    show_aug_prev = fields.Boolean()
    show_sep_prev = fields.Boolean()
    show_oct_prev = fields.Boolean()
    show_nov_prev = fields.Boolean()
    show_dec_prev = fields.Boolean()

