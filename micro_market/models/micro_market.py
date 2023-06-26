from odoo import models, fields


class MicroMarketWarehouse(models.Model):
    _name = "stock.warehouse"
    _inherit = ['stock.warehouse', 'mail.thread']
    _description = "Location"
    _order = "name"

    name = fields.Char('Name', index=True, required=True, default=None,
                       tracking=True, size=50)
    partner_id = fields.Many2one('res.partner', 'Customer', default=None,
                                 check_company=True, ondelete='restrict',
                                 copy=False)
    partner_name = fields.Char(string='Customer/Location', store=True)
    code = fields.Char('Short Name', required=True, size=50)
    location_id = fields.Char('Location Id', size=6, tracking=True, copy=False)
    location_type = fields.Selection([
        ('micro_market', 'Micro Market'),
        ('pantry', 'Pantry'),
        ('transit', 'Truck'),
        ('view', 'Warehouse'),
        ('branch', 'Branch')], string='Location Type',
        default='view', index=True, required=True, tracking=True)
    location_type_view = fields.Selection([
        ('micro_market', 'Micro Market'),
        ('pantry', 'Pantry'),
        ('transit', 'Truck'),
        ('view', 'Warehouse'),
        ('branch', 'Branch')], string='Location Type',
        default='view', index=True, required=True, tracking=True, store=True,
        related='location_type')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=5)
    city = fields.Char('City')
    county = fields.Char('County')
    state_id = fields.Many2one('res.country.state', string="State",
                               domain="[('country_id', '=', country_id)]")
    state_name = fields.Char(string="State", store=True)
    country_id = fields.Many2one('res.country', string="Country")
    email = fields.Char('Email', store=True, readonly=False)
    contact_person = fields.Char('Contact Name', store=True, readonly=False)
    operator_own = fields.Boolean()
    uuid = fields.Many2one('uuid.uuid', string='Beacon', tracking=True,
                           domain="[('micro_market_id', '=', False)]",
                           copy=False)
    beacon_major = fields.Char('Beacon Major', tracking=True, copy=False,
                               related='uuid.beacon_major')
    beacon_minor = fields.Char('Beacon Minor', tracking=True, copy=False,
                               related='uuid.beacon_minor')
    merchant_id = fields.Char('Merchant ID', tracking=True, copy=False,
                              related='uuid.merchant_id')
    terminal_id = fields.Char('Terminal ID', tracking=True, copy=False,
                              related='uuid.terminal_id')
    apriva_client_id = fields.Char('Apriva Client ID', tracking=True,
                                   copy=False, related='uuid.apriva_client_id')
    secret_key = fields.Char('Secret Key', copy=False,
                             related='uuid.secret_key')
    catalog_ids = fields.Many2many('product.catalog', string='Product Catalog',
                                   domain="[('operator_id', '=', "
                                          "company_id)]")
    select_catalog_products = fields.Boolean('Select All', default=True)
    product_ids = fields.Many2many('product.product.catalog')
    single_product_ids = fields.Many2many('product.product', 'micro_market_id')
    product_filter_ids = fields.Many2many('product.product', store=True)
    catalog_product_ids = fields.One2many('catalog.micro.market',
                                          'micro_market_id')
    market_product_ids = fields.One2many('product.micro.market',
                                         'micro_market_id',
                                         domain=[
                                             ('is_discontinued', '=', False)],
                                         tracking=True, copy=True)
    check_group = fields.Boolean()
    market_address = fields.Char('Address')
    value = fields.Float('Product Value')
    currency_id = fields.Many2one(related='company_id.currency_id')
    active_date = fields.Date(string='Activated Date',
                              default=fields.Date.today)
    low_stock = fields.Integer(string='Low Stock Products')
    avg_sale = fields.Float(string='Average Sales', digits='Product Price',
                            help='Average sales of current month')
    total_sale = fields.Float(string='Total Sales', digits='Product Price',
                              help='Total sales of current month')
    division_id = fields.Many2one('res.division')
    catalog_length = fields.Integer(string="Count")
    operator_street = fields.Char('Operator Street',
                                  related='company_id.street')
    operator_street2 = fields.Char('Operator Street2',
                                   related='company_id.street2')
    operator_zip = fields.Char('Operator Zip', related='company_id.zip')
    operator_county = fields.Char('Operator County',
                                  related='company_id.county')
    operator_city = fields.Char('Operator City', related='company_id.city')
    operator_state_id = fields.Many2one('res.country.state',
                                        string="Operator Fed. State",
                                        related='company_id.state_id')
    operator_country_id = fields.Many2one('res.country',
                                          string="Operator Country",
                                          related='company_id.country_id')
    customer_street = fields.Char('Customer Street',
                                  related='partner_id.street')
    customer_street2 = fields.Char('Customer Street2',
                                   related='partner_id.street2')
    customer_zip = fields.Char('Customer Zip', related='partner_id.zip')
    customer_county = fields.Char('Customer County',
                                  related='partner_id.county')
    customer_city = fields.Char('Customer City', related='partner_id.city')
    customer_state_id = fields.Many2one('res.country.state',
                                        string="Customer Fed. State",
                                        related='partner_id.state_id')
    customer_country_id = fields.Many2one('res.country',
                                          string="Customer Country",
                                          related='partner_id.country_id')
    have_shipping_customer = fields.Boolean(store=True)
    partner_shipping_id = fields.Many2one('res.partner')
    shipping_customer_street = fields.Char('Shipping Customer Street',
                                           related='partner_shipping_id.street')
    shipping_customer_street2 = fields.Char('Shipping Customer Street2',
                                            related='partner_shipping_id.street2')
    shipping_customer_zip = fields.Char('Shipping Customer Zip',
                                        related='partner_shipping_id.zip')
    shipping_customer_county = fields.Char('Shipping Customer County',
                                           related='partner_shipping_id.county')
    shipping_customer_city = fields.Char('Shipping Customer City',
                                         related='partner_shipping_id.city')
    shipping_customer_state_id = fields.Many2one('res.country.state',
                                                 string="Shipping Customer Fed. State",
                                                 related='partner_shipping_id.state_id')
    shipping_customer_country_id = fields.Many2one('res.country',
                                                   string="Shipping Customer Country",
                                                   related='partner_shipping_id.country_id')
    longitude = fields.Float()
    latitude = fields.Float()
    image = fields.Image(string="Micromarket Image")
    image_128 = fields.Image(string="Micromarket Image_128", related='image',
                             max_width=128, max_height=128)
    catalogs_ids = fields.Many2many('product.catalog', 'market_catalogs_rel')
    internal_notes = fields.Text()
    special_notes = fields.Text(tracking=True)
    current_date = fields.Date(default=fields.Date.today)
    route = fields.Many2one('route.route', tracking=True)
    # frequency_id = fields.Many2one('route.frequency', tracking=True)
    frequency = fields.Many2one('transaction.recurring', tracking=True,
                                copy=False)
    tax = fields.Many2one('account.tax')
    sales_tax = fields.Float(digits='Product Price', tracking=True)
    tax_warning = fields.Text('No sales tax is updated for this Micro Market')
    from_customer = fields.Boolean()
    last_ordered_warehouse = fields.Many2one('stock.warehouse')
    # select_products = fields.Boolean()
    truck_driver = fields.Many2one('hr.employee')
    show_tax_warning = fields.Boolean()
    micro_market_products_count = fields.Integer()
    addl_tax = fields.Boolean(string='Addl.Tax')
    show_tax_rate_1 = fields.Boolean()
    show_tax_rate_2 = fields.Boolean()
    show_tax_rate_3 = fields.Boolean()
    tax_rate_1 = fields.Float('Tax Rate 1')
    tax_rate_2 = fields.Float('Tax Rate 2')
    tax_rate_3 = fields.Float('Tax Rate 3')
    product_category_ids = fields.Many2many('product.category',
                                            'mm_category_rel')
    dom_product_category_ids = fields.Many2many('product.category', store=True)
    enable_tax_rate_1 = fields.Boolean()
    enable_tax_rate_2 = fields.Boolean()
    enable_tax_rate_3 = fields.Boolean()
    partner_readonly = fields.Boolean()


