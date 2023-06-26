from odoo import models, fields


class MicroMarketWarehouse(models.Model):
    _inherit = "stock.warehouse"

    cc_fees = fields.Float(tracking=True)
    app_fees = fields.Float(tracking=True)
    stored_fund_fees = fields.Float(tracking=True)
    brand_fees = fields.Float(tracking=True)
    management_fees = fields.Float(tracking=True)
    platform_fees = fields.Float(tracking=True)
    platform_fees_type = fields.Selection(
        [('percentage', 'Percentage'), ('fixed', 'Fixed')], required=True,
        tracking=True, default='percentage')
    platform_fees_per_day = fields.Float(store=1)
    commission_percentage = fields.Float(tracking=True)
    room_cc = fields.Float('Hotel CC', tracking=True)
    cash_adj = fields.Float(tracking=True)
    additional_fees1 = fields.Float('Group %', tracking=True)
    additional_group1_id = fields.Many2one('customer.fees', string='Group',
                                           tracking=True)
    additional_group1_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], string='Group Base Factor',
        tracking=True)
    additional_fees2 = fields.Float(tracking=True)
    additional_group2_id = fields.Many2one('customer.fees', tracking=True)
    additional_group2_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    additional_fees3 = fields.Float(tracking=True)
    additional_group3_id = fields.Many2one('customer.fees', tracking=True)
    additional_group3_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    group_id = fields.Many2one('customer.fees', string='Hotel Commission',
                               tracking=True)
    group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True, string='Hotel Commission Base Factor')
    group_fees_percentage = fields.Float('Hotel Commission %', tracking=True)
    brand_id = fields.Many2one('customer.fees', tracking=True)
    brand_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    # brand_fees_percentage = fields.Float(tracking=True)
    management_id = fields.Many2one('customer.fees', tracking=True)
    management_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    # management_fees_percentage = fields.Float(tracking=True)
    purchasing_group_id = fields.Many2one('customer.fees', tracking=True)
    purchasing_group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    purchasing_group_fees_percentage = fields.Float(tracking=True)
    national_sales_team_id = fields.Many2one('customer.fees', tracking=True)
    national_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    national_sales_fees_percentage = fields.Float(tracking=True)
    local_sales_team_id = fields.Many2one('customer.fees', tracking=True)
    local_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')],
        tracking=True)
    local_sales_fees_percentage = fields.Float(tracking=True)
    fees_template_id = fields.Many2one('fees.distribution')
    fees_changed = fields.Boolean()


class UserSessionHistory(models.Model):
    _inherit = 'user.session.history'

    cc_fees = fields.Float()
    app_fees = fields.Float()
    stored_fund_fees = fields.Float()
    brand_fees = fields.Float()
    management_fees = fields.Float()
    platform_fees = fields.Float()
    fixed_platform = fields.Boolean()
    commission_percentage = fields.Float()
    room_cc = fields.Float()
    cash_adj = fields.Float()
    additional_fees1 = fields.Float()
    additional_group1_id = fields.Many2one('customer.fees', tracking=True)
    additional_group1_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    additional_fees2 = fields.Float()
    additional_group2_id = fields.Many2one('customer.fees', tracking=True)
    additional_group2_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    additional_fees3 = fields.Float()
    additional_group3_id = fields.Many2one('customer.fees', tracking=True)
    additional_group3_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')], tracking=True)
    group_id = fields.Many2one('customer.fees')
    group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    group_fees_percentage = fields.Float()
    brand_id = fields.Many2one('customer.fees')
    brand_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    # brand_fees_percentage = fields.Float(tracking=True)
    management_id = fields.Many2one('customer.fees')
    management_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    # management_fees_percentage = fields.Float(tracking=True)
    purchasing_group_id = fields.Many2one('customer.fees')
    purchasing_group_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'),
         ('platform_fees', 'Platform Fees')])
    purchasing_group_fees_percentage = fields.Float()
    national_sales_team_id = fields.Many2one('customer.fees')
    national_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    national_sales_fees_percentage = fields.Float()
    local_sales_team_id = fields.Many2one('customer.fees')
    local_sales_base_factor = fields.Selection(
        [('margin', 'Margin'), ('net_sales', 'Net Sales'),
         ('gross_sales', 'Gross Sales'), ('platform_fees', 'Platform Fees')])
    local_sales_fees_percentage = fields.Float()


class SessionProductList(models.Model):
    _inherit = 'session.product.list'

    cost_price = fields.Float(digits='Product Price')
