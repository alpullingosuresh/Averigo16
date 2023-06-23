from odoo import models, fields


class ResCustomerType(models.Model):
    _inherit = 'res.customer.type'

    color = fields.Char()