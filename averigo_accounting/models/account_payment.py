from odoo import models, fields


class AverigoAccountPayment(models.Model):
    _inherit = 'account.payment'

    customer_no = fields.Char('Customer No', size=10, related='partner_id.code',
                              states={'draft': [('readonly', False)]})
    vendor_no = fields.Char('Vendor No', size=10,
                            related='partner_id.vendor_code',
                            states={'draft': [('readonly', False)]})
    customer_debit = fields.Char('Customer Balance', copy=False)
    vendor_debit = fields.Char('Vendor Balance', copy=False)
    partner_card_id = fields.Many2one('res.partner.card',
                                      string='Customer Card',
                                      states={'draft': [('readonly', False)]})
    check_id = fields.Many2one('res.partner.check', string='Check',
                               states={'draft': [('readonly', False)]})
    check_no = fields.Char('Check No')
    check_date = fields.Date('Check Date')
    check_amount = fields.Float('Amount')
    check_bank_id = fields.Many2one('res.bank')
    partner_bank_name = fields.Char()
    notes = fields.Text()
    internal_notes = fields.Text()
    revision_no = fields.Integer('Revision No', default=0)
    revision_date = fields.Date('Revision Date',
                                default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='Owner', readonly=False,
                              default=lambda self: self.env.user.id)
    advance_payment = fields.Boolean('Advance Payment',
                                     help="This is used to identify advance payment record")
    payment_mode_id = fields.Many2one('account.payment.mode',
                                      string="Mode Of Payment")
    check = fields.Boolean('Is Check', help="This is used to give attribute")
    balance_amount = fields.Monetary(string='Balance Amount',
                                     required=True, readonly=True,
                                     states={'draft': [('readonly', False)]},
                                     tracking=True)
    reconciled_misc_receipts_ids = fields.Many2many('account.move',
                                                    string='Reconciled Misc recipts',

                                                    help="Misc Recipts whose journal items have been reconciled with these payments.")
    has_misc_receipts = fields.Boolean(
        help="Technical field used for usability purposes")
    reconciled_misc_receipts_count = fields.Integer()
    advance_count = fields.Integer(
        help="Used to hide the payment difference if there is any advance payment")
    bill_ids = fields.One2many('payment.bill.line', 'payment_id')
    unapplied_amount = fields.Float()
    extra_unapplied_amount = fields.Float()
    narration = fields.Text()
    is_advance = fields.Boolean()
    is_bank = fields.Boolean()
    is_credit_card = fields.Boolean()
    is_write_off = fields.Boolean()
    invoice_balance = fields.Float()
    cust_advance_balance = fields.Float(store=True, )
    advance_move_line_ids = fields.Many2many('account.move.line', store=True)
    phone = fields.Char(related='partner_id.phone')
    division_id = fields.Many2one('res.division')
    bill_ids_len = fields.Integer()
    account_id = fields.Many2one('account.account', string='Account',
                                 tracking=True)
    account_dom_ids = fields.Many2many('account.account')
    credit_card_id = fields.Many2one('res.partner.card', string='Credit Card',
                                     states={'draft': [('readonly', False)]})
    card_type = fields.Selection(
        [('master_card', 'Master Card'), ('visa', 'Visa')], string='Card Type',
        default='master_card')
    card_number = fields.Char('Card #')
    card_name = fields.Char('Name')
    card_expiry = fields.Date(default=fields.Date.context_today)
