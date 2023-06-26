from odoo import api, fields, models


class CreateMultiProduct(models.Model):
    _name = 'create.products'
    _description = 'Temporary, Create Multiple Products From GPM'
    _rec_name = 'name'

    upc_code = fields.Many2one('global.product.master', string='UPC Code')
    products_ids = fields.Many2one('create.bulk.products')
    upc_ids = fields.One2many('barcode.barcode', 'upc_id',
                              string="Add More UPC")
    create_product_id = fields.Many2many('global.product.master')
    get_barcode = fields.Boolean('get_val', default=False)
    res_location = fields.Many2one('stock.warehouse', 'Primary Location')
    primary_location = fields.Many2one('stock.location', 'Primary Location')
    type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service')], default='product')
    product_code = fields.Char('Product Code')
    name = fields.Char('Product Name')
    standard_price = fields.Float('Cost')
    list_price_1 = fields.Float('List Price')

    operator_id = fields.Many2one(
        'res.company', 'Operator', required=True, index=True,
        default=lambda self: self.env.company)
    categ_id = fields.Many2one(
        'product.category', 'Category',
        help="Select category for the current product")
    container_tax = fields.Many2one('account.tax', 'Container Tax')
    tax_status = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  string='Taxable', default='yes')
    image_1920 = fields.Binary('Images')
    is_container_deposit = fields.Boolean('Deposit Tax', default=False)
    upc_code_scan = fields.Char('UPC Code')
    uom_id = fields.Many2one(
        'uom.uom', ' Base UoM',  required=True)


class NewClass(models.Model):
    _name = 'create.bulk.products'
    _description = 'Bulk Product'

    product_ids = fields.One2many('create.products', 'products_ids')
    operator_id = fields.Many2one(
        'res.company', 'Operator', required=True, index=True,
        default=lambda self: self.env.company)
    name = fields.Char()
    scan_from_gpm = fields.Boolean(default=False)
