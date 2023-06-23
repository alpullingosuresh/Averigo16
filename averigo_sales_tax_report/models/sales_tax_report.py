

from odoo import fields, models


class SalesTaxReport(models.TransientModel):
    _name = 'sales.tax.report'
    _description = "Sales Tax Report"
    _rec_name = "name"

    name = fields.Char(default="Sales Tax Report")
    partner_ids = fields.Many2many('res.partner', string='Customer',
                                   domain="[('is_customer', '=', True),"
                                          "('parent_id', '=', False),"
                                          "('type', '=', 'contact')]")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string='State',
                               domain="[('country_id', '=', country_id)]")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detail', 'Detail')], 'Report Type',
        default='detail')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    line_ids = fields.One2many('sales.tax.report.lines', 'report_id')
    micro_market_sales = fields.Boolean(default=True)
    ocs_delivery = fields.Boolean()
    sale_order = fields.Boolean()
    all_sales = fields.Boolean()
    report_length = fields.Integer()
    customer_length = fields.Integer(compute='compute_customer_length')


class SalesTaxReportLines(models.TransientModel):
    _name = 'sales.tax.report.lines'
    _description = "Sales Tax Report Lines"

    date = fields.Date(string='Date')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    report_id = fields.Many2one('sales.tax.report', ondelete="cascade")
    total_sales = fields.Float()
    non_taxable_sales = fields.Float()
    taxable_sales = fields.Float()
    tax_rate = fields.Float()
    tax_amount = fields.Float()
    city = fields.Char()
    county = fields.Char()
    state_id = fields.Many2one('res.country.state')
    state = fields.Char(related='state_id.code')
    partner_id = fields.Many2one('res.partner')
