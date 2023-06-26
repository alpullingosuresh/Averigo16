from odoo import models, fields


class SendGridSendEmails(models.Model):
    _name = "email.api"
    _description = "Email Reports"

    name = fields.Char(string="Name")
    company_name = fields.Char(string="Company Name")
    recipient_name = fields.Char(string="Recipient Name")
    to_email = fields.Char(string="Recipient Email ID")
    to_email_partner = fields.Many2one("res.partner", string="Recipient Emails")
    to_email_partner_check = fields.Boolean()
    to_email_lead = fields.Many2one("crm.lead", string="Recipient Emails")
    to_email_lead_check = fields.Boolean()
    to_email_contact = fields.Many2one("mailing.contact",
                                       string="Recipient Emails")
    to_email_contact_check = fields.Boolean()
    to_email_applicant = fields.Many2one("hr.applicant",
                                         string="Recipient Emails")
    to_email_applicant_check = fields.Boolean()
    from_email = fields.Many2one("email.sent", string="Sender Email")
    temp_type = fields.Many2one('mail.template', string="Email Template")
    temp_id = fields.Char(string="Template_id")
    send_date = fields.Datetime(string="Send Date", readonly=True,
                                default=fields.Datetime.now)
    error_msg = fields.Text(string="Error Content", readonly=True)
    error_check = fields.Boolean()
    state = fields.Selection([('send', "Send"), ('error', "Error")],
                             readonly=True, string="State", default='send')
    bounce_msg = fields.Text(string="Bounce Message")
    email_finder = fields.Integer(string="Email finder")
