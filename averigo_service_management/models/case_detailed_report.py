from odoo import models, fields


class CaseseReport(models.TransientModel):
    _name = 'case.report'
    _description = 'Case Management Report'
    _rec_name = ''

    name = fields.Char(string='Name', default='Case Management Report')
    is_reported = fields.Boolean(string="Reported From", default=True)
    reported_from = fields.Date(string='Reported From Date')
    reported_to = fields.Date(string='Reported To Date',
                              default=fields.Date.today())
    is_closed = fields.Boolean(string="Closed")
    close_from = fields.Date(string='Case Close From Date')
    close_to = fields.Date(string='Case Close To Date',
                           default=fields.Date.today())
    subject_id = fields.Many2one('case.subject', string='Subject')
    account_id = fields.Many2one('res.partner', string='Account Name')
    stage_ids = fields.Many2many('case.management.stage',
                                 'case_management_stage_report',
                                 string='Case Status')
    assigned_ids = fields.Many2many('hr.employee',
                                    'hr_employee_assigned_report',
                                    string='Assigned To')
    report_order = fields.Selection(
        [('report_date', 'Report Date'), ('closed_date', 'Closed Date')],
        default='report_date')
    sort_by = fields.Selection(
        [('ascending', 'Ascending'), ('descending', 'Descending')],
        string='Sort By',
        default='descending')

    # line_ids = fields.One2many('case.report.line', 'report_id', string='Report Lines')
    any_stage = fields.Boolean(string='Any Stage')
    line_ids = fields.Many2many('case.management', string='Report Lines')
