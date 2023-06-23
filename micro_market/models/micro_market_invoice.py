from odoo import models, fields


class MicroMarketInvoice(models.Model):
    _inherit = 'account.move'

    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', 'micro_market')]")


class MicroMarketInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    micro_market_id = fields.Many2one('stock.warehouse', store=True,
                                      related='move_id.micro_market_id')
    subsidy_amount = fields.Float(digits='Product Price')


class UserSessionHistory(models.Model):
    _inherit = 'user.session.history'

    subsidy_amount = fields.Float(digits='Product Price')


class SessionProductList(models.Model):
    _inherit = 'session.product.list'

    subsidy_amount = fields.Float(digits='Product Price')
