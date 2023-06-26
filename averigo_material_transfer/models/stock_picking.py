from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_transfer = fields.Boolean()
    issuer_id = fields.Many2one('res.users', default=lambda s: s.env.user.id,
                                tracking=True)
    transfer_receiver_id = fields.Many2one('res.users', tracking=True)


class StockMove(models.Model):
    _inherit = 'stock.move'

    warehouse_dest_id = fields.Many2one('stock.warehouse',
                                        domain="[('location_type', '=', 'view')]")
    bin_dest_location = fields.Many2one('stock.location',
                                        domain="[('warehouse_id', '=', warehouse_dest_id)]")
    inventory_loc_stock = fields.Integer()
    transfer_loc_stock = fields.Integer()
