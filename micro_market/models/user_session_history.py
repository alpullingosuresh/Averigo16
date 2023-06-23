from odoo import fields, models


class UserSessionHistory(models.Model):
    _inherit = 'user.session.history'

    additional_tax_label_1 = fields.Char()
    additional_tax_rate_1 = fields.Float()
    additional_tax_label_2 = fields.Char()
    additional_tax_rate_2 = fields.Float()
    additional_tax_label_3 = fields.Char()
    additional_tax_rate_3 = fields.Float()
    micro_market_id = fields.Many2one('stock.warehouse',
                                      string="Micromarket Name", index=True)


class SessionProductList(models.Model):
    _inherit = 'session.product.list'

    additional_tax_amount_1 = fields.Float()
    additional_tax_amount_2 = fields.Float()
    additional_tax_amount_3 = fields.Float()
