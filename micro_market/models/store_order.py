from odoo import models, fields
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES


class StoreOrder(models.Model):
    _inherit = 'stock.picking'
    _description = "Transfer"
    _order = "name desc, priority desc, date asc, id desc"

    active = fields.Boolean(string="Active", default=True)
    micro_market_id = fields.Many2one('stock.warehouse',
                                      domain="[('location_type', '=', "
                                             "'micro_market')]",
                                      states={'confirmed': [('readonly', True)],
                                              'assigned': [('readonly', True)],
                                              'done': [('readonly', True)],
                                              'cancel':
                                                  [('readonly', True)]}, )
    transit_location = fields.Many2one('stock.warehouse', 'Transit Location',
                                       domain="[('location_type', '=', "
                                              "'transit')]",
                                       states={
                                           'confirmed': [('readonly', True)],
                                           'assigned': [('readonly', True)],
                                           'done': [('readonly', True)],
                                           'cancel':
                                               [('readonly', True)]}, )
    transit_location_id = fields.Many2one('stock.location',
                                          'Transit Location Stock',
                                          states={
                                              'confirmed': [('readonly', True)],
                                              'assigned': [('readonly', True)],
                                              'done': [('readonly', True)],
                                              'cancel':
                                                  [('readonly', True)]})
    warehouse_id = fields.Many2one('stock.warehouse', 'Location',
                                   domain="[('location_type', '=', 'view')]",
                                   states={'confirmed': [('readonly', True)],
                                           'assigned': [('readonly', True)],
                                           'done': [('readonly', True)],
                                           'cancel':
                                               [('readonly', True)]})
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        check_company=True,
        # , domain="[('id', 'in', partner_ids)]",
        states={'confirmed': [('readonly', True)],
                'assigned': [('readonly', True)],
                'done': [('readonly', True)], 'cancel':
                    [('readonly', True)]})
    scheduled_date = fields.Datetime(
        'Scheduled Date', inverse='_set_scheduled_date', store=True,
        index=True, default=fields.Datetime.now, tracking=False,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Scheduled time for the first part of the shipment to be processed. Setting manually a value here would set it as expected date for all the stock moves.")
    promise_date = fields.Date(default=fields.Date.context_today,
                               states={'confirmed': [('readonly', True)],
                                       'assigned': [('readonly', True)],
                                       'done': [('readonly', True)], 'cancel':
                                           [('readonly', True)]}, tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Operator', related='picking_type_id.company_id',
        readonly=True, store=True, index=True)
    store_order_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Approved'),
        ('assigned', 'Picked'),
        ('done', 'Received'),
        ('cancel', 'Cancelled'),
    ], string='Status', copy=False, index=True, readonly=True, store=True,
        tracking=True, default='draft',
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        required=True, readonly=True,
        states={'draft': [('readonly', False)]},
    )
    priority = fields.Selection(
        PROCUREMENT_PRIORITIES, string='Priority',
        inverse='_set_priority', store=True,
        index=True, tracking=False,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Products will be reserved first for the transfers with the highest priorities.")
    route = fields.Many2one('route.route',
                            states={'confirmed': [('readonly', True)],
                                    'assigned': [('readonly', True)],
                                    'done': [('readonly', True)], 'cancel':
                                        [('readonly', True)]}, tracking=True)
    order_date = fields.Date(default=fields.Date.context_today,
                             states={'confirmed': [('readonly', True)],
                                     'assigned': [('readonly', True)],
                                     'done': [('readonly', True)], 'cancel':
                                         [('readonly', True)]}, tracking=True)
    delivered_date = fields.Date(copy=False)
    partner_address = fields.Char()
    total_quantity = fields.Integer()
    products = fields.Integer()
    reason_backorder = fields.Text('Backorder Reason')
    reason_backorder_note = fields.Text('Backorder Reason Note',
                                        related='backorder_id.reason_backorder')
    signature = fields.Binary('Warehouse Signature', copy=False,
                              attachment=True, )
    signed_by = fields.Char('Warehouse Signed By',
                            help='Name of the person that signed.', copy=False)
    signed_on = fields.Date('Warehouse Signed On',
                            help='Date of the signature.', copy=False)
    cus_signature = fields.Binary('Customer Signature', copy=False,
                                  attachment=True, )
    cus_signed_by = fields.Char('Customer Signed By',
                                help='Name of the person that signed.',
                                copy=False)
    cus_signed_on = fields.Date('Customer Signed On',
                                help='Date of the signature.', copy=False)
    store_order = fields.Boolean()
    partner_ids = fields.Many2many('res.partner')
    add_all = fields.Boolean(default=True,
                             states={'confirmed': [('readonly', True)],
                                     'assigned': [('readonly', True)],
                                     'done': [('readonly', True)], 'cancel':
                                         [('readonly', True)]})
    show_all = fields.Boolean(
        states={'assigned': [('readonly', True)], 'done': [('readonly', True)],
                'cancel': [('readonly', True)]})
    category_ids = fields.Many2many('product.category',
                                    states={'confirmed': [('readonly', True)],
                                            'assigned': [('readonly', True)],
                                            'done': [('readonly', True)],
                                            'cancel':
                                                [('readonly', True)]})
    category_dom_ids = fields.Many2many('product.category', 'id')
    transit_picking = fields.Boolean('Transit')
    transit_picking_id = fields.Many2one('stock.picking', 'Transit Picking Of')
    return_picking = fields.Boolean('Return')
    return_picking_id = fields.Many2one('stock.picking', 'Return Picking Of')
    pick_user_id = fields.Many2one('res.users', 'Picking User')
    purchase_picking = fields.Boolean()
    order_number = fields.Char()
    receive_inventory = fields.Boolean()
    extra_mm_products_length = fields.Integer()
    dom_extra_mm_products = fields.Many2many('product.product',
                                             'rel_dom_extra_mm_products')
    extra_mm_products = fields.Many2many('product.product',
                                         'rel_extra_mm_products')
    no_of_days = fields.Integer(string="Number of days")

    class StoreOrderLine(models.Model):
        _inherit = 'stock.move'
        _description = "Transfer Line"

        source_stock = fields.Integer(store=True, string='Source Stock')
        dest_stock = fields.Integer(store=True, string='Micro Market Stock')
        source_stock_uom = fields.Char()
        dest_stock_uom = fields.Char()
        max_qty = fields.Integer(string='Maximum Quantity')
        min_qty = fields.Integer(string='Minimum Quantity')
        categ_id = fields.Many2one('product.category', store=True,
                                   related='product_id.categ_id')
        active = fields.Boolean('Active', default=True)
        product_uom = fields.Many2one('uom.uom', 'Unit of Measure',
                                      required=True,
                                      domain="[('category_id', '=', product_uom_category_id)]")
        product_uom_ids = fields.Many2many('uom.uom')
        product_last_sales = fields.Integer()
        micro_market_id = fields.Many2one('stock.warehouse',
                                          string="Micro Market")

        ordered_qty = fields.Integer()
        temp_qty = fields.Float()
        product_code = fields.Char()
        product_name = fields.Char()
        select_product = fields.Boolean()
        picking_qty = fields.Integer()
        picked_qty = fields.Integer()


class DetailStoreOrderLine(models.Model):
    _inherit = 'stock.move.line'

    # Reserved qty and qty done is changed from float to integer
    move_product_ids = fields.Many2many('product.product')
    picked_qty = fields.Integer('Picked Qty')
    store_order = fields.Boolean(store=True, related='picking_id.store_order')
