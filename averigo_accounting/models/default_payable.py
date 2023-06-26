from odoo import fields, models


class DefaultPayable(models.Model):
    _name = 'default.payable'
    _inherit = 'mail.thread'
    _description = 'Default Payable'
    """Default Values In Payable"""

    name = fields.Char(default='Payable')
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company.id)
    payable_account_id = fields.Many2one('account.account',
                                         domain="[('internal_type', '=', 'payable'),('deprecated', '=', False)]")
    terms_discount_account_id = fields.Many2one('account.account',
                                                domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    accrued_account_id = fields.Many2one('account.account',
                                         domain="[('deprecated', '=', False)]")
    purchase_discount_account_id = fields.Many2one('account.account',
                                                   domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    insurance_account_id = fields.Many2one('account.account',
                                           domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    misc_bill_account_id = fields.Many2one('account.account',
                                           domain="[('deprecated', '=', False)]")
    advance_account_id = fields.Many2one('account.account',
                                         domain="[('internal_type', '=', 'payable'),('deprecated', '=', False)]")
    tax_account_id = fields.Many2one('account.account',
                                     domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    ship_handling_account_id = fields.Many2one('account.account',
                                               domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    write_off_account_id = fields.Many2one('account.account',
                                           domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    bill_seq_id = fields.Many2one('ir.sequence', string="Bill Sequence",
                                  domain="[('bill_seq', '=', True)]")
    bill_refund_seq_id = fields.Many2one('ir.sequence',
                                         string="Debit Note Sequence",
                                         domain="[('bill_refund_seq', '=', True)]")
    adv_payment_vendor_seq_id = fields.Many2one('ir.sequence',
                                                string="Advance Sequence",
                                                domain="[('adv_payment_vendor_seq', '=', True)]")
    payment_vendor_seq_id = fields.Many2one('ir.sequence',
                                            string="Payment Sequence",
                                            domain="[('payment_vendor_seq', '=', True)]")
