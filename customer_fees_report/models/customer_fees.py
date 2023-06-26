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
from odoo import fields, models


class CustomerFees(models.Model):
    _name = 'customer.fees'
    _inherit = 'mail.thread'
    _description = "Customer Fees"
    _rec_name = "name"

    name = fields.Char('Company Name', tracking=True)
    active = fields.Boolean(string="Active", default=True)
    image_1920 = fields.Image()
    type_id = fields.Many2one('customer.fees.type', tracking=True,
                              ondelete='restrict')
    id_number = fields.Char('EIN/SSN', tracking=True, copy=False)
    id_number_masked = fields.Char('EIN/SSN', related='id_number',
                                   readonly=False, tracking=True, copy=False)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=5, tracking=True)
    city = fields.Char('City')
    county = fields.Char('County')
    state_id = fields.Many2one('res.country.state', string="State",
                               domain="[('country_id', '=', country_id)]")
    country_id = fields.Many2one('res.country', string="Country")
    address = fields.Char()
    primary_contact = fields.Char('Primary Contact', tracking=True)
    primary_email = fields.Char('Primary Email', tracking=True)
    primary_phone = fields.Char('Primary Phone', tracking=True)
    primary_mobile = fields.Char('Primary Mobile', tracking=True)
    accounts_payable_contact = fields.Char('Accounts Payable Contact',
                                           tracking=True)
    accounts_payable_email = fields.Char('Accounts Payable Email',
                                         tracking=True)
    accounts_payable_phone = fields.Char('Accounts PayablePhone',
                                         tracking=True)
    accounts_payable_mobile = fields.Char('Accounts PayableMobile',
                                          tracking=True)
    attachment_ids_1099 = fields.Many2many('ir.attachment',
                                           'form_1099_attachment',
                                           string='1099 Form')
    date_1099_attached = fields.Date()
    attachment_ids_banking_info = fields.Many2many('ir.attachment',
                                                   'banking_info_attachment',
                                                   string='Banking Information')
    attachment_ids_contract = fields.Many2many('ir.attachment',
                                               'contract_attachment',
                                               string='Contract')
    attachment_ids_others = fields.Many2many('ir.attachment',
                                             'others_attachment',
                                             string='Others')
    comment = fields.Text(string="Internal notes")
    special_notes = fields.Text(string="Special Notes")


class CustomerFeesType(models.Model):
    _name = 'customer.fees.type'
    _description = "Customer Fees Type"

    name = fields.Char(required=1)
    readonly = fields.Boolean()
    restrict_delete = fields.Boolean()
