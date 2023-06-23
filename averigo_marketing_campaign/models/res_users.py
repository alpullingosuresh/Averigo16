from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    group_mail_marketing = fields.Boolean(string="Mail Marketing",
                                          default=True)
