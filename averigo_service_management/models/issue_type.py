from odoo import fields, models


class IssueType(models.Model):
    _name = "issue.type"
    _description = "Issue Type"

    name = fields.Char()
    category_id = fields.Many2one('case.management.category', string="Category")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company)
