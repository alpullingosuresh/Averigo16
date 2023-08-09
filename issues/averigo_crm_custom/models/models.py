from odoo import fields, models


class CrmLeadInherit(models.Model):
    """inherit crm.lead model to add averigo specific fields"""
    _inherit = 'crm.lead'

    stage_id = fields.Many2one('crm.stage',
                               group_expand='_read_group_stage_ids')
    no_of_rooms = fields.Integer(string="Room")
    checkin_frequency = fields.Char(string="Occupancy Rate")
    visitors_types_ids = fields.Many2many('crm.visitor.types',
                                          string="Types Of visitors")
    opportunity_url = fields.Char('Lead url')
    lead_transfer_url = fields.Char('Lead Transfer url')
    answer_count = fields.Integer()
    is_activity_scheduled = fields.Boolean('Site Survey Scheduled')
    is_won_stage = fields.Boolean('Won stage')
    is_site_survey_stage = fields.Boolean('Site survey stage')
    is_proposal_stage = fields.Boolean('Proposal stage')
    is_agreement_stage = fields.Boolean('Agreement stage')
    is_sow_stage = fields.Boolean('Sow stage')
    sales_person_agreement_ids = fields.Many2one('docusign.agreement',
                                                 "Sales Person's Signed Agreements")
    account_id = fields.Many2one('docu.credentials', 'DocuSign Account')
    document = fields.Char(string='Agreements')
    sow_document = fields.Char(string='Sow')
    complete_document = fields.Char('Agreement Status')
    sow_complete_document = fields.Char('Status')
    attach_id = fields.Many2one('ir.attachment', string='Signed Attachments')
    sow_attach_id = fields.Many2one('ir.attachment', string='Sow Documents')
    indication_note = fields.Text(tracking=True)
    sow_indication_note = fields.Text(tracking=True)
    survey_answer_id = fields.Many2one('survey.user_input')
    parent_lead_id = fields.Integer('Parent Lead Id')
    activity_id = fields.Many2one('mail.activity')
    proposal_attachment_records = fields.Boolean('Proposal Check')


class CrmAdminUsers(models.Model):
    _name = 'crm.users.notify'

    user_ids = fields.Many2many('res.users', string="Users")
    name = fields.Char(default="Admin users")


class CrmTeamInherit(models.Model):
    _inherit = 'crm.team'

    user_ids = fields.Many2many('res.users', string="Users")

class CrmStages(models.Model):
    _inherit = 'crm.stage'

    is_averigo_stage = fields.Boolean(string="Is Averigo Stage", default=False)


class Visitors(models.Model):
    _name = 'crm.visitor.types'
    _rec_name = 'visitors'
    _description = "CRM Visitor Types"

    visitors = fields.Char(string="Visitors Types")
