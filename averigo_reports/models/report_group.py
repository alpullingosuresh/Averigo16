from odoo import fields, models


class ReportGroup(models.Model):
    _name = 'report.group'
    _description = "Averigo Report Groups"

    name = fields.Char(string='Group Name', required=True)

    _sql_constraints = [("name_uniq", "unique(name)",
                         "Report group name must be unique!")]
