from odoo import models, fields


class InvoiceReceipt(models.Model):
    _name = "invoice.receipt"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Invoice Receipt'
    """Invoice Receipt"""

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    amount = fields.Float()
    receipt_date = fields.Date(default=fields.Date.context_today)
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')],
        default='draft')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company.id)
    user_id = fields.Many2one('res.users',
                              default=lambda self: self.env.user.id)
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    journal_id = fields.Many2one('account.journal', string='Journal',
                                 required=True, tracking=True,
                                 domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', company_id)]")
    payment_mode_id = fields.Many2one('account.payment.mode',
                                      string="Mode Of Payment")
    account_id = fields.Many2one('account.account', string='Deposit To',
                                 required=True, tracking=True)
    account_dom_ids = fields.Many2many('account.account')
    partner_bank_account_id = fields.Many2one('res.partner.bank',
                                              string="Customer Bank Account",
                                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    partner_bank_name = fields.Char()
    check_id = fields.Many2one('res.partner.check', string='Check')
    partner_card_id = fields.Many2one('res.partner.card',
                                      string='Customer Card')
    card_type = fields.Selection(
        [('master_card', 'Master Card'), ('visa', 'Visa')], string='Card Type',
        default='master_card')
    card_number = fields.Char('Card #')
    cust_advance_balance = fields.Float(store=True)
    advance_move_line_ids = fields.Many2many('account.move.line', store=True)
    invoice_balance = fields.Float()
    phone = fields.Char(related='partner_id.phone')
    invoice_ids = fields.One2many('invoice.receipt.line', 'invoice_receipt_id')
    invoice_ids_len = fields.Integer()
    unapplied_amount = fields.Float()
    extra_unapplied_amount = fields.Float()
    narration = fields.Text()
    is_advance = fields.Boolean()
    is_bank = fields.Boolean()
    is_credit_card = fields.Boolean()
    is_check = fields.Boolean()
    is_write_off = fields.Boolean()
    check_no = fields.Char()


class InvoiceReceiptLines(models.Model):
    _name = "invoice.receipt.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Invoice Receipt Lines'
    """Invoice Receipt Lines"""

    invoice_receipt_id = fields.Many2one('invoice.receipt')
    invoice_id = fields.Many2one('account.move')
    company_id = fields.Many2one('res.company', related='invoice_id.company_id')
    currency_id = fields.Many2one('res.currency',
                                  related='invoice_id.currency_id')
    name = fields.Char('Invoice #', related='invoice_id.name')
    partner_id = fields.Many2one('res.partner', related='invoice_id.partner_id')
    invoice_date_due = fields.Date(related='invoice_id.invoice_date_due')
    amount_total_view = fields.Float(related='invoice_id.amount_total_view')
    amount_adjusted = fields.Float()
    amount_residual = fields.Float()
    invoice_amount_residual = fields.Monetary(
        related='invoice_id.amount_residual')
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
