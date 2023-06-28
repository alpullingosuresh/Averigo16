from odoo import models, fields


class UoMCustomTypes(models.Model):
    _name = "custom.uom.types"

    name = fields.Char('Name', required=True)
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)


class ProductUoM(models.Model):
    _inherit = 'multiple.uom'

    name = fields.Char(string="Name", reqired=False)
    type = fields.Many2one('custom.uom.types', string='UoM', required=True)
