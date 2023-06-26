from odoo import models, fields


class IrSorts(models.Model):
    _name = 'ir.sorts'
    _description = "IR SORT"

    is_sort_filter = fields.Boolean("Saving the Current Loop")
    model = fields.Char("Model name")
    res_id = fields.Integer("If res model saving the res id")
    target = fields.Char("target field")
    sort_id = fields.Char("sort id")
    asc = fields.Boolean("ascending")
    viewID = fields.Integer("Current View ID")
