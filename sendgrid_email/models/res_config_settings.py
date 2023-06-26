from odoo import models, fields


class SendGridApiConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    send_grid_api_check = fields.Boolean(string="SendGrid API")
    send_grid_api_value = fields.Char(string='API key',
                                      config_parameter='sendgrid.api_value')
