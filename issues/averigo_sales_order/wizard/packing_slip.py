from odoo import fields, models


class PackingSlip(models.Model):
    _inherit = 'stock.picking.batch'
    _description = "Packing Slip"

    user_id = fields.Many2one('res.users', string='Responsible', tracking=True,
                              check_company=True,
                              default=lambda self: self.env.user,
                              help='Person responsible for this Packing Slip')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In progress'), ('done', 'Done'),
         ('cancel', 'Cancelled')], default='draft', copy=False, tracking=True,
        required=True, readonly=True)
    stock_move_ids = fields.One2many('stock.move', 'move_ids',
                                     string='Move Line')
    packing_view = fields.Boolean(default=False)
    date = fields.Date(string="Date", default=lambda self: fields.Date.today())
    no_of_copies = fields.Integer(string='Number of Copies', default=1)
    group_by = fields.Selection([('categ', 'Category'), ('bin', 'Bin')],
                                default='categ')
    total_qty = fields.Integer(string="Total Quantity")
    total_order = fields.Integer(string="Total Order")
    select_all_pick = fields.Boolean('Select All Picking')
    select_all_invoice = fields.Boolean('Select All Invoice')
    select_all_delivery = fields.Boolean('Select All Delivery')
    state_check = fields.Boolean(default=False)
    consol_pick_ids = fields.One2many('consolidated.pick.list', 'batch_id',
                                      string='Consolidated Pick List')


class StockMovePackingSlip(models.Model):
    _inherit = "stock.move"

    move_ids = fields.Many2one('stock.picking.batch',
                               string='Packing Slip Move')
    categ_id = fields.Many2one(string='Product Category',
                               related='product_id.categ_id')
    bin_location_id = fields.Many2one(string='Bin Location',
                                      related='product_id.primary_location')
    truck_driver_id = fields.Many2one(string='Truck Driver',
                                      related='picking_id.route_id.truck_id.truck_driver')


class ConsolidatedPickList(models.Model):
    _name = 'consolidated.pick.list'

    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, )

    uom = fields.Many2one('uom.uom', string='UoM')
    qty = fields.Integer(string='Picking Quantity')
    batch_id = fields.Many2one('stock.picking.batch')
    on_hand_qty = fields.Float(string='On Hand Qty')
    categ_id = fields.Many2one(string='Product Category',
                               related='product_id.categ_id')
    bin_location_id = fields.Many2one(string='Bin Location',
                                      related='product_id.primary_location')
