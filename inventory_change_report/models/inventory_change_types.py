from odoo import models, fields


class InventoryChangeType(models.Model):
    _name = "inventory.change.type"
    _description = "Inventory Change Type"
    _order = 'sequence asc'

    name = fields.Char("Name")
    code = fields.Char("Code")
    sequence = fields.Integer()
