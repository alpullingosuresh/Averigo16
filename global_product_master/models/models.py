from odoo import fields, models


class GlobalProductMaster(models.Model):
    _name = 'global.product.master'
    _description = 'Global Product Master'

    name = fields.Char('Product Name', index=True, required=True)
    image = fields.Binary(required=True)
    active = fields.Boolean(string="Active", default=True)
    get_val = fields.Boolean('get_val', default=False)
    type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service')], string='Product Type', default='product',
        required=True)
    upc_ids = fields.One2many('gpm.barcode', 'upc_id', string="UPC Codes",
                              copy=True, required=True)
    product = fields.Char(string='Product Name')
    product_template_image_ids = fields.One2many('product.image',
                                                 'product_tmpl_id',
                                                 string="Extra Product Media",
                                                 copy=True)


class ProductImage(models.Model):
    _name = 'product.image'
    _description = "Product Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    Operator_id = fields.Many2one('res.company', 'Operator')
    product_tmpl_id = fields.Many2one('global.product.master',
                                      "Product Template", index=True)
    embed_code = fields.Char()
    can_image_1024_be_zoomed = fields.Boolean("Can Image 1024 be zoomed")
    first_image = fields.Integer(default=0)


class ProductUPC(models.Model):
    _name = 'gpm.barcode'
    _description = "Global Barcode"
    _rec_name = 'barcode'

    get_val = fields.Boolean('get_val', default=False)
    barcode = fields.Char('UPC Codes', required=True)
    upc_id = fields.Many2one('global.product.master', 'upc_ids', index=True)
