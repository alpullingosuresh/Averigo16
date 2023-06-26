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
from odoo.addons.base.models.res_partner import _tz_get

from odoo import models, fields

import logging

_logger = logging.getLogger(__name__)

MONTH_SELECTION = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]


class AverigoTransactionRecurring(models.Model):
    _name = 'transaction.recurring'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Transaction Recurring"

    active = fields.Boolean(string="Active", default=True)
    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id)
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 related='sale_id.partner_id')
    name = fields.Char('Name', required=True)
    recurring_type = fields.Selection(
        [('scheduled', 'Scheduled'), ('reminder', 'Reminder'),
         ('unscheduled', 'Unscheduled')], 'Recurring Type',
        default='scheduled')
    interval_type = fields.Selection(
        [('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'),
         ('yearly', 'Yearly')],
        'Interval Type', default='daily')
    mm_action = fields.Boolean()
    micro_market_id = fields.Many2one('stock.warehouse')
    mm_product_ids = fields.Many2many('product.micro.market',
                                      domain="[('micro_market_id', '=', micro_market_id), ('is_discontinued', '=', False)]")
    sale_id = fields.Many2one('sale.order')
    purchase_id = fields.Many2one('purchase.order')
    bill_id = fields.Many2one('account.move')
    po_no = fields.Char('PO No', related='bill_id.invoice_origin')
    color = fields.Integer(string='Color Index', default=0)
    days = fields.Integer('Days')
    weeks = fields.Selection(
        [('7', 'Sun'), ('1', 'Mon'), ('2', 'Tue'), ('3', 'Wed'), ('4', 'Thu'),
         ('5', 'Fri'), ('6', 'sat')], 'Weeks', default='7')
    month = fields.Selection(MONTH_SELECTION, default='1')
    monthly_selection = fields.Selection(
        [('day', ' '), ('dayofweek', '')], 'Monthly Selection', default='day',
        required=True)
    month_day = fields.Many2one('day.day', string="Day",
                                default=lambda self: self.env.ref(
                                    'averigo_recurring.day1'))
    week_no = fields.Selection(
        [('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'),
         ('5', 'Last')],
        'Week Selection', default='1')
    day_name = fields.Selection(
        [('7', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'),
         ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'),
         ('6', 'Saturday')], 'Day Name', default='7')
    month_day_int = fields.Integer('Day')
    user_id = fields.Many2one('res.users', string="Login User",
                              default=lambda self: self.env.user.id)
    start_date = fields.Date('Start Date', default=fields.Date.today)
    end_date = fields.Date('End Date')
    notify_option = fields.Selection(
        [('create_only', 'Create transactions and do not tell me'),
         ('create_notify', 'Create transactions and give me alert message')],
        'Notification Option', default='create_only')
    notify_days = fields.Integer('Reminder days')
    next_execution_date = fields.Date('Next Execution Date',
                                      default=fields.Date.today)
    monday = fields.Boolean('Monday', default=True)
    tuesday = fields.Boolean('Tuesday', default=True)
    wednesday = fields.Boolean('Wednesday', default=True)
    thursday = fields.Boolean('Thursday', default=True)
    friday = fields.Boolean('Friday', default=True)
    saturday = fields.Boolean('Saturday', default=True)
    sunday = fields.Boolean('Sunday', default=True)
    report_id = fields.Many2one('ir.actions.report')
    report_format = fields.Selection(
        [('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')], string='Format',
        default='pdf')
    template_id = fields.Many2one('mail.template', string='Email Template',
                                  domain="[('model', '=', 'transaction.recurring')]")
    model_id = fields.Many2one('ir.model', 'Model')
    filters = fields.Text('Filters')
    recipient_ids = fields.Many2many('res.partner', string="Recipients")
    no_end_date = fields.Boolean(default=True)
    time_picker = fields.Float()
    recurring_tz = fields.Selection(_tz_get, string='Timezone',
                                    default=lambda self: self._context.get(
                                        'tz'))
    report_partner_ids = fields.Many2many('res.partner')
    next_execution_datetime = fields.Datetime(store=True)
    report_action = fields.Boolean()
    report_date = fields.Selection(
        [('previous', 'Previous Day'), ('week', 'This Week'),
         ('month', 'This Month')],
        default='previous', required=True)
    state = fields.Selection([('running', 'Running'), ('closed', 'Closed')],
                             default='running')

    last_execution = fields.Datetime("Last Execution Date")


class RecurringDays(models.Model):
    _name = 'day.day'
    _description = "Recurring Days"

    name = fields.Char('Day')
    day = fields.Char()
