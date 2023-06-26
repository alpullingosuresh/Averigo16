from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    add_button = fields.Boolean('Add')

    warehouse_id = fields.Many2one('stock.warehouse', 'Location',
                                   domain="[('location_type', '=', 'view'),"
                                          " ('is_parts_warehouse', '!=', True)]")
    material_receipt = fields.Boolean()
    to_be_printed = fields.Boolean()
    product_ids = fields.Many2many('product.product','pro_pick_ids_rel',
                                   domain="[('type', 'in', ['product'])]")
    dom_product_ids = fields.Many2many('product.product','pro_dom_pick_ids_rel')
    purchase_manager = fields.Many2one('hr.employee', tracking=True)
    purchase_order_date = fields.Datetime(related='purchase_id.date_order')
    division_id = fields.Many2one('res.division', tracking=True)
    department_id = fields.Many2one('hr.department', tracking=True)
    receiver_id = fields.Many2one('res.users', default=lambda s: s.env.user.id,
                                  tracking=True)
    service_product_purchase = fields.Boolean()
    bill_picking = fields.Boolean()
    account_move_id = fields.Many2one('account.move')
    is_purchase_return = fields.Boolean(default=False,
                                        string='Is Purchase Return')


class StockMove(models.Model):
    _inherit = 'stock.move'

    cost_price = fields.Float(digits='Product Cost')
    product_value = fields.Float(digits='Product Price')
    dom_location_id = fields.Many2one('stock.location',
                                      related='picking_id.warehouse_id.lot_stock_id')
    dom_location_ids = fields.Many2many('stock.location')
    bin_location = fields.Many2one('stock.location',
                                   domain="[('location_id', '=', dom_location_id)]")
