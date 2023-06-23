from odoo import models, fields


class SendGridAPI(models.Model):
    _inherit = "ir.config_parameter"

    company_id = fields.Many2one('res.company', string="Company ID")
