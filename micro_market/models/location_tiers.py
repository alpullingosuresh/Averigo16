from odoo import models, fields


class LocationTiers(models.Model):
    _name = "location.tiers"
    _description = "Location Tiers"

    name = fields.Char(string="Name")
    field_id = fields.Many2one("ir.model.fields")
    view_id_tree = fields.Many2one("ir.ui.view")
    view_id_form = fields.Many2one("ir.ui.view")
