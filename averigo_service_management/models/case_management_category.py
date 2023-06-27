from odoo import fields, models


class CaseManagementCategory(models.Model):
    _name = "case.management.category"
    _description = "Case Management Category"

    active = fields.Boolean(string="Active", default=True, )
    name = fields.Char(string="Name", required=True, )
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company)
    issue_type_ids = fields.Many2many('issue.type', 'issue_type_category_rel', string="Issue Type")
