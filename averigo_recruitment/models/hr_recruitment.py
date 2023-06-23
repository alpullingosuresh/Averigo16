from odoo import fields, models


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    user_id = fields.Many2one('res.users', "Responsible",
                              domain="[('user_type', '!=', 'customer')]",
                              tracking=True, default=lambda self: self.env.uid)
