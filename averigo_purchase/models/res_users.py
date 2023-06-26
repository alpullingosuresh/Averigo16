
from odoo import models, fields
class ResUsers(models.Model):
    _inherit = 'res.users'



    group_purchase_order_lock = fields.Boolean(string="Purchase Order Lock/Unlock", default=True)
    warehouse_id = fields.Many2one('stock.warehouse', tracking=True, domain="[('location_type', '=', 'view')]")

