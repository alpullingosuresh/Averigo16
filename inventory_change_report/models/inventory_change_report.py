from odoo import fields, models


class InventoryChangeReport(models.TransientModel):
    _name = 'inventory.change.report'
    _description = "Inventory Change Report"
    _rec_name = "name"

    name = fields.Char(default="Inventory Change Report")
    customer_ids = fields.Many2many('res.partner', 'customer_id_chnge_rel',
                                    string='Customer',
                                    domain="[('id', 'in', partner_ids)]")
    partner_ids = fields.Many2many('res.partner', 'partner_ids_change_rel')
    mm_dom_ids = fields.Many2many('stock.warehouse',
                                  'store_warehouse_mm_dom_rel')
    mm_ids = fields.Many2many('stock.warehouse', 'store_warehouse_mm_ids_rel',
                              string='Micro Markets')
    category_ids = fields.Many2many('product.category', string='Category')
    search_string = fields.Char(string='Item Search')
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    changes = fields.Many2many("inventory.change.type")
    total_cost = fields.Float(string='Total Item Cost',
                              currency_field="currency_id")
    total_price = fields.Float(string='Total Item Price',
                               currency_field="currency_id")
    record_count = fields.Integer("Records Found")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    line_ids = fields.One2many('inventory.change.report.lines', 'report_id')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')


class InventoryChangeReportLines(models.TransientModel):
    _name = 'inventory.change.report.lines'
    _description = "Inventory Change Report Lines"

    mm_id = fields.Many2one("stock.warehouse", string="Store")
    user_id = fields.Many2one('res.users', string="User Name")
    date = fields.Date(string='Date')
    product_id = fields.Many2one('product.product', string="Product")
    item_code = fields.Char(string='Item #', related="product_id.default_code",
                            store=1)
    item_description = fields.Text(string='Item Description',
                                   related="product_id.description_sale")
    category_id = fields.Many2one('product.category', string='Category',
                                  related="product_id.categ_id", store=1)
    change_type = fields.Selection([('all', 'All Changes'),
                                    ('manual', 'Overage'),
                                    ('receive', 'Receive Store Order'),
                                    ('spoil', 'Spoilage'),
                                    ('return', 'Return to Warehouse'),
                                    ('theft', 'Shrinkage')],
                                   string="Change Type")
    qty = fields.Integer(string='Quantity')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    cost = fields.Float(string='Cost')
    total_cost = fields.Float(string='Total Item Cost', default=0,
                              currency_field="currency_id")
    price = fields.Float(string='Item Price', default=0,
                         currency_field="currency_id")
    total_price = fields.Float(string='Total Item Price', default=0,
                               currency_field="currency_id")
    report_id = fields.Many2one('inventory.change.report', ondelete="cascade")
