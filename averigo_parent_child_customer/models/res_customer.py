from odoo import fields, models


class ResCustomer(models.Model):
    _inherit = "res.partner"

    front_end_children = fields.One2many('res.partner', 'parent_partner_id')
    is_frontend_boolean = fields.Boolean()

    child_count = fields.Integer(
        "Child Count", compute='_compute_child_count', store=True)
