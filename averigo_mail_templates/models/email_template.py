from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True)
    default = fields.Boolean(string="Create in new operator")
    check_company = fields.Boolean()
