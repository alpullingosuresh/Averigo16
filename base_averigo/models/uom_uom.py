from odoo import fields, models


class UomUom(models.Model):
    _inherit = 'uom.uom'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
