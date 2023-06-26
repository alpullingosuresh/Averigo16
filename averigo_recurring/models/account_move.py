from odoo import models, fields


class AccountMoveRecurring(models.Model):
    _inherit = 'account.move'

    account_bill_recurring = fields.One2many('transaction.recurring',
                                             'bill_id', string="Recurring")
    is_recurring = fields.Boolean('Is Recurring', default=False, copy=False)
    is_recurring_transaction = fields.Boolean('Is Recurring', default=False,
                                              copy=False)
