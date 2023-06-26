from odoo import fields, models


class Purchase(models.Model):
    _inherit = 'purchase.order'
    _description = "Purchase Requisition/Order"

    averigo_purchase = fields.Boolean()
    direct_purchase_order = fields.Boolean()
    to_be_printed = fields.Boolean()
    state = fields.Selection([
        ('draft', 'PR'),
        ('sent', 'PR Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Confirmed'),
        ('done', 'Closed'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft',
        tracking=True)
    due_date = fields.Date('Delivery Date')
    contact = fields.Many2one('res.partner',
                              domain="[('parent_id', '=', partner_id), ('parent_id', '!=', False), "
                                     "('addr_type', '=', 'contact')]")
    purchase_manager = fields.Many2one('hr.employee')
    warehouse_id = fields.Many2one('stock.warehouse', 'Location',
                                   domain="[('location_type', '=', 'view'), ('is_parts_warehouse', '!=', True)]")
    ship_via = fields.Many2one('ship.via', string='Ship Via')
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms',
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    division_id = fields.Many2one('res.division')
    department_id = fields.Many2one('hr.department')
    vendor_street = fields.Char('Vendor Street')
    vendor_street2 = fields.Char('Vendor Street2')
    vendor_zip = fields.Char('Vendor Zip', size=5)
    vendor_city = fields.Char('Vendor City')
    vendor_county = fields.Char('Vendor County')
    vendor_state_id = fields.Many2one('res.country.state',
                                      string="Vendor State")
    vendor_country_id = fields.Many2one('res.country', string="Vendor Country")
    ship_street = fields.Char('Ship To Street')
    ship_street2 = fields.Char('Ship To Street2')
    ship_zip = fields.Char('Ship To Zip', size=5)
    ship_city = fields.Char('Ship To City')
    ship_county = fields.Char('Ship To County')
    ship_state_id = fields.Many2one('res.country.state', string="Ship To State")
    ship_country_id = fields.Many2one('res.country', string="Ship To Country")
    bill_street = fields.Char('Bill To Street')
    bill_street2 = fields.Char('Bill To Street2')
    bill_zip = fields.Char('Bill To Zip', size=5)
    bill_city = fields.Char('Bill To City')
    bill_county = fields.Char('Bill To County')
    bill_state_id = fields.Many2one('res.country.state', string="Bill To State")
    bill_country_id = fields.Many2one('res.country', string="Bill To Country")
    shipping_handling = fields.Float(digits='Product Price')
    insurance = fields.Float(digits='Product Price')
    total_discount = fields.Float(digits='Product Price')
    total_discount_view = fields.Float(digits='Product Price')
    tax_calc = fields.Float(digits='Product Price')
    received = fields.Boolean()
    product_ids = fields.Many2many('product.product','product_product_ids_rel')
    total_container_deposit = fields.Float(digits='Product Price')
    container_deposit_view = fields.Float(digits='Product Price')
    dom_product_ids = fields.Many2many('product.product','product_product_dom_product_ids_rel')
    user_limit_purchase = fields.Boolean()
    preload_msg = fields.Boolean()
    internal_commands = fields.Text()
    tax_amount_view = fields.Float(digits='Product Price')
    sale_line_ids = fields.Many2many('sale.order')
    add_button = fields.Boolean('Add')
    associated_product = fields.Boolean(string='Add Associated Products')


class PurchaseOrderLines(models.Model):
    _inherit = 'purchase.order.line'
    _description = "Requisition/Order Line"

    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
                                  domain="[]")
    product_uom_ids = fields.Many2many('uom.uom')
    discount = fields.Float(digits='Product Price')
    cost_tax = fields.Float('Tax', digits='Product Price')
    tax_status = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], 'Taxable', default='no', tracking=True)
    taxable = fields.Boolean(compute_sudo=True)
    vendor_part_desc = fields.Char()
    container_deposit_amount = fields.Float('Container Deposit',
                                            digits='Product Price')
    diff_container_amount = fields.Float('Diff Container',
                                         digits='Product Price')
    diff_discount = fields.Float('Diff Discount', digits='Product Price')
    diff_tax_amount = fields.Float('Diff Tax', digits='Product Price')
    container_amount_unit = fields.Float(store=True,
                                         digits='Product Price')
    discount_amount_unit = fields.Float(store=True,
                                        digits='Product Price')
    tax_amount_unit = fields.Float(store=True,
                                   digits='Product Price')
    price_unit = fields.Float(string='Unit Price', required=True,
                              digits='Product Cost')
    active = fields.Boolean(default=True,
                            help="Set active to false to hide the orderline.")
