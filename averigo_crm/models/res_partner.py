from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    reports_to = fields.Char(string="Email Reports To")
    from_lead = fields.Boolean(string="Is Created From Lead", default=False)
    count = fields.Integer(string="Count")
    mail_activities_count = fields.Integer()
