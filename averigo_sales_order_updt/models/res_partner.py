from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    advance_balance_amount = fields.Float()
