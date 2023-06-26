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


class CustomerItemList(models.TransientModel):
    _name = 'customer.item.list'
    _description = "Customer Item List Report"
    _rec_name = "name"

    name = fields.Char(default="Customer Item list Report")
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 domain="[('is_customer', '=', True),('parent_id', '=', False)]")
    customer_ids = fields.Many2many('res.partner')

    search_string = fields.Char(string='Item Search')

    record_count = fields.Integer("Records Found")
    mm_ids = fields.Many2many('stock.warehouse', string='Micromarkets')
    location_type = fields.Selection([('Micromarket / Pantry', 'All'),
                                      ('warehouse', 'Order Products'),
                                      ('Micromarket', 'Micromarket'),
                                      ('Pantry', 'Pantry'), ],
                                     string='Location Type',
                                     default='Micromarket', index=True,
                                     tracking=True)
    line_ids = fields.One2many('customer.item.list.lines', 'report_id',
                               string="Invoice")
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    show_cp_code = fields.Boolean()


class CustomerItemListLines(models.TransientModel):
    _name = 'customer.item.list.lines'
    _description = "Customer Item List Lines"

    partner_id = fields.Many2one("res.partner", string="Customer")
    product_id = fields.Many2one("product.product",
                                 string="Product description")
    mm_id = fields.Many2one("stock.warehouse", string="Micromarket")
    uom_id = fields.Many2one("uom.uom", string="UoM")
    categ_id = fields.Many2one("product.category", string="Category")
    margin_price = fields.Float(string='Margin Price %', store=True)
    item_price = fields.Float(string='Current Price', store=True)
    item_cost = fields.Float(string='Product Cost', store=True)
    product_code = fields.Char('Product Code', store=True)

    report_id = fields.Many2one('customer.item.list')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    cp_code = fields.Char(string="CP Code", size=60)


class PantryProduct(models.Model):
    _inherit = 'product.pantry'
    _description = 'Panty Products'

    """Product Linked to Pantry"""
    cost_price = fields.Float(related='product_id.standard_price', store=True)
