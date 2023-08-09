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
import re
import logging

from odoo.exceptions import UserError, ValidationError

from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)


class CustomerOrderItems(models.Model):
    _inherit = 'res.partner'
    # _order = 'name, code'

    def _get_check_group(self):
        """ Get default  """
        if self.env.user.has_group('base_averigo.averigo_operator_user'):
            return True
        else:
            return False

    customer_product_ids = fields.One2many(
        'customer.product', 'customer_product_id', tracking=True, copy=True)
    product_ids = fields.Many2many('product.product', domain="[('type', 'in', ['product', "
                                                             "'consu'])]", string='Products')
    product_filter_ids = fields.Many2many(
        'product.product', 'catalog_filter_id', compute='_compute_product_filter_ids')
    delete_products = fields.Boolean(compute='_compute_product_filter_ids')
    multiple_uom_products = fields.One2many(
        'product.customer.uom', 'partner_id')
    product_select_uom_length = fields.Integer(
        string="Count", compute="compute_product_select_uom_length")
    catalog_product_ids = fields.One2many('catalog.customer', 'partner_id')
    catalog_length = fields.Integer(
        string="Count", compute="_get_cat_prod_count")
    select_catalog_products = fields.Boolean('Select All', default=True)
    check_group = fields.Boolean(
        compute='_compute_check_group', default=_get_check_group)
    catalog_ids = fields.Many2many('product.catalog', domain="[('catalog_type', '=', 'customer')]",
                                   string='Product Catalog')
    product_catalog_ids = fields.Many2many('product.product.catalog')
    product_count = fields.Integer(compute='_compute_product_count')
    buy_all_item = fields.Boolean(default=False)
    route_id = fields.Many2one('route.route', string='Route')
    drop_location_id = fields.Many2one(
        'drop.location', string='Drop Off Location')
    auto_gen_customer_code = fields.Boolean(
        compute='compute_auto_gen_customer_code')
    customer_code_auto = fields.Boolean(copy=False)
    type = fields.Selection(selection_add=[('request', "Request")])
    warning = fields.Char('Warning', compute='_compute_warning')
    warning_check = fields.Boolean(default=True)

    @api.onchange('credit_limit')
    def _onchange_credit_limit(self):
        if self.credit_limit:
            float_str = str(self.credit_limit)
            str_replace = float_str.replace('.', '')
            if len(str_replace) > 12:
                raise ValidationError(
                    'Credit limit should not exceed 12 digits')

    @api.onchange('name', 'nick_name')
    def _onchange_name_check(self):
        regex = re.compile('[@_!#$%^*()<>?/\|}{~:]')
        if self.name:
            if regex.search(self.name) != None:
                raise UserError(
                    _("You cannot use special character for name."))
        if self.nick_name:
            if regex.search(self.nick_name) != None:
                raise UserError(
                    _("You cannot use special character for nickname."))

    def _compute_product_count(self):
        """
        Function to compute the number of product in the order_line
        """
        for rec in self:
            rec.product_count = len(rec.customer_product_ids)

    # def action_product_count(self):
    #

    @api.depends('name')
    def compute_auto_gen_customer_code(self):
        for rec in self:
            sales_default = self.env['sales.default'].search(
                [('operator_id', '=', self.env.company.id)])
            rec.auto_gen_customer_code = sales_default.customer_no_sequence

    @api.depends('catalog_product_ids', 'catalog_length')
    def _get_cat_prod_count(self):
        for rec in self:
            rec.catalog_length = len(rec.catalog_product_ids)

    @api.onchange('select_catalog_products')
    def _select_all(self):
        """To select all the products in the list"""
        if self.select_catalog_products:
            for catalog_product_id in self.catalog_product_ids:
                catalog_product_id.select_product = True
        else:
            for catalog_product_id in self.catalog_product_ids:
                catalog_product_id.select_product = False

    @api.onchange('catalog_ids')
    def get_products(self):
        """get the product list from product catalog """
        exist_product = self.customer_product_ids.mapped('product_id').ids
        product_ids = self.catalog_ids.catalog_product_ids
        customer_catalog = []
        for product_id in product_ids:
            self.product_catalog_ids += product_id
            product = product_id.product_id.id
            if product not in exist_product:
                dic = {
                    'product_id': product,
                    'name': product_id.product_id.name,
                    'catalog_id': product_id.catalog_id.id,
                    'product_code': product_id.product_code,
                    'uom_id': product_id.uom_id.id,
                    'categ_id': product_id.categ_id.id,
                    'tax_status': product_id.tax_status,
                    'list_price': product_id.list_price,
                    'item_cost': product_id.product_id.standard_price,
                }
                if product_id.list_price > 0:
                    dic.update({'margin_price': ((
                        product_id.list_price - product_id.product_id.standard_price) / product_id.list_price) * 100, })
                else:
                    dic.update({
                        'margin_price': 0,
                    })
                vals = (0, 0, dic)
                customer_catalog.append(vals)
        self.catalog_product_ids = [(2, 0, 0)] + customer_catalog

    def reset(self):
        self.product_ids = None
        self.catalog_ids = None
        self.catalog_product_ids = [(5, 0, 0)]
        self.select_catalog_products = True

    @api.depends('name')
    def _compute_check_group(self):
        if self.env.user.has_group('base_averigo.averigo_operator_user'):
            self.check_group = True
        else:
            self.check_group = False

    @api.depends('multiple_uom_products', 'product_select_uom_length')
    def compute_product_select_uom_length(self):
        for rec in self:
            rec.product_select_uom_length = len(rec.multiple_uom_products)

    def cancel_multiple_uom_product(self):
        self.multiple_uom_products = None
        self.product_ids = None

    @api.depends('customer_product_ids')
    def _compute_product_filter_ids(self):
        for rec in self:
            rec.product_filter_ids = None
            products = rec.customer_product_ids.mapped('product_id')
            for product in products:
                if not product.multiple_uom:
                    rec.product_filter_ids += product
                elif product.multiple_uom:
                    product_uom = product.product_uom_ids.mapped('convert_uom')
                    customer_products = self.env['customer.product'].search(
                        [('customer_product_id', '=', rec.id), ('product_id', '=', product.id)])
                    uom_length = product_uom + product.uom_id
                    cat_uom = customer_products.mapped('uom_id')
                    uom_lst = []
                    for uom in uom_length:
                        if uom not in cat_uom:
                            uom_lst.append(uom)
                    # if len(catalog_products.mapped('uom_id')) == len(uom_length):
                    if not uom_lst:
                        rec.product_filter_ids += product
            product_select = rec.customer_product_ids.filtered(
                lambda s: s.select_product is True)
            if product_select:
                rec.delete_products = True
            else:
                rec.delete_products = False

    def add_product_catalog(self):
        """ Add catalog products"""
        products = self.catalog_product_ids
        product_list = []
        for product in products:
            exist_product = self.customer_product_ids.mapped('product_id').ids
            if product.select_product:
                if product.product_id.id not in exist_product:
                    vals = (0, 0, {
                        'product_id': product.product_id.id,
                        'name': product.name,
                        'product_code': product.product_code,
                        'uom_id': product.uom_id.id,
                        'catalog_id': product.catalog_id.id,
                        'tax_status': product.tax_status,
                        'list_price': product.list_price,
                        'catalog_price': product.list_price,
                        'item_cost': product.item_cost,
                        'margin_price': product.margin_price,
                    })
                    product_list.append(vals)
        self.customer_product_ids = [(2, 0, 0)] + product_list
        self.product_ids = None
        self.catalog_ids = None
        self.catalog_product_ids = None
        self.select_catalog_products = True

    def add_product(self):
        """ Add products to Customer Product"""
        self.warning_check = True
        products = self.product_ids
        exist_product_check = self.customer_product_ids.mapped(
            'product_id').ids
        exist_product = self.product_filter_ids.ids
        product_list = []
        product_uom_lists = []
        for product in products:
            if product.id in exist_product_check:
                vals = (0, 0, {
                    'product_id': product.id
                })
                product_uom_lists.append(vals)
            elif product.id not in exist_product:
                dic = {
                    'product_id': product.id,
                    'name': product.name,
                    'product_code': product.default_code,
                    'uom_id': product.uom_id.id,
                    'tax_status': product.tax_status,
                    'item_cost': product.standard_price,
                }
                cust_list_price = 0
                if self.price_category == 'list_price_1':
                    cust_list_price = product.list_price_1
                    # dic.update({
                    #     'list_price': product.list_price_1,
                    # })
                elif self.price_category == 'list_price_2':
                    cust_list_price = product.list_price_2
                    # dic.update({
                    #     'list_price': product.list_price_2,
                    # })
                elif self.price_category == 'list_price_3':
                    cust_list_price = product.list_price_3
                    # dic.update({
                    #     'list_price': product.list_price_3,
                    # })
                elif not self.price_category:
                    cust_list_price = product.list_price
                    # dic.update({
                    #     'list_price': product.list_price,
                    # })
                dic.update({
                    'list_price': cust_list_price,
                })
                if product.list_price > 0 and cust_list_price != 0:
                    # dic.update(
                    #     {'margin_price': ((product.list_price - product.standard_price) / product.list_price) * 100, })
                    dic.update(
                        {'margin_price': ((cust_list_price - product.standard_price) / cust_list_price) * 100, })

                else:
                    dic.update(
                        {'margin_price': 0, })
                vals = (0, 0, dic)
                product_list.append(vals)
                self.product_filter_ids += product
        self.multiple_uom_products = [(2, 0, 0)] + product_uom_lists
        self.customer_product_ids = [(2, 0, 0)] + product_list
        self.product_ids = None

    def add_multiple_uom_product(self):
        """ Add products with different UOM"""
        products = self.multiple_uom_products
        product_list = []
        for product in products:
            if product.add_product:
                if not product.uom_id:
                    raise UserError(_('UOM is not selected'))
                else:
                    dic = {
                        'product_id': product.product_id.id,
                        'name': product.product_id.name,
                        'product_code': product.product_id.default_code,
                        'tax_status': product.product_id.tax_status,
                        'item_cost': product.multiple_uom_id.standard_price,
                        'uom_id': product.uom_id.id,
                    }
                    if self.price_category == 'list_price_1':
                        dic.update({
                            'list_price': product.multiple_uom_id.sale_price_1 if product.multiple_uom_id else product.product_id.list_price_1,
                        })
                    elif self.price_category == 'list_price_2':
                        dic.update({
                            'list_price': product.multiple_uom_id.sale_price_2 if product.multiple_uom_id else product.product_id.list_price_2,
                        })
                    elif self.price_category == 'list_price_3':
                        dic.update({
                            'list_price': product.multiple_uom_id.sale_price_3 if product.multiple_uom_id else product.product_id.list_price_3,
                        })
                    elif not self.price_category:
                        dic.update({
                            'list_price': product.multiple_uom_id.sale_price_1 if product.multiple_uom_id else product.product_id.list_price,
                        })
                    if product.product_id.list_price > 0:
                        dic.update(
                            {'margin_price': ((
                                product.product_id.list_price - product.product_id.standard_price) / product.product_id.list_price) * 100, })
                    vals = (0, 0, dic)
                    product_list.append(vals)
                    self.product_filter_ids += product.product_id
        self.customer_product_ids = [(2, 0, 0)] + product_list
        self.multiple_uom_products = None
        self.product_ids = None

    @api.depends('customer_product_ids', 'product_ids')
    def _compute_warning(self):
        for record in self:
            price_list = record.customer_product_ids.filtered(
                lambda s: s.list_price == 0)
            product_name = price_list.mapped('product_id.name')
            products = " "
            for i in product_name:
                products += str(i) + ' , '
            if price_list:
                record.warning = products
            else:
                record.warning = False

    def close_warning(self):
        self.warning_check = False

    @api.model
    def create(self, vals):
        res = super(CustomerOrderItems,
                    self.with_context({'mail_create_nosubscribe': True, 'tracking_disable': True})).create(vals)
        if res.is_customer:
            sales_default = self.env['sales.default'].search(
                [('operator_id', '=', res.operator_id.id)])
            sequence = self.env.ref('base_averigo.seq_customer_auto')
            if sales_default.customer_no_sequence:
                seq = sequence.with_context(force_company=res.operator_id.id).next_by_code("res.partner.customer") or _(
                    'New')
                res.code = seq
                res.customer_code_auto = True
            if 'code' not in vals or vals['code'] is False and (
                    'vms_customer_id' not in vals or not vals.get('vms_customer_id', False)):
                _logger.info(
                    '================================================')
                _logger.info(vals.get('vms_customer_id', False))
                _logger.info(
                    '================================================')
                seq = sequence.with_context(force_company=res.operator_id.id).next_by_code(
                    "res.partner.customer") or _(
                    'New')
                lim = 0
                while self.env['res.partner'].search(
                        [('code', '=', seq),
                         ('operator_id', '=', vals.get('operator_id')), ('operator_id', '=', res.operator_id.id)]).id and not vals.get('vms_customer_id', False) and lim < 10:
                    seq = sequence.with_context(force_company=res.operator_id.id).next_by_code(
                        "res.partner.customer") or _(
                        'New')
                    if seq == None or seq == False:
                        seq = self.env['res.partner'].search(
                            [('operator_id', '=', vals.get('operator_id'))], order='create_date desc', limit=1)
                        seq_ok = False
                        try_counter = 1
                        while not seq_ok:
                            if seq.id:
                                seq = int(seq.code)+try_counter
                            else:
                                seq = 1
                            try:
                                res.code = seq
                                seq_ok = True
                            except:
                                try_counter += 1
                                continue
                res.code = seq
        return res


