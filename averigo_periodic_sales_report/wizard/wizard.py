from odoo import models, fields


class WeeklySalesReportLine(models.TransientModel):
    """"""
    _name = 'periodic.sales.report.line'

    report_id = fields.Many2one('periodic.sales.report')
    start_date = fields.Date()
    end_date = fields.Date()
    name = fields.Char(default='Sales Report Lines')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")
    weeks = fields.Char('Weeks')
    qty_pre_week = fields.Integer(string='Previous Period',
                                  default=0)
    qty_cur_week = fields.Integer(string='Current Period',
                                  default=0)
    qty_differance = fields.Float(string='Percentage(%)')
    sales_pre_week = fields.Float(string='Previous Period($)',
                                  default=0)
    sales_cur_week = fields.Float(string='Current Period($)',
                                  default=0)
    sales_differance = fields.Float(string='Percentage(%)')
    product_with_no_sale = fields.Integer(string='Product With No Sale',
                                          default=0)
    product_sold_out = fields.Integer(string='Product Sold Out',
                                      default=0)
    type = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly')])
    qty_up_bool = fields.Boolean()
    qty_down_bool = fields.Boolean()
    qty_neutral_bool = fields.Boolean()
    qty_status = fields.Char('Status')
    sales_up_bool = fields.Boolean()
    sales_down_bool = fields.Boolean()
    sales_neutral_bool = fields.Boolean()
    sales_status = fields.Char('Status')


class TransactionReport(models.TransientModel):
    _name = 'periodic.sales.report'
    _description = "Sales Report"

    MONTH_SELECTION = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    name = fields.Char(default='Sales Report')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    report_line_ids = fields.One2many('periodic.sales.report.line', 'report_id',
                                      ondelete="cascade")
    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        domain="[('location_type', '=', 'micro_market')]")
    report_id = fields.Many2one('ir.actions.report')
    template_id = fields.Many2one('mail.template', string='Email Template',
                                  domain="[('model', '=', 'periodic.recurring')]")
    recipient_ids = fields.Many2many('res.partner', string="Recipients")
    report_length = fields.Integer(default=0)
    start_date = fields.Date()
    end_date = fields.Date()
    previous_start_date = fields.Date(readonly=True)
    previous_end_date = fields.Date(readonly=True)
    type = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly')],
                            default='weekly', )
    scheduler = fields.Boolean()
    mail_config = fields.Many2one('res.mail.config')
    year = fields.Selection(selection='_get_year', string='Year')
    month = fields.Selection(MONTH_SELECTION, string='Month')
    week = fields.Selection(selection='_get_week', string='Week')
    total_sales = fields.Float(string='Current Total Sales($)',
                               default=0)
    total_qty = fields.Integer(string='Current Total Quantity', default=0)
    pre_total_sales = fields.Float(string='Previous Total Sales($)',
                                   default=0)
    pre_total_qty = fields.Integer(string='Previous Total Quantity', default=0)
    total_no_sale_product = fields.Integer(string='Product With No Sales',
                                           default=0)
