from odoo import models, fields


class ProductCatalog(models.Model):
    _name = 'product.catalog'
    _rec_name = 'name'
    _description = 'Product Catalog'
    """Product Catalog Creation"""

    name = fields.Char(string='Product Catalog', required=True)
    active = fields.Boolean(string="Active", default=True)
    product_ids = fields.Many2many('product.product',
                                   domain="[('type', 'in', ['product', "
                                          "'consu'])]", string='Products')
    product_filter_ids = fields.Many2many('product.product',
                                          'catalog_filter_id', store=True)
    catalog_product_ids = fields.One2many('product.product.catalog',
                                          'catalog_id', copy=True)
    micro_market_ids = fields.Many2many('stock.warehouse')
    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id,
                                  readonly=True)
    category_ids = fields.Many2many('product.category', string='Category')
    multiple_uom_products = fields.One2many('product.uom', 'catalog_id')
    product_select_uom_length = fields.Integer(string="Count", store=True)
    catalog_type = fields.Selection([
        ('micro_market', 'Micro Market'),
        ('customer', 'Customer')], string='Catalog Type',
        default='micro_market', required=True, tracking=True)
    show_wizard = fields.Boolean(store=True)
    changed_catalog_ids = fields.Many2many('product.product.catalog')


class Product(models.Model):
    _inherit = 'product.product'

    catalog_ids = fields.Many2many('product.catalog', string='Product Catalog')
    catalog_filter_id = fields.Many2one('product.catalog')
    micro_market_id = fields.Many2one('stock.warehouse')


class ProductCatalogProduct(models.Model):
    _name = 'product.product.catalog'
    _inherit = 'mail.thread'
    _rec_name = 'name'
    _description = 'Products in Catalog'
    """Product Linked to Product Catalog"""

    product_id = fields.Many2one('product.product', index=True, required=True,
                                 translate=True,
                                 domain="[('type', 'in', ['product', 'consu'])]")
    name = fields.Char()
    product_code = fields.Char('Product code')
    tax_status = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  'Taxable Status')
    categ_id = fields.Many2one('product.category', 'Product Category',
                               store=True, related='product_id.categ_id')
    upc_ids = fields.Many2many('upc.code.multi', tracking=True, store=True)
    image = fields.Image(related='product_id.image_1920')
    image_catalog = fields.Image(max_width=32, max_height=32,
                                 related='product_id.image_1920')
    list_price = fields.Float('Public Price', readonly=False,
                              digits='Product Price', tracking=True)
    uom_category = fields.Integer()
    uom_id = fields.Many2one('uom.uom', tracking=True)
    uom_ids = fields.Many2many('uom.uom', string='UOMs', store=True)
    catalog_id = fields.Many2one('product.catalog')
    description = fields.Text('Description', translate=True)
    specification = fields.Text('Specifications', translate=True)
    max_qty = fields.Integer(tracking=True, default=1)
    min_qty = fields.Integer(tracking=True, default=1)


class CatalogMultipleUom(models.Model):
    _name = 'product.uom'
    _description = 'Add Multiple UOM Products to Catalog'
    """Add Multiple UOM Products to Catalog"""

    catalog_id = fields.Many2one('product.catalog')
    product_id = fields.Many2one('product.product',
                                 domain="[('multiple_uom', '=', True)]")
    uom_id = fields.Many2one('uom.uom', string='UOM')
    uom_ids = fields.Many2many('uom.uom', string='Product UOMs')
    multiple_uom_ids = fields.Many2many('multiple.uom')
    multiple_uom_id = fields.Many2one('multiple.uom')
    add_product = fields.Boolean('Add', default=True)
    add_to_mm = fields.Boolean('Add To MM')
    micro_market_ids = fields.Many2many('stock.warehouse')
