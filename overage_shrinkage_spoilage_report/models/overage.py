from odoo import fields, models


class OverageReport(models.TransientModel):
    _name = 'overage.report'
    _description = "Overage Report"
    _rec_name = "name"

    name = fields.Char(default="Overage Spoilage Shrinkage Report")
    customer_ids = fields.Many2many('res.partner','partner_id', string='Customer',
                                    domain="[('id', 'in', partner_ids)]")
    partner_ids = fields.Many2many('res.partner')
    mm_dom_ids = fields.Many2many('stock.warehouse','warehouse_id')
    mm_ids = fields.Many2many('stock.warehouse', string='Micromarkets')
    category_ids = fields.Many2many('product.category', string='Category')
    search_string = fields.Char(string='Item Search')
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    changes = fields.Many2many("inventory.change.type",
                               domain="[('is_portal_user', 'in', True)]")
    total_cost = fields.Float(string='Total Item Cost')
    total_price = fields.Float(string='Total Item Price')
    total_quantity = fields.Integer(string='Total Item Quantity')
    record_count = fields.Integer("Records Found")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    division_ids = fields.Many2many('res.division', string='Branch')
    dom_division_ids = fields.Many2many('res.division','division_id')
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    line_ids = fields.One2many('overage.report.lines', 'report_id')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')
    product_ids = fields.Many2many('product.product','product_id')
    product_dom_ids = fields.Many2many('product.product')
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail')], default='detail')


class InventoryChangeReportLines(models.TransientModel):
    _name = 'overage.report.lines'
    _description = "Overage Report Lines"

    mm_id = fields.Many2one("stock.warehouse", string="Micromarkets")
    user_id = fields.Many2one('res.users', string="User Name")
    date = fields.Date(string='Date')
    product_id = fields.Many2one('product.product', string="Product")
    item_code = fields.Char(string='Product Code',
                            related="product_id.default_code", store=1)
    item_description = fields.Text(string='Product Description',
                                   related="product_id.description_sale")
    category_id = fields.Many2one('product.category', string='Category',
                                  related="product_id.categ_id", store=1)
    change_type = fields.Selection([('all', 'All Changes'),
                                    ('manual', 'Overage'),
                                    ('receive', 'Receive Store Order'),
                                    ('spoil', 'Spoilage'),
                                    ('return', 'Return to Warehouse'),
                                    ('shrinkage', 'Shrinkage')],
                                   string="Change Type")
    qty = fields.Integer(string='Quantity')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    cost = fields.Float(string='Cost')
    total_cost = fields.Float(string='Total Product Cost', default=0)
    price = fields.Float(string='Product Price', default=0)
    total_price = fields.Float(string='Total Product Price', default=0)
    report_id = fields.Many2one('overage.report', ondelete="cascade")
