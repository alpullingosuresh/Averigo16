from odoo import models, fields, api


class InventoryChangeType(models.Model):
    _inherit = "inventory.change.type"

    is_portal_user = fields.Boolean()
