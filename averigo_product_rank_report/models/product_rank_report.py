from odoo import models, fields


class ProductRankReport(models.TransientModel):
    _name = 'product.rank.report'
    _description = 'Product Rank Report'
    """Product Rank Report"""

    # _transient_max_count = 1

    name = fields.Char(compute='compute_name')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        domain="[('location_type', '=', 'micro_market'), ('company_id', '=', company_id)]")
    mm_dom_ids = fields.Many2many('stock.warehouse',
                                  compute='compute_partner_ids')
    start_date = fields.Date()
    end_date = fields.Date()
    report_length = fields.Integer(compute='compute_report_length')
    rank_line_ids = fields.Many2many('rank.report.line')
    rank_detail_line_ids = fields.Many2many('rank.detail.line')
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detailed', 'Detail')], default='summary',
        required=True)
    detailed_report_length = fields.Integer(compute='compute_detailed_length')
    categ_ids = fields.Many2one('product.category', 'categ_id',
                                domain="[('id', 'in', categ_dom_ids)]")
    categ_dom_ids = fields.Many2many('product.category',
                                     compute='compute_categ_ids')
    partner_ids = fields.Many2many('res.partner', string='Customer',
                                   domain="[('id', 'in', customer_ids)]")
    customer_ids = fields.Many2many('res.partner',
                                    compute='compute_partner_ids')
    period = fields.Selection(
        [('one_month', 'This Month'), ('last_month', 'Last Month'),
         ('three_month', 'Last 3 Months'),
         ('six_month', 'Last 6 Months')], default='one_month')
    previous_start_date = fields.Date(readonly=True)
    previous_end_date = fields.Date(readonly=True)


class RankReportLine(models.TransientModel):
    _name = 'rank.report.line'
    _description = 'Product Rank Line'
    """Product Rank Line"""

    rank = fields.Integer('Rank')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    product_name = fields.Char('Item Description')
    categ_name = fields.Char('Category')
    quantity = fields.Integer(string="Quantity")
    amount = fields.Float('Amount')
    rank_id = fields.Many2one('product.rank.report')


class RankDetailReport(models.TransientModel):
    _name = 'rank.detail.line'
    _description = 'Product Rank Detailed Line'

    rank = fields.Integer(string="Rank")
    item_description = fields.Char('Item Description')
    item_no = fields.Char('Item #')
    categ_name = fields.Char('Category')
    status = fields.Char('Status')
    qty_cp = fields.Integer(string="Quantity")
    qty_pp = fields.Integer(string="Quantity(Previous Period)")
    difference = fields.Integer(string="Difference")
    selling_price = fields.Float(string='Selling Price')
    amount = fields.Float(string='Amount')
    amount_pp = fields.Float(string='Amount(Previous Period)')
    rank_id = fields.Many2one('product.rank.report')
    up_bool = fields.Boolean()
    down_bool = fields.Boolean()
    neutral_bool = fields.Boolean()
