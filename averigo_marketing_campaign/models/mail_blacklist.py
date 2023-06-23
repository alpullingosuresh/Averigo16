from odoo import models, fields


class MailingBlacklist(models.Model):
    _inherit = 'mail.blacklist'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
