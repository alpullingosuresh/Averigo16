from odoo import models, fields


class UTMTag(models.Model):
    _inherit = 'utm.tag'
    _description = "Campaign Tags"

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