class CustomerProduct(models.Model):
    _name = 'customer.product'
    _inherit = 'mail.thread'
    _description = 'Customer Product'

    """Product Linked to Customer"""

    active = fields.Boolean('Active', related='customer_product_id.active')
    customer_product_id = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product', index=True, required=True, translate=True,
                                 domain="[('type', 'in', ['product', 'consu'])]")
    product_code = fields.Char(
        'Product code', store=True, related='product_id.default_code')
    name = fields.Char(string="Description", related='product_id.name')
    uom_category = fields.Integer()
    uom_ids = fields.Many2many(
        'uom.uom', compute='compute_multiple_uom_id', string='Product UOMs')
    uom_id = fields.Many2one(
        'uom.uom', domain="[('category_id', '=', uom_category)]", tracking=True)
    tax_status = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], 'Taxable', tracking=True)
    order_type = fields.Many2one('order.type', string='Order Types')
    list_price = fields.Float(
        'Selling Price', readonly=False, digits='Product Price', tracking=True)
    item_cost = fields.Float(
         string='Item Cost', digits='Product Price', store=True, compute='_compute_item_cost')
    margin_price = fields.Float(string='Margin %', digits='Product Price')
    catalog_id = fields.Many2one('product.catalog')
    catalog_price = fields.Float()
    price_status = fields.Char(compute='_compute_price_status')
    select_product = fields.Boolean(default=True)

    @api.depends('product_id.standard_price')
    def _compute_item_cost(self):
        for rec in self:
            rec.item_cost = rec.product_id.standard_price

    @api.depends('product_id')
    def compute_multiple_uom_id(self):
        for rec in self:
            multiple_uom_ids = self.env['multiple.uom'].search(
                [('uom_template_id', '=', rec.product_id.product_tmpl_id.id)])
            product_uom_ids = multiple_uom_ids.mapped(
                'convert_uom') + rec.product_id.uom_id
            uom_ids = product_uom_ids
            rec.uom_ids += uom_ids

    @api.depends('list_price')
    def _compute_price_status(self):
        for rec in self:
            if rec.catalog_id:
                if rec.list_price == rec.catalog_price:
                    rec.price_status = 'Catalog - %s' % rec.catalog_id.name
                    if rec.list_price > 0:
                        rec.margin_price = (
                            (rec.list_price - rec.item_cost) / rec.list_price) * 100
                else:
                    rec.price_status = 'Entered'
                    if rec.list_price > 0:
                        rec.margin_price = (
                            (rec.list_price - rec.item_cost) / rec.list_price) * 100
            else:
                rec.price_status = 'Entered'
                if rec.list_price > 0:
                    rec.margin_price = (
                        (rec.list_price - rec.item_cost) / rec.list_price) * 100

    @api.depends('uom_id')
    @api.onchange('uom_id')
    def get_uom_id(self):
        for i in self._origin.product_id.product_uom_ids:
            cust_list_price = self._origin.product_id.list_price
            if i.convert_uom == self.uom_id:
                self.item_cost = i.standard_price
                if self.customer_product_id.price_category == 'list_price_1':
                    cust_list_price = i.sale_price_1
                elif self.customer_product_id.price_category == 'list_price_2':
                    cust_list_price = i.sale_price_2
                elif self.customer_product_id.price_category == 'list_price_3':
                    cust_list_price = i.sale_price_3
                elif not self.customer_product_id.price_category:
                    cust_list_price = i.sale_price_1
                self.list_price = cust_list_price
            elif self.uom_id == self.product_id.uom_id:
                self.item_cost = self.product_id.standard_price
                if self.customer_product_id.price_category == 'list_price_1':
                    cust_list_price = self.product_id.list_price_1
                elif self.customer_product_id.price_category == 'list_price_2':
                    cust_list_price = self.product_id.list_price_2
                elif self.customer_product_id.price_category == 'list_price_3':
                    cust_list_price = self.product_id.list_price_3
                elif not self.customer_product_id.price_category:
                    cust_list_price = self.product_id.list_price_1
                self.list_price = cust_list_price


