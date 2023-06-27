from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    case_id = fields.Many2one('case.management', 'Case', index=True)
    machine_id = fields.Many2one('account.asset', 'Machine')
    machine_filter_ids = fields.Many2many('account.asset',
                                          compute='_compute_machine_filter_ids')
    billable = fields.Boolean('Billable')
    timesheet_amount = fields.Float('Amount')
    account_id = fields.Many2one('account.analytic.account', 'Analytic Account',
                                 required=True, ondelete='restrict',
                                 index=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
