from odoo import fields, models


class ProductSaleReport(models.TransientModel):
    _name = 'averigo.reports'
    _description = "Averigo Report Screen"

    name = fields.Char(default="Averigo Report")