class CustomerMultipleUom(models.Model):
    _name = 'product.customer.uom'
    _description = 'Add Multiple UOM Products to Customer'
    """Add Multiple UOM Products to Customer"""

    partner_id = fields.Many2one('res.partner')
    name = fields.Char('Product')
    product_id = fields.Many2one(
        'product.product', domain="[('multiple_uom', '=', True)]")
    uom_id = fields.Many2one('uom.uom', string='UOM')
    uom_ids = fields.Many2many(
        'uom.uom', compute='compute_multiple_uom_id', string='Product UOMs')
    multiple_uom_ids = fields.Many2many(
        'multiple.uom', compute='compute_multiple_uom_id')
    multiple_uom_id = fields.Many2one('multiple.uom')
    add_product = fields.Boolean('Add', default=True)
    micro_market_ids = fields.Many2many('stock.warehouse')

    @api.depends('product_id')
    def compute_multiple_uom_id(self):
        for rec in self:
            multiple_uom_ids = self.env['multiple.uom'].search(
                [('uom_template_id', '=', rec.product_id.product_tmpl_id.id)])
            customer_products = self.env['customer.product'].search(
                [('customer_product_id', '=', rec.partner_id.id), ('product_id', '=', rec.product_id.id)])
            product_uom_ids = multiple_uom_ids.mapped(
                'convert_uom') + rec.product_id.uom_id
            uom_ids = product_uom_ids - customer_products.mapped('uom_id')
            rec.uom_ids += uom_ids
            rec.multiple_uom_ids += multiple_uom_ids

    @api.onchange('uom_id')
    def get_uom_domain(self):
        multiple_uom = self.env['multiple.uom'].search([('uom_template_id', '=', self.product_id.product_tmpl_id.id),
                                                        ('convert_uom', '=', self.uom_id._origin.id)])
        self.multiple_uom_id = multiple_uom.id


class CustomerCatalog(models.Model):
    _name = 'catalog.customer'
    _description = 'Catalog Product in Customer'
    """Product from Selected Catalog"""

    partner_id = fields.Many2one('res.partner')
    catalog_id = fields.Many2one('product.catalog')
    product_id = fields.Many2one('product.product')
    categ_id = fields.Many2one(
        'product.category', 'Product Category', store=True, related='product_id.categ_id')
    select_product = fields.Boolean('Add', default=True)
    name = fields.Char()
    product_code = fields.Char('Product code')
    tax_status = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], 'Taxable Status')
    list_price = fields.Float(
        'Public Price', readonly=False, digits='Product Price')
    item_cost = fields.Float(
        related='product_id.standard_price', string='Item Cost', store=True)
    uom_id = fields.Many2one('uom.uom')
    margin_price = fields.Float('Margin %')


class CustomerOrderType(models.Model):
    _name = 'order.type'
    _description = "Order Type"

    name = fields.Char()
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company)
