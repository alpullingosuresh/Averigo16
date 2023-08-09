from odoo import api, fields, models


class MergeSurveyData(models.Model):
    _inherit = "survey.user_input"

    lead_id = fields.Many2one('crm.lead')


class SendSurvey(models.TransientModel):
    _inherit = 'survey.invite'

    crm_id = fields.Many2one('crm.lead')
    survey_url = fields.Char(related=False, readonly=True)


class SurveyImageQuestion(models.Model):
    _inherit = 'survey.question'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company.id)
    question_type = fields.Selection(selection_add=[
        ('images', 'Images')
    ])
    width = fields.Selection([
        ('full_width', 'Full-Width'), ('half_width', 'Half-Width'),
        ('thrice_width', 'Thrice-width')
    ])


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    answer_type = fields.Selection(selection_add=[
        ('images', 'Images'), ('signature', 'Signature')
    ])
    file = fields.Binary('Images')
    file_type = fields.Selection([('image', 'image'), ('pdf', 'pdf')])
