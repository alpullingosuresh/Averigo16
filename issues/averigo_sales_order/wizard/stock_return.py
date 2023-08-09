from odoo import fields, models


class StockReturnLine(models.TransientModel):
    _name = "stock.return.line"
    _rec_name = 'product_id'
    _description = 'Stock Return Line'

    product_id = fields.Many2one('product.product', string="Product",
                                 required=True,
                                 domain="[('id', '=', product_id)]")
    quantity = fields.Float("Quantity", digits='Product Unit of Measure',
                            required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                             related='move_id.product_uom', readonly=False)
    return_id = fields.Many2one('stock.return', string="Wizard")
    move_id = fields.Many2one('stock.move', "Move")
    return_source_id = fields.Many2one('stock.location', string='Source')
    return_dest_id = fields.Many2one('stock.location', string='Source')
    return_source_filter_ids = fields.Many2many('stock.location')
    return_dest_filter_ids = fields.Many2many('stock.location','location_id')


class StockReturn(models.TransientModel):
    _name = 'stock.return'
    _description = 'Stock Return'

    picking_id = fields.Many2one('stock.picking')
    product_return_moves = fields.One2many('stock.return.line', 'return_id',
                                           'Moves')
    location_id = fields.Many2one('stock.location', 'Return Location')
    location_dest_id = fields.Many2one('stock.location', 'Source Location')
    return_truck = fields.Boolean('Return From Truck')
    return_cust = fields.Boolean(help="This is a used to show warning")