class MicroMarketProduct(models.Model):
    _name = 'product.micro.market'
    _inherit = 'mail.thread'
    _description = 'Micro Market Product'

    """Product Linked to Micro Market"""

    active = fields.Boolean('Active', related='micro_market_id.active')
    product_id = fields.Many2one('product.product', index=True, required=True,
                                 translate=True,
                                 domain="[('type', 'in', ['product', 'consu'])]")
    add_upc = fields.Char()
    upc_ids = fields.Many2many('upc.code.multi', tracking=True, store=True)
    name = fields.Char(store=True, related='product_id.name')
    image = fields.Image(string='Image', related='product_id.image_128')
    image_32 = fields.Image(string='Image_32', related='image', max_width=32,
                            max_height=32)
    image_64 = fields.Image(string='Image_64', related='image', max_width=64,
                            max_height=64)
    catalog_id = fields.Many2one('product.catalog')
    product_code = fields.Char('Product code', store=True,
                               related='product_id.default_code')
    tax_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Sales Tax',
                                  tracking=True)
    categ_id = fields.Many2one('product.category', 'Product Category',
                               store=True, related='product_id.categ_id',
                               index=True)
    list_price = fields.Float('Selling Price', readonly=False,
                              digits='Product Price', tracking=True)
    subsidy = fields.Float('Subsidy', digits='Product Price', tracking=True)
    uom_category = fields.Integer()
    uom_id = fields.Many2one('uom.uom',
                             domain="[('category_id', '=', uom_category)]",
                             tracking=True)
    micro_market_id = fields.Many2one('stock.warehouse', index=True)
    max_qty = fields.Integer(tracking=True, default=1)
    min_qty = fields.Integer(tracking=True, default=1)
    description = fields.Text()
    state = fields.Selection([('stock', 'Stock'), ('low', 'Low')], store=True)
    price_status = fields.Char(store=True)
    quantity = fields.Float('Current Stock', digits='Product Unit of Measure')
    catalog_price = fields.Float(digits='Product Price')
    # product_select = fields.Boolean()
    is_container_tax = fields.Boolean('Container Deposit',
                                      related='product_id.is_container_tax')
    container_deposit_tax = fields.Many2one('account.tax',
                                            domain="[('crv', '=',  True)]",
                                            tracking=True)
    container_deposit_amount = fields.Float('Container Deposit Amount',
                                            digits='Product Price')
    cost_price = fields.Float(related='product_id.standard_price', store=True,
                              digits='Product Price')
    discontinued = fields.Boolean(default=False, store=True)
    eoq = fields.Integer()
    partner_id = fields.Many2one('res.partner', 'Customer/Location', store=True,
                                 related='micro_market_id.partner_id',
                                 ondelete='restrict')
    company_id = fields.Many2one('res.company', store=True,
                                 related='micro_market_id.company_id')
    sales_tax = fields.Float(store=True, related='micro_market_id.sales_tax',
                             digits='Product Price')
    sales_tax_amount = fields.Float(store=True, digits='Product Price')
    discontinued_date = fields.Date()
    discontinued_user = fields.Char(
        help='Name of the user who discontinued the product')
    opening_stock = fields.Float('Opening Stock')
    is_discontinued = fields.Boolean(string="Discontinued")
    info = fields.Text()
    product_last_sales = fields.Integer(store=False)
    tax_rate_percentage_1 = fields.Float('Additional Tax1 %')
    tax_rate_percentage_2 = fields.Float('Additional Tax2 %')
    tax_rate_percentage_3 = fields.Float('Additional Tax3 %')
    tax_rate_1 = fields.Float('Tax Rate 1')
    tax_rate_2 = fields.Float('Tax Rate 2')
    tax_rate_3 = fields.Float('Tax Rate 3')
    enable_tax_rate_1 = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         default='no', tracking=True)
    enable_tax_rate_2 = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         default='no', tracking=True)
    enable_tax_rate_3 = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         default='no', tracking=True)


