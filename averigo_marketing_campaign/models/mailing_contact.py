from odoo import models, fields


class MailingContact(models.Model):
    _inherit = 'mailing.contact'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
