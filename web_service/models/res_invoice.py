from odoo import models, fields


class SessionHistory(models.Model):
    _inherit = 'user.session.history'

    invoice_no = fields.Char()
    format_date = fields.Char()
    payroll_name = fields.Char()
    uuid = fields.Char()


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    app_user = fields.Many2one('res.app.users')
    transaction_id = fields.Char()
    card_last = fields.Char()
    pay_method = fields.Char()
    sales_tax_amount = fields.Float()
    container_deposit_amount = fields.Float()
    subsidy_amount = fields.Float()


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_type = fields.Selection(
        [('app_user', "Normal Invoice"), ('payroll_invoice', "Payroll Invoice"),
         ('front_desk', "Front Desk Invoice")])
