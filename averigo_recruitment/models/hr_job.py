from odoo import fields, models


class Job(models.Model):
    _inherit = 'hr.job'

    user_id = fields.Many2one('res.users', "Responsible",
                              domain="[('user_type', '!=', 'customer')]",
                              tracking=True)
    hr_responsible_id = fields.Many2one(
        'res.users', "HR Responsible",
        domain="[('user_type', '!=', 'customer')]", tracking=True,
        help="Person responsible of validating the employee's contracts.")


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    default_user_id = fields.Many2one("res.users", string="Default User",
                                      domain="[('user_type', '!=', 'customer')]"
                                      )
