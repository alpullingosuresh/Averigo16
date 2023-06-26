from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MachineParts(models.Model):
    _inherit = "product.template"

    is_machine_part = fields.Boolean('Equipment Part',
                                     help="This is used to seperate Equipment part product")
    qty_available_parts = fields.Float('Quantity On Hand',
                                       digits='Product Unit of Measure')
    averigo_reordering_rules = fields.Integer('Reordering Rules')
    averigo_reordering_min_qty = fields.Float()
    averigo_reordering_max_qty = fields.Float()
