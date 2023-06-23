from odoo import models, fields


class ResMonths(models.Model):
    _name = 'res.months'

    name = fields.Char(string="Month")
    code = fields.Char(string="Ccde")
    number = fields.Integer()
