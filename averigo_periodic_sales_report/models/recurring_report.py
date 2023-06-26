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
import io
import base64
import csv
import xlsxwriter
import logging
import calendar
import json
import datetime
import pytz
from datetime import timedelta, time, date
from odoo.fields import Date
from PIL import Image
from math import ceil
from dateutil.relativedelta import *
from odoo.addons.base.models.res_partner import _tz_get

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from odoo.tools import date_utils


class AverigoPeriodicRecurringLine(models.TransientModel):
    """"""
    _name = 'periodic.recurring.line'

    report_id = fields.Many2one('periodic.recurring')
    start_date = fields.Date()
    end_date = fields.Date()
    name = fields.Char(default='Sales Report Lines')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")
    weeks = fields.Char('Weeks')
    qty_pre_week = fields.Integer(string='Total Units Sold In Previous Week',
                                  default=0)
    qty_cur_week = fields.Integer(string='Total Units Sold In Current Week',
                                  default=0)
    qty_differance = fields.Float()
    sales_pre_week = fields.Float(string='Total Sales In Previous Week',
                                     default=0)
    sales_cur_week = fields.Float(string='Total Sales In Current Week',
                                     default=0)
    sales_differance = fields.Float()
    product_with_no_sale = fields.Integer(string='Product With No Sale',
                                          default=0)
    product_sold_out = fields.Integer(string='Product Sold Out In This Period',
                                      default=0)
    type = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly')])
    qty_up_bool = fields.Boolean()
    qty_down_bool = fields.Boolean()
    qty_neutral_bool = fields.Boolean()
    qty_status = fields.Char('Status')
    sales_up_bool = fields.Boolean()
    sales_down_bool = fields.Boolean()
    sales_neutral_bool = fields.Boolean()
    sales_status = fields.Char('Status')


