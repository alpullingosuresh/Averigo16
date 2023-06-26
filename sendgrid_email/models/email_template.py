from odoo import models, fields


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    temp_id = fields.Char(string="Template ID")
    generation = fields.Char(string="Template Generation", default="Dynamic",
                             readonly=True)
    version_status = fields.Selection(
        [('success', 'Success'), ('failed', 'Failed To Create')])
    ver_editor = fields.Selection([('design', "Design"), ('code', "Code")],
                                  string="Version Editor", default="design")
    sedgrid_readonly = fields.Boolean(string="SendGrid Readonly Template",
                                      default=False)


class EmailTemplateDetails(models.Model):
    _name = "email.template"
    _rec_name = "temp_name"
    _description = "SendGrid Template Details"

    temp_name = fields.Char(string="Template Name", required=True)
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
    generation = fields.Char(string="Template Generation", default="Dynamic",
                             readonly=True)
    ver_name = fields.Char(string="Version Name")
    ver_subject = fields.Char(string="Version Subject", required=True)
    ver_editor = fields.Selection([('design', "Design"), ('code', "Code")],
                                  string="Version Editor", default="design")
    temp_cont = fields.Html(string="Template Content",
                            help="content convert to html code", translate=True,
                            sanitize=False)
    temp_id = fields.Char(string="Template ID")
    version_status = fields.Selection(
        [('success', 'Success'), ('Ffailed', 'Failed To Create')])
