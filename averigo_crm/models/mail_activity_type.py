from odoo import models, fields


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"
    _description = "Activity Types"

    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
