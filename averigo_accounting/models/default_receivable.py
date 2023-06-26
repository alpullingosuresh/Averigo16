from odoo import fields, models


class DefaultReceivable(models.Model):
    _name = 'default.receivable'
    _inherit = 'mail.thread'
    _description = 'Default Receivable'
    """Default Values In Receivable"""

    name = fields.Char(default='Receivable')
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company.id)
    due_days = fields.Integer('Aging Invoice Report (Due Days)', default=30,
                              required=True)
    due_days_2 = fields.Integer(default=60, required=True)
    due_days_3 = fields.Integer(default=90, required=True)

    receivables_control_account_id = fields.Many2one('account.account',
                                                     domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]")
    terms_discount_account_id = fields.Many2one('account.account',
                                                domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    sales_tax_liability_account_id = fields.Many2one('account.account',
                                                     domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    s_h_account_id = fields.Many2one('account.account',
                                     domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    accrued_receivable_account_id = fields.Many2one('account.account', domain=[
        ('deprecated', '=', False)])
    rental_receivable_account_id = fields.Many2one('account.account',
                                                   domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]")
    sugar_tax_account_id = fields.Many2one('account.account',
                                           domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    hazard_fee_account_id = fields.Many2one('account.account',
                                            domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    miscellaneous_receipt_control_account_id = fields.Many2one(
        'account.account', domain=[('deprecated', '=', False)])
    sales_discount_account_id = fields.Many2one('account.account',
                                                domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    advance_account_id = fields.Many2one('account.account',
                                         domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]")
    insurance_account_id = fields.Many2one('account.account',
                                           domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    write_off_account_id = fields.Many2one('account.account',
                                           domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    service_receivable_account_id = fields.Many2one('account.account',
                                                    domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]")
    fuel_charge_account_id = fields.Many2one('account.account',
                                             domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    inv_seq_id = fields.Many2one('ir.sequence', string="Invoice Sequence",
                                 domain="[('inv_seq', '=', True)]")
    inv_refund_seq_id = fields.Many2one('ir.sequence',
                                        string="Credit Note Sequence",
                                        domain="[('inv_refund_seq', '=', True)]")
    adv_payment_customer_seq_id = fields.Many2one('ir.sequence',
                                                  string="Advance Sequence",
                                                  domain="[('adv_payment_customer_seq', '=', True)]")
    invoice_receipt_seq_id = fields.Many2one('ir.sequence',
                                             string="Invoice Receipt Sequence",
                                             domain="[('invoice_receipt_seq', '=', True)]")
