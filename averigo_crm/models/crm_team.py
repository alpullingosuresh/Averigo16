from odoo import models, fields


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    company_id = fields.Many2one('res.company', string="Operator",
                                 default=lambda self: self.env.company,
                                 readonly=True)
