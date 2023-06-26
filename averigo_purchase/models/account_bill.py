
from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    to_be_printed = fields.Boolean()
    shipping_handling = fields.Float(digits='Product Price')
    insurance = fields.Float(digits='Product Price')
    total_discount = fields.Float(digits='Product Price')
    total_container_deposit = fields.Float(digits='Product Price')
    tax_amount_view = fields.Float(digits='Product Price')
    # subtotal_amount_view = fields.Float(store=1, compute='compute_total_amounts')
    picking_id = fields.Many2one('stock.picking')
    amount_total_view = fields.Float( digits='Product Price')
    from_purchase = fields.Boolean()
    from_picking = fields.Boolean()
    purchase_manager = fields.Many2one('hr.employee')
    division_id = fields.Many2one('res.division')
    department_id = fields.Many2one('hr.department')
    product_ids = fields.Many2many('product.product','product_pro_bill_ids_rel')
    dom_product_ids = fields.Many2many('product.product','pro_dom_bill_ids_rel')
    direct_bill = fields.Boolean()
    warehouse_id = fields.Many2one('stock.warehouse', 'Location',
                                   domain="[('location_type', '=', 'view'),('is_parts_warehouse', '=', False)]")


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Float('Discount', digits='Product Price')
    extra_amount_line = fields.Boolean()
    discount_amount_line = fields.Boolean()
    insurance_amount_line = fields.Boolean()
    shipping_handling_amount_line = fields.Boolean()
    container_deposit_line = fields.Boolean()
    tax_amount_line = fields.Boolean()
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    product_uom_ids = fields.Many2many('uom.uom')
    product_uom_categ = fields.Many2one('uom.category', related='product_id.uom_id.category_id')
    cost_price_unit = fields.Float(string='Unit Price', digits='Product Cost')

