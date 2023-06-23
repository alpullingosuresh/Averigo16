from odoo import models, fields


class UTMStage(models.Model):
    _inherit = 'utm.stage'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
