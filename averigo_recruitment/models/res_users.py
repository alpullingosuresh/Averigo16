from odoo import models, fields


class ResUsersRecruitment(models.Model):
    _inherit = 'res.users'

    group_recruitment_operator = fields.Boolean(string="Recruitment",
                                                default=True)