class MicroMarketCatalog(models.Model):
    _name = 'catalog.micro.market'
    _description = 'Catalog Product in Micro Market'
    """Product from Selected Catalog"""

    micro_market_id = fields.Many2one('stock.warehouse')
    catalog_id = fields.Many2one('product.catalog')
    product_id = fields.Many2one('product.product')
    select_product = fields.Boolean('Add', default=True)
    name = fields.Char()
    image = fields.Image()
    product_code = fields.Char('Product code')
    tax_status = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  'Taxable Status')
    categ_id = fields.Many2one('product.category', 'Product Category')
    list_price = fields.Float('Public Price', readonly=False,
                              digits='Product Price')
    upc_ids = fields.Many2many('upc.code.multi')
    uom_id = fields.Many2one('uom.uom')
    max_qty = fields.Integer()
    min_qty = fields.Integer()


class CustomerMicroMarket(models.Model):
    _inherit = 'res.partner'

    total_mm = fields.Integer(string="Total MM")


class MarketMultipleUom(models.Model):
    _name = 'product.market.uom'
    _description = 'Add Multiple UOM Products to Micro Market'
    """Add Multiple UOM Products to MM"""

    micro_market_id = fields.Many2one('stock.warehouse')
    product_id = fields.Many2one('product.product',
                                 domain="[('multiple_uom', '=', True)]")
    uom_id = fields.Many2one('uom.uom', string='UOM')
    uom_ids = fields.Many2many('uom.uom', string='Product UOMs')
    multiple_uom_ids = fields.Many2many('multiple.uom')
    multiple_uom_id = fields.Many2one('multiple.uom')
    add_product = fields.Boolean('Add', default=True)
    add_to_mm = fields.Boolean('Add To MM')
