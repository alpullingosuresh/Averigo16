from odoo import models, fields


class PantryWarehouse(models.Model):
    _inherit = "stock.warehouse"

    pantry_product_ids = fields.One2many('product.pantry', 'pantry_id',
                                         tracking=True, copy=True)


class PantryProduct(models.Model):
    _name = 'product.pantry'
    _inherit = 'mail.thread'
    _description = 'Panty Products'

    """Product Linked to Pantry"""

    pantry_id = fields.Many2one('stock.warehouse')
    active = fields.Boolean('Active', related='pantry_id.active')
    product_id = fields.Many2one('product.product', index=True, required=True,
                                 translate=True,
                                 domain="[('type', 'in', ['product', 'consu'])]")
    add_upc = fields.Char()
    upc_ids = fields.Many2many('upc.code.multi', tracking=True, store=True)
    name = fields.Char()
    image = fields.Image(string='Image', related='product_id.image_128')
    image_32 = fields.Image(string='Image_32', related='image', max_width=32,
                            max_height=32)
    image_64 = fields.Image(string='Image_64', related='image', max_width=64,
                            max_height=64)
    catalog_id = fields.Many2one('product.catalog')
    product_code = fields.Char('Product code', store=True,
                               related='product_id.default_code')
    tax_status = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  'Taxable Status', tracking=True)
    categ_id = fields.Many2one('product.category', 'Product Category',
                               store=True, related='product_id.categ_id')
    list_price = fields.Float('Selling Price', readonly=False,
                              digits='Product Price', tracking=True)
    uom_category = fields.Integer()
    uom_id = fields.Many2one('uom.uom',
                             domain="[('category_id', '=', uom_category)]",
                             tracking=True)
    max_qty = fields.Integer(tracking=True, default=1)
    min_qty = fields.Integer(tracking=True, default=1)
    description = fields.Text()
    state = fields.Selection([('stock', 'Stock'), ('low', 'Low')])
    price_status = fields.Char()
    quantity = fields.Float()
    catalog_price = fields.Float()
    select_product = fields.Boolean(default=True)
    is_container_tax = fields.Boolean('Container Deposit',
                                      related='product_id.is_container_tax')
    container_deposit_tax = fields.Many2one('account.tax',
                                            domain="[('crv', '=',  True)]",
                                            related='product_id.crv_tax',
                                            tracking=True)
    cost_price = fields.Float(related='product_id.standard_price')
    partner_id = fields.Many2one('res.partner', 'Customer/Location', store=True,
                                 related='pantry_id.partner_id',
                                 ondelete='restrict')
    company_id = fields.Many2one('res.company', store=True,
                                 related='pantry_id.company_id')
    sales_tax = fields.Float(store=True, related='pantry_id.sales_tax')
    sales_tax_amount = fields.Float(store=True)
    discontinued_date = fields.Date()
    discontinued_user = fields.Char(
        help='Name of the user who discontinued the product')
