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

from odoo import models


class WhereSoldReport(models.AbstractModel):
    _name = 'report.where_sold_report.report_where_sold'

    # def _get_report_values(self, docids, data=None):
    #     line_ids = self.env['where.sold.line'].search([('id', 'in', data['sale_ids'])])
    #     total_quantity = sum(line_ids.mapped('quantity'))
    #     total_sold = sum(line_ids.mapped('sold'))
    #     records = {
    #         'line_ids': line_ids,
    #         'start_date': data['start_date'],
    #         'end_date': data['end_date'],
    #         'total_quantity': total_quantity,
    #         'total_sold': total_sold,
    #         'currency_id': self.env.company.currency_id,
    #     }
    #     return records
