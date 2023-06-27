from odoo import fields, models


class CaseManagementChannel(models.Model):
    _name = "case.management.channel"
    _description = "Case Management Channel"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company)
