from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PartsLine(models.Model):
    _name = "parts.line"

    parts_id = fields.Many2one('product.product', string="Parts",
                               required=True,
                               domain=[('is_machine_part', '=', True)])
    uom_id = fields.Many2one('uom.uom', related='parts_id.uom_id',
                             required=True)
    quantity = fields.Integer('Quantity', required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 required=True,
                                 default=lambda self: self.env.company)
    machine_id = fields.Many2one('account.asset', string="Equipment")
