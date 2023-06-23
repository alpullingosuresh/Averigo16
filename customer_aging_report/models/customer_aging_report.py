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
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero
from PIL import Image
from odoo.tools import date_utils
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from lxml import etree
from odoo.addons.base.models.ir_ui_view import (
    transfer_field_to_modifiers, transfer_node_to_modifiers,
    transfer_modifiers_to_node,
)


def setup_modifiers(node, field=None, context=None, in_tree_view=False):
    modifiers = {}
    if field is not None:
        transfer_field_to_modifiers(field, modifiers)
    transfer_node_to_modifiers(
        node, modifiers, context=context, in_tree_view=in_tree_view)
    transfer_modifiers_to_node(modifiers, node)


try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class CustomerAgingReport(models.TransientModel):
    _name = 'customer.aging.report'
    _description = 'Aging By Customer'
    """Aging By Customer"""

    _transient_max_hours = 0.0

    name = fields.Char()
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    division_id = fields.Many2one('res.division', string='Division')
    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    partner_ids = fields.Many2many('res.partner', string='Customer')
    customer_aging_line_ids = fields.Many2many('customer.aging.line')
    start_date = fields.Date(required=True, default=fields.Date.today())
    report_length = fields.Integer()
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail'),
         ('transaction', 'Transaction')],
        string='Report Type', required=True, default='summary')
    aged_by = fields.Selection(
        [('inv_date', 'Invoice Date'), ('due_date', 'Due Date')],
        string='Aged By',
        required=True, default='due_date')


class CustomerAgingReportLine(models.TransientModel):
    _name = 'customer.aging.line'
    _description = 'Customer Aging Report Line'
    """Customer Aging Report Line"""

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    display_type = fields.Selection([('line_section', "Section")],
                                    default=False)
    name = fields.Text(' ', translate=True)
    partner_code = fields.Char('Customer No')
    partner_id = fields.Many2one('res.partner', string='Customer')
    division_id = fields.Many2one('res.division', string='Division')
    department_id = fields.Many2one('hr.department', string='Department')
    invoice_type = fields.Selection(
        [('invoice', 'Invoice'), ('advance', 'Advance'),
         ('credit_note', 'Credit Memo')],
        string='Type', default='invoice')
    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    invoice_no = fields.Many2one('account.move', string='Transaction No')
    invoice_date = fields.Date('Transaction Date')
    invoice_status = fields.Char('Invoice Status')
    route_id = fields.Many2one('route.route', string='Route')
    due_date = fields.Date('Due Date')
    aging = fields.Char('Aging')
    balance = fields.Char('Balance')
    street = fields.Char('Customer Address')
    current = fields.Float('Current')
    period_length = fields.Float('1-30')
    period_length_2 = fields.Float('31-60')
    period_length_3 = fields.Float('61-90')
    period_length_4 = fields.Float('Above 90')
    total = fields.Float('Total')
    period_check = fields.Char('Period Check')
    amount = fields.Float('Amount')
    cust_balance = fields.Float()
