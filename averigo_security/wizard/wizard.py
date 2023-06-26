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
from odoo import models, fields, api, _
from lxml import etree
from lxml.html import builder as html


class Invite(models.TransientModel):
    _inherit = 'mail.wizard.invite'

    user_ids = fields.Many2many('res.users', string='Users')
    dom_user_ids = fields.Many2many('res.users')
    send_mail = fields.Boolean('Send Email', default=False,
                               help="If checked, the partners will receive an "
                                    "email warning they have been added in the"
                                    " document's followers.")


class MailFollowersWizard(models.TransientModel):
    _name = 'mail.followers.wizard'

    res_model = fields.Char('Related Document Model', required=True,
                            index=True, help='Model of the followed resource')
    lead_id = fields.Many2many('crm.lead', index=True,
                               help='Id of the followed resource')
    sale_id = fields.Many2many('sale.order', index=True,
                               help='Id of the followed resource')
    purchase_id = fields.Many2many('purchase.order', index=True,
                                   help='Id of the followed resource')
    payment_id = fields.Many2many('account.payment', index=True,
                                  help='Id of the followed resource')
    stock_picking_id = fields.Many2many('stock.picking', index=True,
                                        help='Id of the followed resource')
    invoice_id = fields.Many2many('account.move', index=True,
                                  help='Id of the followed resource')
    partner_id = fields.Many2many('res.partner', 'follower_partner_ids',
                                  index=True,
                                  help='Id of the followed resource')
    micromarket_id = fields.Many2many('stock.warehouse', index=True,
                                      help='Id of the followed resource')
    user_ids = fields.Many2many('res.users', string='Users')
    partner_ids = fields.Many2many('res.partner', 'sender_partner_ids',
                                   string='Recipients',
                                   help="List of partners that will be added"
                                        " as follower of the current "
                                        "document.")
    channel_ids = fields.Many2many('mail.channel', string='Channels',
                                   help='List of channels that will be added'
                                        ' as listeners of the current '
                                        'document.',
                                   domain=[('channel_type', '=', 'channel')])
    message = fields.Html('Message')
    send_mail = fields.Boolean('Send Email', default=False,
                               help="If checked, the partners will receive an"
                                    " email warning they have been added in"
                                    " the document's followers.")
