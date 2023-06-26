from odoo import models, fields


class AverigoProductImport(models.TransientModel):
    _name = 'product.import'
    _description = 'Product Import Wizard'
    file = fields.Binary(string="Select File")
    file_type = fields.Selection([('csv', 'CSV'), ('xls', 'XLS / XLSX')],
                                 default='csv')
