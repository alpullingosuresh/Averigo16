from odoo import models, fields


class EmployeeDiscountReport(models.TransientModel):
    _name = 'employee.discount.report'
    _description = 'Employee Discount Report'
    """Employee Discount Report"""

    # _transient_max_count = 1

    name = fields.Char(compute='compute_name')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    app_user_ids = fields.Many2many('res.app.users', string='Employees')
    employee_ids = fields.Many2many('res.app.users',
                                    compute='compute_employee_ids', store=False)
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        domain="[('location_type', '=', 'micro_market'), ('company_id', '=', company_id)]")
    start_date = fields.Date()
    end_date = fields.Date()
    date_time = fields.Datetime(string="Used Date", readonly=True,
                                default=fields.Datetime.now(), store=True)
    report_length = fields.Integer(compute='compute_report_length')
    discount_line_ids = fields.Many2many('discount.report.line')
    include_all_employees = fields.Boolean('Include All Employees')
    discount_detail_line_ids = fields.Many2many('discount.detail.line')
    report_type = fields.Selection(
        [('summary', 'Summary'), ('detailed', 'Detail')], default='summary',
        required=True)
    detailed_report_length = fields.Integer(compute='compute_detailed_length')


class DiscountReportLine(models.TransientModel):
    _name = 'discount.report.line'
    _description = 'Employee Discount Line'
    _order = 'total_discount desc'
    """Employee Discount Line"""

    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    qty = fields.Integer('Total Quantity')
    app_user = fields.Many2one('res.app.users', string="User")
    total_discount = fields.Float('Total Discount')
    total_products = fields.Integer('Total Products')
    purchase_orders = fields.Integer('Total Orders')
    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")


class DiscountDetailReport(models.TransientModel):
    _name = 'discount.detail.line'
    _description = 'Employee Discount Detailed Line'
    _order = 'total_discount desc'

    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")
    app_user = fields.Many2one('res.app.users', string="User")
    session_date = fields.Datetime(string='Order Date')
    qty = fields.Integer(string='Quantity')
    product_id = fields.Many2one('product.product', string='Product')
    product_name = fields.Char(related='product_id.name', store=True)
    list_price = fields.Float('List Price')
    price = fields.Float('Sold Price')
    total_discount = fields.Float('Total Discount')
    discount_id = fields.Many2one('employee.discount.report')
    product_category = fields.Char('Product Category',
                                   related='product_id.categ_id.name',
                                   store=True)
    invoice_no = fields.Char('Invoice No')
    payment_method = fields.Char('Payment Method')
