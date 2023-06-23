
from odoo import models, fields


class UpcChangeHistory(models.Model):
    _name = 'upc.code.history'
    _description = 'UPC Change History'

    note = fields.Char()
    product_id = fields.Many2one('product.template')
    user_id = fields.Many2one('res.users', string="User")
    time = fields.Datetime(string="Time")


class SingleProductMaster(models.Model):
    _inherit = 'product.template'

    upc_change_history = fields.One2many('upc.code.history', 'product_id')

    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True,
        required=True, help="Select category for the current product", tracking=True)
    product_type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service')], string='Product Type', default='product', required=True)

    primary_upc = fields.Char(string='UPC Code')
    upc_code = fields.Many2one('global.product.master', string='GPM UPC Code')
    operator_id = fields.Many2one(
        'res.company', 'Operator', required=True, index=True,
        default=lambda self: self.env.company)
    product_code = fields.Char('Product Code', tracking=True)
    default_code = fields.Char('Product Code', tracking=True)
    tax_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Taxable Status', default='yes')
    list_price_1 = fields.Float('List Price 1', digits='Product Price', tracking=True)
    list_price_2 = fields.Float('List Price 2', digits='Product Price', tracking=True)
    list_price_3 = fields.Float('List Price 3', digits='Product Price', tracking=True)
    sale_acc = fields.Many2one('account.account', 'Sales Account', tracking=True)
    vendor = fields.Many2one('res.partner', 'Preferred Vendor', tracking=True)
    cost_price = fields.Float('Price', digits='Product Price')
    cogs_acc = fields.Many2one('account.account', 'COGS Account', tracking=True)
    inventory_acc = fields.Many2one('account.account', 'Inventory Account', tracking=True)
    res_location = fields.Many2one('stock.warehouse', 'Primary Location')
    primary_location = fields.Many2one('stock.location', 'Primary Location')
    primary_locations = fields.Many2many('stock.location')
    res_partner = fields.Many2one('res.partner', 'Preferred Vendor', tracking=True)
    res_manufacturer = fields.Many2one('res.partner', 'Manufacturer')
    manufacturer = fields.Text(string='Manufacturer', tracking=True)
    product_uom_ids = fields.One2many('multiple.uom', 'uom_template_id', string="Add Multiple UoM",
                                      copy=True, tracking=True)
    upc_ids = fields.One2many('upc.code.multi', 'upc_id', string="UPC Codes", ondelete='cascade', tracking=True,
                              track_visibility='always')
    get_barcode = fields.Boolean('get_val', default=False)
    upc_codes = fields.Many2many('upc.code.multi', string='UPCs for Scanning')
    # litre_type = fields.Float('Litre Type')
    litre_type = fields.Selection([('less_than_750', 'Less than 710 ml'), ('greater_710', 'Greater 710 ml')],
                                  'Litre Type')
    fluid_ounce = fields.Float('Fluid Ounce', digits='Product Price')
    multiple_uom = fields.Boolean('Multiple UoM', default=False)
    is_container_tax = fields.Boolean('Container Deposit', default=False)
    mnp_id = fields.Char('MPN')
    stock_open = fields.Float('Open Stock', tracking=True, digits='Product Unit of Measure')
    reorder_point = fields.Integer('Micromarket Min', default=1, tracking=True)
    reorder_qty = fields.Integer('Micromarket Max', default=1, tracking=True)
    min_qty = fields.Integer('Warehouse Min', default=1, tracking=True)
    max_qty = fields.Integer('Warehouse Max', default=1, tracking=True)
    rate_per_uint = fields.Float('Opening Stock Rate Per Unit', digits='Product Price')
    get_upc_code = fields.Boolean('get_upc_code', default=False)
    is_sugar_tax = fields.Boolean('Sugar Tax', default=False)
    is_container_deposit = fields.Boolean('Deposit Tax', default=False)
    product_image_ids = fields.One2many('extra.image', 'product_tmple_id', string="Extra Product Media",
                                        copy=True)
    last_purchase_date = fields.Date()
    # crv_tax = fields.Float('CRV')
    crv_tax = fields.Many2one('account.tax', string='Container Deposit Tax', domain="[('crv', '=',  True)]",
                              track_visibility='onchange')
    container_deposit_amount = fields.Float('Container Deposit Amount', digits='Product Price')

    type = fields.Selection([

        ('consu', 'Consumable'), ('service', 'Service'), ('product', 'Storable Product')],
        string='Product Type', default='product', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')
    # override standard_price field to copy the price
    standard_price = fields.Float(
        'Cost', copy=True,
        inverse='_set_standard_price', search='_search_standard_price',
        digits='Product Cost', groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the last unit that left the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""")




class ProductUoM(models.Model):
    _name = 'multiple.uom'
    _description = 'Product Multiple UoM'

    uom_template_id = fields.Many2one('product.template', 'UoM', index=True)
    convert_uom = fields.Many2one('uom.uom', 'Convert UoM', required=True)
    quantity = fields.Integer('Quantity')
    standard_price = fields.Float('Cost', digits='Product Cost')
    sale_price_1 = fields.Float('Sales Price 1', digits='Product Price')
    sale_price_2 = fields.Float('Sales Price 2', digits='Product Price')
    sale_price_3 = fields.Float('Sales Price 3', digits='Product Price')


class Barcode(models.Model):
    _name = 'barcode.barcode'
    _description = 'Temporary, to keep multiple UPC While creating bulk product list from GPM'
    _rec_name = 'barcode'

    barcode = fields.Char('UPC')
    get_barcode = fields.Boolean('get_val', default=False)
    upc_id = fields.Many2one('create.products')


class UPCCode(models.Model):
    _name = 'upc.code.multi'
    _description = 'Multiple UPC Code in Operator level'
    _rec_name = 'upc_code_id'

    upc_code_id = fields.Char('UPC Code', tracking=True)
    get_upc_code = fields.Boolean('get_val', default=False)
    upc_id = fields.Many2one('product.template')
    product_company_id = fields.Many2one(related='upc_id.company_id')
    operator_id = fields.Many2one(
        'res.company', 'Operator', required=True, default=lambda self: self.env.company)




class ExtraImages(models.Model):
    _name = 'extra.image'
    _description = 'Multiple images of Product in Operator level'
    _order = 'sequence, id'
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    image_1920 = fields.Image("Image", required=True)
    product_tmple_id = fields.Many2one('product.template', "Product Template", index=True, ondelete='cascade')
    sequence = fields.Integer(default=10, index=True)