class AverigoPeriodicRecurring(models.Model):
    _name = 'periodic.recurring'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Periodic Recurring"

    def _get_default_time(self):
        time_now_hour = datetime.datetime.now(pytz.timezone("US/Pacific")).time().hour
        return time_now_hour

    name = fields.Char(default='Periodic Sales Report')
    report_line_ids = fields.One2many('periodic.recurring.line', 'report_id',
                                      ondelete="cascade")
    micro_market_id = fields.Many2one('stock.warehouse')
    report_id = fields.Many2one('ir.actions.report')
    template_id = fields.Many2one('mail.template', string='Email Template',
                                  domain="[('model', '=', 'periodic.recurring')]")
    recipient_ids = fields.Many2many('res.partner', string="Recipients")
    time_picker = fields.Float(default=_get_default_time)
    recurring_tz = fields.Selection(_tz_get, string='Timezone',
                                    default=lambda self: self._context.get(
                                        'tz'))
    start_date = fields.Date()
    end_date = fields.Date()
    previous_start_date = fields.Date(readonly=True)
    previous_end_date = fields.Date(readonly=True)
    type = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly')])

    def scheduled_periodic_report(self):
        day = date.today()
        if day.weekday() == 1:
            micro_market_ids = self.env['stock.warehouse'].search(
                [('location_type', '=', 'micro_market')])
            i = 0
            for micro_market_id in micro_market_ids:
                print(i + 1, micro_market_id)
                data = self.env['periodic.recurring'].create({
                    'micro_market_id': micro_market_id.id,
                    'type': 'weekly',
                    'template_id': self.env['mail.template'].search([('name', '=', 'Periodic Sales Report')]).id,
                })
                data.get_weekly_report_value()

        day = datetime.datetime.now()
        if day.day == 1:
            self.get_monthly_report_value()

    def get_weekly_report_value(self):
        day = date.today()
        if day.weekday() == 0:
            cur_start_date = day - timedelta(7)
            cur_end_date = day - timedelta(1)
        else:
            dif = day.weekday()
            cur_start_date = day - timedelta(7 + dif)
            cur_end_date = day - timedelta(1 + dif)
        self.start_date = cur_start_date
        self.end_date = cur_end_date
        print(self.start_date, self.end_date, self.previous_start_date,
              self.previous_end_date, self.micro_market_id)
        qty_pre_week, qty_cur_week, sales_pre_week, sales_cur_week, qty_differance, sales_differance, product_with_no_sale, product_sold_out, qty_status, sales_status = self.get_query_value(
            firstdate=self.start_date, lastdate=self.end_date, mm_record=self.micro_market_id)
        report_vals = {
            'micro_market_id': self.micro_market_id.id,
            'qty_pre_week': qty_pre_week,
            'qty_cur_week': qty_cur_week,
            'qty_differance': qty_differance,
            'qty_status' : qty_status,
            'sales_pre_week': sales_pre_week,
            'sales_cur_week': sales_cur_week,
            'sales_differance': sales_differance,
            'sales_status' : sales_status,
            'product_with_no_sale': product_with_no_sale,
            'product_sold_out': product_sold_out,
            'report_id': self.id,
            'type': self.type,
        }
        self.report_line_ids = [(0, 0, report_vals)]
        self.export_excel()

    def get_monthly_report_value(self):
        day = datetime.datetime.now()
        if day.day == 1:
            last_month = fields.Date.subtract(fields.Date.today(), months=1)
            self.start_date = date_utils.start_of(last_month, 'month')
            self.end_date = date_utils.end_of(last_month, 'month')
            date = fields.Date.subtract(last_month, months=1)
            self.previous_start_date = date_utils.start_of(date, 'month')
            self.previous_end_date = date_utils.end_of(date, 'month')
            print(self.start_date, self.end_date, self.previous_start_date, self.previous_end_date)
            qty_pre_week, qty_cur_week, sales_pre_week, sales_cur_week, qty_differance, sales_differance, product_with_no_sale, product_sold_out, qty_status, sales_status = self.get_query_value(
                firstdate=self.start_date, lastdate=self.end_date,
                mm_record=self.micro_market_id)
            report_vals = {
                'micro_market_id': self.micro_market_id.id,
                'qty_pre_week': qty_pre_week,
                'qty_cur_week': qty_cur_week,
                'qty_differance': qty_differance,
                'qty_status': qty_status,
                'sales_pre_week': sales_pre_week,
                'sales_cur_week': sales_cur_week,
                'sales_differance': sales_differance,
                'sales_status': sales_status,
                'product_with_no_sale': product_with_no_sale,
                'report_id': self.id,
                'type': self.type,
            }
            self.report_line_ids = [(0, 0, report_vals)]

    def get_query_value(self, firstdate, lastdate, mm_record):
        # firstdate = '2022-01-01'
        # lastdate = '2022-01-30'
        query_cur = """SELECT SUM(spl.qty) AS current_qty, SUM(spl.net_price) AS current_sales
                        FROM session_product_list spl
                        INNER JOIN
                        user_session_history ush ON ush.id=spl.session_id
                        WHERE micro_market_id = %s AND ush.create_date
                        BETWEEN '%s' AND '%s'""" % (mm_record.id, firstdate, lastdate)
        self.env.cr.execute(query_cur)
        vals_cur = self.env.cr.dictfetchall()
        query_pre = """SELECT SUM(spl.qty) AS previous_qty, SUM(spl.net_price) AS previous_sales
                        FROM session_product_list spl
                        INNER JOIN
                        user_session_history ush ON ush.id=spl.session_id
                        WHERE micro_market_id = %s AND ush.create_date
                        BETWEEN '%s' AND '%s'""" % (mm_record.id, firstdate, lastdate)
        self.env.cr.execute(query_pre)
        vals_pre = self.env.cr.dictfetchall()
        # query_no_sale = """SELECT COUNT(pmm.product_id) AS product_count FROM product_micro_market pmm
        #                 WHERE pmm.micro_market_id = %s AND ush.create_date
        #                 BETWEEN '%s' AND '%s' AND GROUP BY pmm.product_id""" % (mm_record.id, firstdate, lastdate)
        query_no_sale = """SELECT COUNT(pmm.product_id) AS product_count FROM session_product_list spl
                                INNER JOIN user_session_history ush ON ush.id=spl.session_id
                                INNER JOIN product_micro_market pmm ON pmm.micro_market_id = ush.micro_market_id
                                WHERE ush.micro_market_id = %s AND pmm.product_id != spl.product_id AND ush.create_date
                                BETWEEN '%s' AND '%s' GROUP BY pmm.product_id""" % (
        mm_record.id, firstdate, lastdate)
        self.env.cr.execute(query_no_sale)
        val_no_sale = self.env.cr.dictfetchall()
        sold_out_product = []
        if type == 'weekly':
            query_out_of_stk = """SELECT pmm.product_id FROM session_product_list spl
                            INNER JOIN user_session_history ush ON ush.id=spl.session_id
                            INNER JOIN product_micro_market pmm ON pmm.micro_market_id = ush.micro_market_id
                            WHERE ush.micro_market_id = %s AND pmm.product_id = spl.product_id
                            AND ush.create_date
                            BETWEEN '%s' AND '%s' GROUP BY pmm.product_id""" % (mm_record.id, firstdate, lastdate)
            self.env.cr.execute(query_out_of_stk)
            val_out_of_stk = self.env.cr.dictfetchall()
            for val in val_out_of_stk:
                product = self.env['product.product'].search([('id', '=', val['product_id'])])
                current_qty = product.with_context(location=mm_record.location_id,
                                                   to_date=lastdate).qty_available
                starting_qty = product.with_context(location=mm_record.location_id,
                                                   to_date=firstdate).qty_available
                # print(product.name, current_qty, starting_qty)
                if starting_qty > 0 and current_qty <= 1000:
                    sold_out_product.append(product.id)
        qty_pre_week = 0
        qty_cur_week = 0
        sales_pre_week = 0
        sales_cur_week = 0
        product_with_no_sale = len(val_no_sale)
        product_sold_out = len(sold_out_product)
        qty_differance = 0
        sales_differance = 0

        for val in vals_cur:
            if val['current_qty']:
                qty_cur_week = val['current_qty']
            if val['current_sales']:
                sales_cur_week = val['current_sales']
        for val in vals_pre:
            if val['previous_qty']:
                qty_pre_week = val['previous_qty']
            if val['previous_sales']:
                sales_pre_week = val['previous_sales']

        if qty_pre_week != 0:
            qty_differance = (qty_cur_week - qty_pre_week) * 100 / qty_pre_week
        if sales_differance != 0:
            sales_differance = (sales_cur_week - sales_pre_week) * 100 / sales_cur_week
        if qty_differance < 0:
            qty_status = '▼'
        elif qty_differance > 0:
            qty_status = '▲'
        else:
            qty_status = '-'
        if sales_differance < 0:
            sales_status = '▼'
        elif sales_differance > 0:
            sales_status = '▲'
        else :
            sales_status = '-'
        return qty_pre_week, qty_cur_week, sales_pre_week, sales_cur_week, qty_differance, sales_differance, product_with_no_sale, product_sold_out, qty_status, sales_status

    def _get_report_base_filename(self):
        """ generate report file name """
        r_name = "Weekly Sales Report "
        date_string = Date.today()
        return r_name + " " + str(date_string)

    def export_excel(self):
        """ export report to excel """
        if self.type == 'weekly':
            report_to_take = self.report_line_ids.ids
        else:
            report_to_take = self.report_line_ids.ids
        data = {
            'id': self.id,
            'line_ids': self.report_line_ids.ids,
            'micro_ids': self.micro_market_id.id,
            'date_time': fields.Date.today(),
            'type': self.type,
            'records': report_to_take,
        }
        return {
            'type': 'ir_actions_xlsx_download',
            'data': {'model': 'periodic.recurring',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': self._get_report_base_filename(),
                     }
        }

    def get_xlsx_report(self, data, response):
        print("JJJJJJJJJJJJJJJJJJJJJJJJJJ")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        user_obj = self.env.user
        company_obj = self.env.user.company_id
        c_symbol = company_obj.currency_id.symbol
        c_symbol = ""
        try:
            size = 600, 700
            buf_image = io.BytesIO(base64.b64decode(company_obj.report_logo))
            image = Image.open(io.BytesIO(base64.b64decode(company_obj.report_logo)))
            image.thumbnail(size, Image.ANTIALIAS)
            imgByteArr = io.BytesIO()
            image.save(imgByteArr, format = image.format)
            buf_image = io.BytesIO(imgByteArr.getvalue())
        except Exception:
            pass
        # prepare company address
        c_address_1 = (company_obj.street if company_obj.street else '') + ", " + (
            company_obj.street2 if company_obj.street2 else '')
        c_address_2 = (company_obj.city if company_obj.city else '') + ", " + (
            company_obj.state_id.code if company_obj.state_id else '') + ", " + (
                          company_obj.zip if company_obj.zip else '')
        # prepare report date
        if data['type'] == 'weekly':
            sheet = workbook.add_worksheet('Weekly Sales Report')
        if data['type'] == 'monthly':
            sheet = workbook.add_worksheet('Monthly Sales Report')
        format1 = workbook.add_format(
            {'font_size': 22, 'bold': True, 'bg_color': '#D3D3D3'})
        format4 = workbook.add_format({'font_size': 22})
        format2 = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'center'})
        format3 = workbook.add_format({'font_size': 10})
        format8 = workbook.add_format({'font_size': 10, 'align': 'right'})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        format9 = workbook.add_format(
            {'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format7 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        format7.set_align('center')
        format1.set_align('center')
        format9.set_align('center')

        row = col = 0
        format10 = workbook.add_format(
            {'font_size': 10, 'bold': True, 'align': 'right'})
        sheet.write(row, col + 10, company_obj.name, format10)
        # sheet.write(row, col + 11, company_obj.name, format5)
        sheet.write(row + 1, col + 10, c_address_1, format8)
        sheet.write(row + 2, col + 10, c_address_2, format8)

        row += 3
        if data['type'] == 'weekly':
            sheet.merge_range(row, col, row + 1, col + 10,
                              'Weekly Sales Report', format1)
        if data['type'] == 'monthly':
            sheet.merge_range(row, col, row + 1, col + 10,
                              'Monthly Sales Report', format1)
        # if data['start_date']:
        #     sheet.write(row + 2, col, "Start Date", format5)
        #     sheet.write(row + 3, col, data['start_date'] or ' ', format3)
        # if data['end_date']:
        #     sheet.write(row + 2, col + 2, "End Date", format5)
        #     sheet.write(row + 3, col + 2, data['end_date'] or ' ', format3)
        sheet.write(row + 2, col + 9, "Report Date :", format5)
        sheet.write(row + 2, col + 10, data['date_time'], format3)
        row += 5

        if data['type'] == 'weekly':
            headings = ['Location', 'Quantity - Previous Week', 'Quantity - Current Week', 'Up/Down Arrow', '% Change',
                        'Sales - Previous Week', 'Sales - Current Week', 'Up/Down Arrow', '% Change', 'Products with No Sales', ' Out Of Stock Products']
        else:
            headings = ['Location', 'Quantity - Previous Week', 'Quantity - Current Week', 'Up/Down Arrow', '% Change',
                        'Sales - Previous Week', 'Sales - Current Week', 'Up/Down Arrow', '% Change', 'Products with No Sales']

        for heading in headings:
            sheet.write(row, col, heading, format9)
            col = col + 1
        row += 1
        col = 0
        for line in data['records']:
            rec = self.env['periodic.sales.report.line'].search([('id', '=', line)])
            sheet.write(row, col, rec.micro_market_id.name, format3)
            sheet.write(row, col+1, rec.qty_pre_week, format3)
            sheet.write(row, col+2, rec.qty_cur_week, format3)
            sheet.write(row, col+3, rec.qty_status, format2)
            sheet.write(row, col+4, rec.qty_differance, format3)
            sheet.write(row, col+5, rec.sales_pre_week, format3)
            sheet.write(row, col+6, rec.sales_cur_week, format3)
            sheet.write(row, col+7, rec.sales_status, format2)
            sheet.write(row, col+8, rec.sales_differance, format3)
            sheet.write(row, col+9, rec.product_with_no_sale, format3)
            if rec.type == 'weekly':
                sheet.write(row, col+10, rec.product_sold_out, format3)
            row += 1

        workbook.close()
        output.seek(0)
        # response.stream.write(output.read())
        # output.close()
        data_record = base64.encodestring(output.getvalue())
        ir_values = {
            'name': "Periodic Sales Report.xlsx",
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        print("data", data_id)
        message = _(
            "Weekly Sales Report of " + str(
                self.micro_market_id.name) + ". Period " + str(
                self.start_date) + " to " + str(
                self.end_date))
        mail = self.env['mail.mail'].sudo().create({
            'subject': "WEEKLY SALES REPORT : " + str(self.micro_market_id.name),
            'email_from': "custest911@gmail.com",
            'email_to': "selestest911@gmail.com",
            'body_html': message,
            'attachment_ids': data_id,
        })
        mail.send()
        # template = self.template_id
        # template.attachment_ids = [(6, 0, [data_id.id])]
        # email_values = {'email_to': 'custest911@gmail.com',
        #                 'email_from': self.env.user.email}
        # mail_id = template.sudo().send_mail(self.id, email_values=email_values,
        #                                     force_send=True)
        # mail_id = self.env['mail.mail'].browse(mail_id)
        # template.attachment_ids = [(3, data_id.id)]
