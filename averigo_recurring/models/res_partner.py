from odoo import models, fields


class ResPartnerRecurring(models.Model):
    _inherit = 'res.partner'

    recurring_count = fields.Integer('Recurring Count')
