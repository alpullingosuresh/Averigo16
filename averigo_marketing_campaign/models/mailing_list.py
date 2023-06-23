from odoo import models, fields


class MailingList(models.Model):
    _inherit = 'mailing.list'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
