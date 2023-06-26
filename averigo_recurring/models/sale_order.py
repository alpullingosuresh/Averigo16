from odoo import models, fields


class SaleOrderRecurring(models.Model):
    _inherit = 'sale.order'

    sale_recurring = fields.One2many('transaction.recurring', 'sale_id',
                                     string="Recurring")
    is_recurring = fields.Boolean('Is Recurring', default=False, copy=False)
    is_recurring_transaction = fields.Boolean('Is Recurring', default=False,
                                              copy=False)
