from odoo import fields, models


class OperatorsEmailWizard(models.TransientModel):
    _name = 'operators.email.wizard'
    _description = 'Operators Email Wizard'

    name = fields.Char(string="Name")
    to_email = fields.Many2many("res.users", string="Recipient Emails")
    body = fields.Text('Rich-text Contents', help=" Message")
    subject = fields.Char('Subject', help='Subject of emails to send', required=True, translate=True)
