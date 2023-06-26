from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    message = fields.Text(string="Message", related='sale_id.message')
    visited = fields.Boolean(string="visited", default=False)
