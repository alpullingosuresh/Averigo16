# -*- coding: utf-8 -*-

from odoo import fields, models


class MasterSearch(models.Model):
    _name = 'master.search'
    _description = "Model for master search"
    _rec_name = 'name'
    _order = "create_date desc"

    name = fields.Char(string="Name")
    res_customers_id = fields.Many2many('res.partner',
                                        'res_customers_search_rel',
                                        'res_customers_id', 'search_id',
                                        string="Locations")
    search_string = fields.Char(string="Search")
    search_mode = fields.Selection(
        [('all', 'All'), ('active', 'Active'), ('inactive', 'Inactive')],
        string="Search Mode", default="active")
    search_by = fields.Selection([('any', 'Any'), ('customer', 'Customer'),
                                  ('micro market', 'Micro Market'),
                                  ('product', 'Product'),
                                  ('transaction details',
                                   'Transactions')],
                                 string="Search By", default='any')
    master_search_ids = fields.Many2many('master.search',
                                         'master_search_self_rel', 'search_id',
                                         'search_id1',
                                         compute="_get_recent_searches",
                                         limit=1)
    history_count = fields.Integer(string="History Count",
                                   compute="_get_history_count")
    customer_ids = fields.Many2many('res.partner',
                                    'master_search_company_rel', 'search_id',
                                    'company_id')
    product_ids = fields.Many2many('product.template',
                                   'master_search_product_rel', 'search_id',
                                   'company_id', )
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        'master_search_micro_market_rel',
                                        'search_id', 'company_id', )
    transaction_details = fields.Many2many('stock.picking',
                                           'master_search_transaction_details_rel',
                                           'search_id',
                                           'company_id', )
    customer_count = fields.Integer(string="Company Count",
                                    compute="_get_operator_count")
    product_count = fields.Integer(string="Product Count",
                                   compute="_get_product_count")
    market_count = fields.Integer(string="Product Count",
                                  compute="_get_market_count")
    transaction_count = fields.Integer(string="Transaction Count",
                                       compute="_get_transaction_count")
    user_id = fields.Many2one('res.users', string="User",
                              default=lambda self: self.env.user)
    match_entire = fields.Boolean(string="Match entire sentence")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    transaction_amount = fields.Float(string="Amount")


class MicroMarketAddress(models.Model):
    _inherit = 'stock.warehouse'

    market_address = fields.Char()

    count_total_products = fields.Integer(string="Total Product")
    available_quantity = fields.Integer(string="Available Quantity")
    below_reorder_level = fields.Integer(string="Below Reorder Level")
