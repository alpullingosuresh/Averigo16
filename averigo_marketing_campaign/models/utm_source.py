from odoo import models, fields


class UTMSource(models.Model):
    _inherit = 'utm.source'
    _description = "Campaign Type"

    name = fields.Char(string='Campaign Name', required=True, translate=True)
