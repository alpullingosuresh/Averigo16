from odoo import models, fields


class ResDiscountSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tax_cloud_id = fields.Char('Tax Cloud Id', config_parameter='tax_cloud_id')
    tax_cloud_key = fields.Char('Tax Cloud Key',
                                config_parameter='tax_cloud_key')


class AccountTaxUpdate(models.Model):
    _inherit = 'account.tax'

    micro_market_id = fields.Many2one('stock.warehouse', copy=False)
