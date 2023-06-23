from odoo import models, fields


class MicroMarket(models.Model):
    _inherit = 'stock.warehouse'

    vms_id = fields.Char(index=True)
    handled_externally = fields.Boolean(string="Handled Externally")
