from odoo import models, fields


class AdditionalMails(models.Model):
    _name = 'additional.emails'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)


class SowActionWizard(models.TransientModel):
    _name = "sow.action.wizard"

    email_ids = fields.Many2many('additional.emails',
                                 string='Additional Emails')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    file = fields.Binary('Documents', related='attachment_ids.datas')
    account_id = fields.Many2one('docu.credentials', 'DocuSign Account')
    crm = fields.Integer()
    data = JSON('data')
    check = fields.Boolean('checkbox')


class AgreementActionWizard(models.TransientModel):
    _name = "agreement.action.wizard"

    email_id = fields.Many2one('res.partner', string='Recipients',
                               )
    additional_emails = fields.Many2many('additional.emails',
                                         string='Additional Emails')
    attachment_ids = fields.Many2many('ir.attachment',
                                      'crm_ir_attachments_rel',
                                      'crm_id',
                                      'attachment_id', 'Attachments')
    file = fields.Binary('Documents', related='attachment_ids.datas')
    account_id = fields.Many2one('docu.credentials', 'DocuSign Account')
    crm = fields.Integer()
    check = fields.Boolean('checkbox')
