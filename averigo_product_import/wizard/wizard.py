# -*- coding: utf-8 -*-
from odoo import fields, models


class AverigoProductImport(models.TransientModel):
    _name = 'product.import'
    _description = 'Product Import Wizard'
    file = fields.Binary(string="Select File")
    file_type = fields.Selection([('csv', 'CSV'), ('xls', 'XLS / XLSX')],
                                 default='csv')
