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


class PortalPartner(models.Model):
    _inherit = 'res.partner'

    show_price = fields.Boolean()
    show_invoice = fields.Boolean()
    create_order = fields.Boolean()
    order_form = fields.Boolean()
    re_order = fields.Boolean()
    customer_dashboard = fields.Boolean()
    report_menu = fields.Boolean()
    type = fields.Selection(selection_add=[('portal', 'Portal'), ('other',)])
    type_address = fields.Selection(
        [('contact', 'Contact'), ('invoice', 'Billing Address'),
         ('delivery', 'Delivery Address'), ('other', 'Other Address'),
         ("private", "Private Address")],
        inverse='_inverse_type_portal',
        string='Address Type')
    type_portal = fields.Selection([('portal', 'Portal')], required=True)
    child_ids_portal = fields.One2many('res.partner', 'parent_id_portal',
                                       string='Contact', domain=[
            ('active', '=', True)],
                                       ondelete='cascade')
    parent_id_portal = fields.Many2one('res.partner', string='Related Company',
                                       index=True)
    portal_check = fields.Boolean(default=False)
    show_image = fields.Boolean(default=False)
    active_check = fields.Boolean('Active User',
                                  inverse='_inverse_active_check')
    username = fields.Char('Username')
    is_default = fields.Boolean(string="Default Address", default=False)
    duplicate_default = fields.Boolean(string="Default Address Set")
    portal_report_ids = fields.Many2many('ir.actions.report',
                                         string='Allowed Reports',
                                         domain=[
                                             ('show_in_portal', '=', True)])
    is_portal_user = fields.Boolean(help="Used to check the contact has "
                                         "portal user")
    user_check = fields.Boolean()
    schedule_tax_id = fields.Many2one('schedule.tax')
    create_case = fields.Boolean()
    child_ids_request = fields.One2many('res.partner', 'parent_id',
                                        string='Contact', domain=[
            ('type', '=', 'request')], ondelete='cascade')
    child_ids_contacts = fields.One2many('res.partner', 'parent_id',
                                         string='Contact & Addresses', domain=[
            ('type', 'in',
             ['contact', 'invoice', 'delivery', 'other', 'private'])],
                                         ondelete='cascade')
    delivery_request = fields.Boolean('Delivery',
                                      help="Used to filter the delivery "
                                           "address request from portal")
    invoice_request = fields.Boolean('Invoice',
                                     help="Used to filter the invoice "
                                          "address request from portal")
