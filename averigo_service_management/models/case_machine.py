from odoo import fields, models


class CaseEquipment(models.Model):
    _inherit = 'account.asset'

    case_ids = fields.Many2many('case.management', 'machine_case_rel',
                                'asset_id', 'case_id', string="Cases")
    case_count = fields.Char(string="Case Count")
    todo_case_count = fields.Integer(string="Number of Cases")
    todo_case_count_unassigned = fields.Integer(
        string="Number of cases unassigned")
    todo_case_count_unattended = fields.Integer(
        string="Number of cases unattended")
    todo_case_count_high_priority = fields.Integer(
        string="Number of cases in high priority")
    todo_case_count_closed = fields.Integer(string="Number of cases in closed")
    machine_recurring_id = fields.Many2one('transaction.recurring', copy=False)
    frequency_date = fields.Date('Next Scheduled Date', copy=False)
    frequency_start_date = fields.Date(default=fields.Date.today, copy=False)
    next_execution_date = fields.Date(copy=False)
    maintenance_duration = fields.Float(help="Maintenance Duration in hours.")
