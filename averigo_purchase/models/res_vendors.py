from odoo import fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'mail.thread', 'mail.activity.mixin']

    is_vendor = fields.Boolean(string="Is Vendor")
    vendor_code = fields.Char(string='Vendor #', copy=False)
    vendor_code_auto = fields.Boolean(copy=False)
    auto_gen_vendor_code = fields.Boolean()
    print_name = fields.Char(string='Print As', size=120)
    purchase_manager = fields.Many2one('hr.employee', related='kam', store=True,
                                       readonly=False)
    kam = fields.Many2one('hr.employee', string="Primary Accounts Manager",
                          store=True,
                          readonly=False)
    ship_via = fields.Many2one('ship.via', string='Ship Via')
    property_supplier_payment_term_id = fields.Many2one('account.payment.term',
                                                        company_dependent=True,
                                                        copy=True,
                                                        string='Vendor Payment Terms',
                                                        help="This payment term will be used instead of the default one for purchase orders and vendor bills")
    property_payment_term_id = fields.Many2one('account.payment.term',
                                               company_dependent=True,
                                               copy=True,
                                               string='Customer Payment Terms',
                                               help="This payment term will be used instead of the default one for sales orders and customer invoices")
    addr_type = fields.Selection(
        [('contact', 'Contact'),
         ('remit', 'Remit to Address'),
         ], string='Address Type',
        default='contact')
    vendor_product_ids = fields.One2many('vendor.product.product',
                                         'res_partner')
    single_product_ids = fields.Many2many('product.product',
                                          'vendor_product_rel')
    vendor_product_filter_ids = fields.Many2many('product.product')
    property_account_payable_id = fields.Many2one('account.account',
                                                  company_dependent=True,
                                                  string="Control",
                                                  domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=True)
    payable_account_id = fields.Many2one('account.account',
                                         domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    vendor_terms_discount_account_id = fields.Many2one('account.account',
                                                       domain="[('deprecated', '=', False)]")
    purchase_discount_account_id = fields.Many2one('account.account',
                                                   domain="[('deprecated', '=', False)]")
    vendor_insurance_account_id = fields.Many2one('account.account',
                                                  domain="[('deprecated', '!=', False)]")
    vendor_advance_account_id = fields.Many2one('account.account',
                                                domain="[('deprecated', '=', False)]")
    vendor_tax_account_id = fields.Many2one('account.account',
                                            domain="[('deprecated', '=', False)]")
    vendor_ship_handling_account_id = fields.Many2one('account.account',
                                                      domain="[('deprecated', '=', False)]")


class VendorProducts(models.Model):
    _name = 'vendor.product.product'
    _description = 'Vendor Product'

    """Product Linked to Vendors"""

    active = fields.Boolean('Active', related='res_partner.active')
    res_partner = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product')
    product_code = fields.Char('Product code', store=True,
                               related='product_id.default_code')
    name = fields.Char(store=True, related='product_id.name')
    vendor_part_code = fields.Char()
    vendor_part_name = fields.Char()
    uom_id = fields.Many2one('uom.uom', store=True, related='product_id.uom_id')
    cost_price = fields.Float(digits='Product Price')
    min_qty = fields.Integer(tracking=True)
    lead_time = fields.Integer()
    lead_unit = fields.Selection([('day', 'Days'), ('week', 'Weeks')],
                                 string='Days/Weeks', default='day')
    product_long_desc = fields.Text()
    tax_status = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], 'Taxable', default='no', tracking=True)
