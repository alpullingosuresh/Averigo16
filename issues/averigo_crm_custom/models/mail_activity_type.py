from odoo import models, fields


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    survey_template_id = fields.Many2one('survey.survey',
                                         string='Survey templates')


class MailActivityInherit(models.Model):
    _inherit = "mail.activity"

    base_url = fields.Char('Survey Url')
    crm_id = fields.Many2one('crm.lead')
    activity_type_multi_id = fields.Many2one(
        'mail.activity.type', string='Activity Type',
        domain=_activity_type_domain,
        ondelete='restrict')
    user_id = fields.Many2one(
        'res.users', 'Assigned to',
        default=lambda self: self.env.user,
        domain=_user_id_domain,
        index=True, required=True)
