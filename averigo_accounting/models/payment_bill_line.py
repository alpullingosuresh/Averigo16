from odoo import fields, models


class PaymentBillLine(models.Model):
    _name = 'payment.bill.line'

    payment_id = fields.Many2one('account.payment')
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
