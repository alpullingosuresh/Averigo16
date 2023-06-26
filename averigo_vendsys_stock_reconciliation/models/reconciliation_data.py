from odoo import models, fields


class ReconciliationData(models.Model):
    _name = 'reconciliation.data'

    market_id = fields.Char(string="MarketId")
    product_id = fields.Char(string='Product')
    fills = fields.Integer(string='Fills')
    waste = fields.Integer(string='Waste')
    endcount = fields.Integer(string='EndCount')
    operator_id = fields.Char(string="OperatorID")
    status = fields.Char(string='Status')
    session_id = fields.Char(string="Session ID")
