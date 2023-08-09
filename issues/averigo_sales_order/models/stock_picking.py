from odoo import models, fields
import odoo.addons.decimal_precision as dp


class StockPickingDate(models.Model):
    _inherit = 'stock.picking'

    route_id = fields.Many2one('route.route', string="Route",
                               inverse='_set_route_id',
                               store=True)
    sale_partner_id = fields.Many2one('res.partner', string="Customer",
                                      inverse='_set_sale_partner_id',
                                      store=True)
    drop_location_id = fields.Many2one('drop.location',
                                       string='Drop Off Location',
                                       inverse='_set_drop_location_id',
                                       store=True)
    note = fields.Text(string="Notes", inverse='_set_notes',
                       store=True)
    note_check = fields.Boolean()
    delivery_order = fields.Boolean(default=False,
                                    help="This is a boolean for delivery orders")
    back_delivery_order = fields.Boolean(default=False,
                                         help="This is a boolean for back delivery orders")
    invoice_pick = fields.Boolean(default=False)
    customer_code = fields.Char('Customer #', related='sale_partner_id.code')
    city = fields.Char('City', related='partner_id.city')
    qty_order = fields.Integer()
    qty_delivered = fields.Integer()
    qty_undelivered = fields.Integer()
    qty_additional = fields.Integer()
    cust_name = fields.Char('Customer Name', related='sale_partner_id.name')
    cust_nick_name = fields.Char('Nick Name',
                                 related='sale_partner_id.nick_name')
    cust_email = fields.Char('Contact Email', related='sale_partner_id.email')
    pack_slip_check = fields.Boolean('Pack Slip',
                                     help="This is a boolean for creating packslip from packslip")
    invoice_check = fields.Boolean('Invoice',
                                   help="This is boolean for creating invoice from packslip")
    delivery_check = fields.Boolean('Delivery',
                                    help="This is a boolean for creating delivery from packlip")
    delivery_status = fields.Boolean(default=False,
                                     help="This is a boolean for delivery status view")
    pick_list = fields.Boolean(default=False,
                               help="This is a boolean for pick list view")
    backorder = fields.Boolean(default=False,
                               help="This is a boolean for backorder view")
    return_picking = fields.Boolean(default=False,
                                    help="This is a return picking")
    is_return_truck = fields.Boolean(default=False,
                                     help="This picking is created a return from truck")
    is_return_cust = fields.Boolean(default=False,
                                    help="This picking is created a return from customer")
    is_created_backorder = fields.Boolean(default=False,
                                          help="This Picking is created backorder")
    is_partial = fields.Boolean(default=False, help="This is a partial picking")
    is_backorder = fields.Boolean(default=False,
                                  help="This is a backorder picking")
    direct_invoice_picking = fields.Boolean(default=False,
                                            help="This is a direct invoice picking")
    invoice_id = fields.Many2one('account.move', string="Invoice")


class StockBackorder(models.TransientModel):
    _name = 'stock.backorder'
    _description = 'Backorder'

    pick_ids = fields.Many2many('stock.picking', 'stock_backorder_rel')


class StockOrderScrap(models.Model):
    _inherit = 'stock.scrap'

    scrap_qty = fields.Float('Quantity',
                             digits=dp.get_precision('Product Unit of Measure'),
                             default=1.0, required=True,
                             states={'done': [('readonly', True)]})
