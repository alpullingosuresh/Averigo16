from odoo import models, fields


class SendGridEmail(models.Model):
    _inherit = 'mailing.mailing'

    email_temp = fields.Many2one("mail.template", string="Email Template")
    temp_id = fields.Char(string="Template ID")
    from_email = fields.Many2one("email.sent", string="Sender Email")
    to_email_partner = fields.Many2many("res.partner",
                                        string="Recipient Emails")
    to_email_partner_check = fields.Boolean()
    to_email_lead = fields.Many2many("crm.lead", string="Recipient Emails")
    to_email_lead_check = fields.Boolean()
    to_email_contact = fields.Many2many("mailing.contact",
                                        string="Recipient Emails")
    to_email_contact_check = fields.Boolean()
    to_email_applicant = fields.Many2many("hr.applicant",
                                          string="Recipient Emails")
    to_email_applicant_check = fields.Boolean()
    email_finder = fields.Integer(string="Email finder")
    sent_count = fields.Integer(string="Send Count")
    send_grid_check = fields.Boolean()
    temp_check = fields.Boolean()
