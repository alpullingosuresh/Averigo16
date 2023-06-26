from odoo import models, fields


class BillPayment(models.Model):
    _name = "bill.payment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bill Payment'
    """Bill Payment"""

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    amount = fields.Float()
    payment_date = fields.Date(default=fields.Date.context_today)
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')],
        default='draft')
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company.id)
    user_id = fields.Many2one('res.users',
                              default=lambda self: self.env.user.id)
    currency_id = fields.Many2one('res.currency',
                                  related='operator_id.currency_id')
    journal_id = fields.Many2one('account.journal', string='Journal',
                                 required=True, tracking=True,
                                 domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', operator_id)]")
    payment_mode_id = fields.Many2one('account.payment.mode',
                                      string="Mode Of Payment")
    account_id = fields.Many2one('account.account', string='Deposit To',
                                 required=True, tracking=True)
    account_dom_ids = fields.Many2many('account.account')
    partner_bank_account_id = fields.Many2one('res.partner.bank',
                                              string="Customer Bank Account",
                                              domain="['|', ('company_id', '=', False), ('company_id', '=', operator_id)]")
    partner_bank_name = fields.Char()
    check_id = fields.Many2one('res.partner.check', string='Check')
    partner_card_id = fields.Many2one('res.partner.card',
                                      string='Customer Card')
    card_type = fields.Selection(
        [('master_card', 'Master Card'), ('visa', 'Visa')], string='Card Type',
        default='master_card')
    card_number = fields.Char('Card #')
    vendor_advance_balance = fields.Float(store=True)
    advance_move_line_ids = fields.Many2many('account.move.line', store=True)
    bill_balance = fields.Float()
    phone = fields.Char(related='partner_id.phone')
    bill_ids = fields.One2many('bill.payment.line', 'bill_payment_id')
    bill_ids_len = fields.Integer()
    unapplied_amount = fields.Float()
    extra_unapplied_amount = fields.Float()
    narration = fields.Text()
    is_advance = fields.Boolean()
    is_bank = fields.Boolean()
    is_credit_card = fields.Boolean()
    is_check = fields.Boolean()
    is_write_off = fields.Boolean()
    check_no = fields.Char()


class BillPaymentLines(models.Model):
    _name = "bill.payment.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bill Payment Lines'
    """Bill Payment Lines"""

    bill_payment_id = fields.Many2one('bill.payment')
    bill_id = fields.Many2one('account.move')
    operator_id = fields.Many2one('res.company', related='bill_id.company_id')
    currency_id = fields.Many2one('res.currency', related='bill_id.currency_id')
    name = fields.Char('Bill #', related='bill_id.name')
    partner_id = fields.Many2one('res.partner', related='bill_id.partner_id')
    bill_date_due = fields.Date(related='bill_id.invoice_date_due')
    amount_total_view = fields.Float(related='bill_id.amount_total_view')
    amount_adjusted = fields.Float()
    amount_residual = fields.Float()
    bill_amount_residual = fields.Monetary(related='bill_id.amount_residual')
    amount_residual_changed = fields.Boolean()
    advance_amount = fields.Float()
    amount_received = fields.Float()
    due_amount = fields.Float(store=True)
    advance_move_line_id = fields.Many2one('account.move.line',
                                           string='Advance',
                                           copy=False)
    have_advance_value = fields.Boolean()
    filter_advance_move_line_ids = fields.Many2many('account.move.line')
    unapplied_amount = fields.Float()
