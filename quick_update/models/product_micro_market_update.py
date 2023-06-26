from odoo import models, fields


class ProductMicroMarketUpdate(models.Model):
    _name = 'product.micro.market.update'
    _inherit = 'product.micro.market'
    _rec_name = 'note'
    _description = "Products Micro Market Update"

    actual_qty = fields.Integer(string="Actual")
    spoiled_qty = fields.Integer(string="Spoiled")
    theft_qty = fields.Integer(string="Theft")
    return_qty = fields.Integer(string="Return")
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse",
                                   domain=[('location_type', '=', 'view')])
    new_max = fields.Integer(string="New Max")
    new_min = fields.Integer(string="New Min")
    new_crv = fields.Many2one('account.tax', domain="[('crv', '=',  True)]",
                              string="New CRV")
    new_crv_amount = fields.Float(string="Container Deposit Amount")
    is_container_tax = fields.Boolean('Container Deposit',
                                      related='product_id.is_container_tax')
    new_tax = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Tax")
    note = fields.Text(string="Notes")
    check = fields.Boolean()
    updated = fields.Boolean()
    quick_update_id = fields.Many2one('quick.update')
    scrap_id = fields.Many2one('stock.scrap')
    picking_id = fields.Many2one('stock.picking')
    cur_mm_stock = fields.Integer(string="Market Stock")
    inventory_id = fields.Many2one("stock.inventory",
                                   string="Inventory Adjustment", index=True)
    pmm_id = fields.Many2one('product.micro.market', string="PMM Id")
    stored_cost = fields.Float()
