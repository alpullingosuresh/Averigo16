from odoo import fields, models


class CaseManagementTag(models.Model):
    _name = "case.management.tag"
    _description = "Case Management Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", default=lambda self: self.env.company)
