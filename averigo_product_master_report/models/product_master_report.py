from odoo import fields, models


class ProductMasterReport(models.TransientModel):
    _name = 'product.master.report'
    _description = "Product Master Report"

    location_type = fields.Selection([
        ('Micro market / Pantry / Warehouse', 'All'),
        ('Warehouse', 'Warehouse'),
        ('Micro market', 'Micro market'),
        ('Pantry', 'Pantry'), ], string='Associated With',
        index=True, tracking=True)
    categ_ids = fields.Many2many('product.category',
                                 string='Product Category')
    # report_length = fields.Integer(compute='_compute_report_length')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
