from odoo import api, models, fields


class StockLocation(models.Model):
    """ Inherited model for creating bin location """
    _inherit = 'stock.location'
    _description = "Bin Location"

    warehouse_id = fields.Many2one('stock.warehouse', string="Location")
    max_pallets = fields.Integer(string="Max Pallets")
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    depth = fields.Float(string="Depth")
    volume = fields.Float(string="Volume")
    is_bin_location = fields.Boolean(string="Bin Location")
