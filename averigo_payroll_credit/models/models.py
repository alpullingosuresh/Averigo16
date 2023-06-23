# -*- coding: utf-8 -*-


from odoo import models, fields


class ResAppUsers(models.Model):
    _inherit = 'res.app.users'

    employee_id = fields.Char(string='Employee id')
    payroll_id = fields.Many2one('prepaid.purchase', string="Payroll")


class EmployeeCreditLimit(models.Model):
    _name = 'employee.credit.limit'
    _description = 'Payroll Credit Line'

    app_user = fields.Many2one('res.app.users', string="User")
    employee_id = fields.Char(string='Employee ID')
    credit_limit = fields.Float(string="Limit")
    payroll_id = fields.Many2one('prepaid.purchase', string="Payroll")
    micro_market_id = fields.Many2one('stock.warehouse', string="Micro Market")
    disable_user = fields.Boolean('Disable User', default=False)
    app_user_name = fields.Char(related='app_user.name', string='Name', readonly=True)
    email = fields.Char(related='app_user.email', readonly=True)
    first_name = fields.Char()
    last_name = fields.Char()
    user_email = fields.Char()


class PrepaidPurchase(models.Model):
    _name = 'prepaid.purchase'
    _description = 'Other Payment Methods'

    _rec_name = 'nick_name'
    nick_name = fields.Char(string="Nick Name")
    payroll_id = fields.Char(string="Account ID")
    active = fields.Boolean(string="Active", default=True)
    deduction_type = fields.Selection(
        [('payroll', 'Payroll Deduction'), ('credit', 'Credit'), ('company', 'Company Credit')], required=True,
        default='payroll')
    partner_id = fields.Many2one('res.partner', string="Bill To Customer", required=True)
    partner_ids = fields.Many2many('res.partner', compute='compute_partner_ids')
    spending_limit = fields.Float(string="Spending Limit")
    disable_payroll = fields.Boolean(string="Disable Account")
    rollover_payroll = fields.Boolean(string="Enable Rollover", default=False)
    allow_unlimited = fields.Boolean(string="Allow Unlimited Spending")
    date_configuration = fields.Selection(
        [('daily', 'Daily'), ('day_of_week', 'Day of Week'), ('day_of_month', 'Day of Month')])
    period_length_week = fields.Selection([('1', '1 Week'), ('2', '2 Weeks')], string="Period Length", default='1')
    period_length_month = fields.Selection(
        [('1', '1st - Last Day of Month'), ('2', '(1-15th) and (16th-Last Day of Month)')], string="Period Length",
        default='1')
    payroll_starts = fields.Date(string="Payroll Starts On")
    micro_markets = fields.Many2one('stock.warehouse', string="Micro Market")
    micro_market_ids = fields.Many2many('stock.warehouse', domain=[('location_type', '=', 'micro_market')])
    app_users = fields.One2many('employee.credit.limit', 'payroll_id', ondelete='cascade')
    app_user_ids = fields.Many2many('res.app.users', 'payroll_id', string='App Users')
    app_user_filter_ids = fields.Many2many('res.app.users', compute='_compute_app_user_filter_ids')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
