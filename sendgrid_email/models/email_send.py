from odoo import models, fields


class EmailDetails(models.Model):
    _name = "email.sent"
    _description = 'SendGrid From Email'
    _rec_name = 'email_id'

    name = fields.Char(string="Name", required=True)
    email_id = fields.Char(string="Email ID", required=True)
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
