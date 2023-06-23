from odoo import models, fields


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    campaign_id = fields.Many2one('utm.campaign', string='Campaign')
    subject = fields.Char('Subject', help='Subject of emails to send',
                          required=True, translate=True)
