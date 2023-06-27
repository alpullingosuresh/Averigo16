from odoo import models, fields, api, _


class CaseSubject(models.Model):
    _name = 'case.subject'
    _description = 'Case Subject'

    name = fields.Char(string='Subject', required=True)
    company_id = fields.Many2one('res.company', 'Operator',
                                 default=lambda self: self.env.company)