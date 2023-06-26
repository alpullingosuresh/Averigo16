from odoo import models, fields


class StockQuantExt(models.Model):
    _inherit = 'stock.quant'
    warehouse_id = fields.Many2one('stock.warehouse', 'Location',
                                   inverse='get_location_id',
                                   domain="[('location_type', '=', 'view')]")
    location_id = fields.Many2one(
        'stock.location', 'Location Stock',
        domain=lambda self: self._domain_location_id(),
        auto_join=True, ondelete='restrict', readonly=True, required=True,
        index=True, check_company=True)
    quantity = fields.Float(
        'Quantity',
        help='Quantity of products in this quant, in the default unit of measure of the product',
        readonly=True, digits='Product Unit of Measure')
    inventory_quantity = fields.Float(
        'Inventoried Quantity',
        inverse='_set_inventory_quantity', groups='stock.group_stock_manager',
        digits='Product Unit of Measure')
    reserved_quantity = fields.Float(
        'Reserved Quantity',
        default=0.0,
        help='Quantity of reserved products in this quant, in the default unit of measure of the product',
        readonly=True, required=True, digits='Product Unit of Measure')
