from odoo import fields, models
import datetime


class PortalCaseManagement(models.Model):
    _inherit = 'case.management'

    portal_case = fields.Boolean()
    year = fields.Char(string='Year', required=True,
                       default=lambda x: str(datetime.datetime.now().year))
    portal_subject = fields.Char(string='Subject')
    is_portal = fields.Boolean(string='Is Portal')

