from odoo import models, fields


class AverigoAccountMove(models.Model):
    _inherit = 'account.move'
    _description = "Invoice/BIll"

    bill_ids = fields.Many2many('account.move', 'account_move_bill_ids_rel',
                                'move_ids', 'bill_id')
    is_misc_receipt = fields.Boolean()
    receipt_type = fields.Selection([
        ('vendors', 'Vendors'),
        ('others', 'Others'),
    ], default='others', required=True, )
    payment_amount = fields.Float()
    vendor_adv_balance = fields.Float()
    bank_name = fields.Char()
    authorisation_code = fields.Char()
    transaction_ref = fields.Char()
    check_ref = fields.Char()
    credit_card_ref = fields.Char()
    name_on_card = fields.Char()
    payer_name = fields.Char()
    payment_date = fields.Date()
    card_expiry_date = fields.Date()
    receipt_distribution_lines = fields.One2many('receipt.credit.distribution',
                                                 'move_id', String="Order Line")
    account_id = fields.Many2one('account.account')
    journal_id = fields.Many2one('account.journal', string='Journal',
                                 required=True,
                                 domain=[('type', '=', 'general')])
    payment_mode_id = fields.Many2one('account.payment.mode',
                                      string="Mode Of Payment")
    payment_mode = fields.Char()
    check_id = fields.Many2one('res.partner.check', string="Check",
                               domain="[('id', 'not in', compute_check_ids), ('is_vendor', '=', True), ('is_advance', '=', True)]")
    compute_check_ids = fields.Many2many('res.partner.check')
    total_container_deposit_view = fields.Float()
    total_sales_tax_amount_view = fields.Float()
    vendor_advance = fields.Boolean(default=False,
                                    help="Used to get the vendor advance payment entry")
    customer_advance = fields.Boolean(default=False,
                                      help="Used to get the customer advance payment entry")


class AverigoAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    advance = fields.Boolean('Advance Payment Journal',
                             help="Used to identify the advance payment journal")
    check_id = fields.Many2one('res.partner.check', string="Check")
    payment_mode_id = fields.Many2one('account.payment.mode',
                                      string="Mode Of Payment")


class ReceiptCreditDistribution(models.Model):
    _name = 'receipt.credit.distribution'

    account_id = fields.Many2one('account.account',
                                 domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    amount = fields.Float()
    notes = fields.Text()
    move_id = fields.Many2one('account.move')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
