from odoo import fields, models


class ReturnPickingLine(models.TransientModel):
    _name = "return.picking.line"
    _description = 'Return Picking Line'

    return_picking_id = fields.Many2one('stock.return.multiple',
                                        string="Wizard Picking")
    picking_id = fields.Many2one('stock.picking', "Picking")
    sale_id = fields.Many2one('sale.order', string="Order #")
    route = fields.Char(string='Route Name')
    customer = fields.Char(string="Customer")
    source_location_id = fields.Many2one('stock.location', string='Source')
    destination_location_id = fields.Many2one('stock.location', string='Source')
    return_truck = fields.Boolean(string='Return From Truck')
    return_customer = fields.Boolean(string='Return From Customer')
    qty_undelivered = fields.Integer(string="Undelivered")


class StockReturnMultipleLine(models.TransientModel):
    _name = "stock.return.multiple.line"
    _rec_name = 'product_id'
    _description = 'Stock Return Multiple Line'

    product_id = fields.Many2one('product.product', string="Product",
                                 required=True,
                                 domain="[('id', '=', product_id)]")
    quantity = fields.Float("Quantity", digits='Product Unit of Measure',
                            required=True)
    qty_undelivered = fields.Integer("Undelivered")
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                             related='move_id.product_uom', readonly=False)
    return_id = fields.Many2one('stock.return.multiple', string="Wizard")
    move_id = fields.Many2one('stock.move', string="Move")
    return_source_id = fields.Many2one('stock.location', string='Source')
    return_dest_id = fields.Many2one('stock.location', string='Source')
    return_source_filter_ids = fields.Many2many('stock.location','source_id')
    return_dest_filter_ids = fields.Many2many('stock.location')
    picking_id = fields.Many2one('stock.picking', string="Reference #")
    sale_id = fields.Many2one('sale.order', string="Order #")


class StockReturn(models.TransientModel):
    _name = 'stock.return.multiple'
    _description = 'Stock Return Multiple'

    picking_ids = fields.Many2many('stock.picking', 'return_stock_picking_rel')
    product_return_picking = fields.One2many('return.picking.line',
                                             'return_picking_id',
                                             'Picking Return')
    product_return_moves = fields.One2many('stock.return.multiple.line',
                                           'return_id', 'Moves')
