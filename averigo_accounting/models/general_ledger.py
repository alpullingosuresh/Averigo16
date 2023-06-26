from odoo import fields, models


class GeneralLedger(models.Model):
    _name = 'general.ledger'
    _inherit = 'mail.thread'
    _description = 'General Ledger'
    """Default Setup General Ledger"""

    name = fields.Char()
    restock_fee_credit_debit = fields.Boolean()
    restock_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('amount', 'Amount')], index=True, tracking=True)
    restock_fee_percent = fields.Float()
    restock_amount = fields.Float()
    display_account = fields.Many2one('account.account',
                                      domain=[('deprecated', '=', False)])
    service_charges = fields.Many2one('account.account',
                                      domain=[('deprecated', '=', False)])
    interest_earned = fields.Many2one('account.account',
                                      domain=[('deprecated', '=', False)])
    interest_paid = fields.Many2one('account.account',
                                    domain=[('deprecated', '=', False)])
    undeposited_funds = fields.Many2one('account.account',
                                        domain=[('deprecated', '=', False)])
    retained_earnings = fields.Many2one('account.account',
                                        domain=[('deprecated', '=', False)])
    journal_adjustment = fields.Many2one('account.account',
                                         domain=[('deprecated', '=', False)])
    restock_fee = fields.Many2one('account.account',
                                  domain=[('deprecated', '=', False)])
