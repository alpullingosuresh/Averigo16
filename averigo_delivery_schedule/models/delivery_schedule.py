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

from odoo import fields, models, api


class DeliverySchedule(models.Model):
    _name = 'delivery.schedule'

    name = fields.Char()
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    schedule_type = fields.Selection(
        [('day', 'Days'), ('week', 'Weeks'), ('month', 'Months')],
        string='Schedule Type',
        default='day')
    frequency = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
         ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
         ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
         ('15', '15')], string="Frequncy",
        default='1')
    route_id = fields.Many2one('route.route', string="Route")
    calender_event_id = fields.Many2one('calendar.event',
                                        string="Calendar Event")
    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id)


class CalendarEventScheduling(models.Model):
    _inherit = 'calendar.event'

    is_delivery_schedule = fields.Boolean(
        help="This is a delivery schedule event")
    delivery_schedule_id = fields.Many2one('delivery.schedule')


class CalendarAttendeeEmployee(models.Model):
    _inherit = 'calendar.attendee'

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
