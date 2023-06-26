from odoo import fields, models


# from odoo.addons.stock.models.stock_warehouse import Orderpoint


class StockWarehouseMachine(models.Model):
    _inherit = "stock.warehouse"

    machine_ids = fields.One2many('account.asset', 'micro_market_id',
                                  string="Equipment")
    is_parts_warehouse = fields.Boolean('Is Parts Warehouse',
                                        help="This is used to separate "
                                             "parts warehouse")


class StockLocation(models.Model):
    _inherit = "stock.location"
    """This field is used to check or to create a relation b/w the 
    area location and partner.The area location is 
    used in the Equipment management to transfer equipment."""
    area_partner_id = fields.Many2one('res.partner', string="Partner_id",
                                      help="The related partner id")
    area_or_pos = fields.Boolean("Area or Pos")
