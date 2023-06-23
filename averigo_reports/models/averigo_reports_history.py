from odoo import fields, models


class AverGoReportHistory(models.Model):
    _name = 'averigo.reports.history'
    _description = "Averigo Reports Usage"

    user_id = fields.Many2one('res.users', string="User")
    report_id = fields.Many2one('ir.actions.report', string="Report")
