from odoo import models, fields
import odoo.addons.decimal_precision as dp

class CustomerSaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "Quotation/Order"

    is_closed = fields.Boolean('is closed', invisible=True)

    kam = fields.Many2one('hr.employee', string='Accounts Manager')
    contact = fields.Char('Contact Name')
    division_id = fields.Many2one('res.division', string="Division")
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 readonly=True,
                                 states={'draft': [('readonly', False)],
                                         'sent': [
                                             ('readonly', False)]},
                                 required=True, change_default=True, index=True,
                                 tracking=1,
                                 domain="[('type', 'in', ['contact', 'portal']),('is_customer', '=', True)]")
    # domain="[('parent_id','=',id),('is_customer', '=', True)]")
    warehouse_id = fields.Many2one(
        'stock.warehouse', 'Location',
        domain="[('location_type', '=', 'view'), ('is_parts_warehouse', '=', False)]",
        required=True, readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, check_company=True)
    partner_invoice_id = fields.Many2one('res.partner',
                                         string='Billing Address',
                                         readonly=True,
                                         states={'draft': [('readonly', False)],
                                                 'sent': [('readonly', False)],
                                                 'sale': [('readonly', False)]},
                                         domain="[('id', 'in', partner_invoice_ids)]")
    partner_invoice_ids = fields.Many2many(
        'res.partner','partner_id')
    partner_shipping_id = fields.Many2one('res.partner',
                                          string='Shipping Address',
                                          readonly=True,
                                          states={
                                              'draft': [('readonly', False)],
                                              'sent': [('readonly', False)],
                                              'sale': [('readonly', False)]},
                                          domain="[('id', 'in', partner_shipping_ids)]", )
    partner_shipping_ids = fields.Many2many(
        'res.partner', )
    purchase_count = fields.Integer()
    delivery_date = fields.Date(string='Delivery Date')
    portal_delivery_date = fields.Datetime(string='Delivery Date')
    drop_ship = fields.Boolean('Drop shipping')
    drop_partner_id = fields.Many2one('res.partner', string='Vendor')
    # cus_product_order = fields.One2many('customer.product.order', 'cus_order_id')
    # add_all = fields.Boolean(default=True)
    cus_product_associate = fields.Boolean(
        store=True, default=True)
    desc_check = fields.Boolean()
    cus_product_assoc_ids = fields.Many2many(
        'product.product', 'cus_product_assoc_rel', string='Customer Products')
    cus_product_filter_ids = fields.Many2many(
        'product.product')
    total_discount = fields.Float()
    total_container_deposit = fields.Float()
    container_deposit_view = fields.Float()
    total_weight = fields.Float()
    shipping_handling = fields.Float()
    insurance = fields.Float()
    department_id = fields.Many2one('hr.department')
    ship_via = fields.Many2one('ship.via', string='Ship Via')
    fob = fields.Selection(
        [('origin', 'Origin'), ('dest', 'Destination')], 'FOB')
    note = fields.Text()
    message = fields.Text()
    notes = fields.Text()
    hold_reason = fields.Many2one('hold.reason')
    closed_reason = fields.Many2one('closed.reason')
    route_id = fields.Many2one('route.route', string='Route')
    inv_street = fields.Char(
        'Bill to Street', related='partner_invoice_id.street')
    inv_street2 = fields.Char(
        'Bill to Street2', related='partner_invoice_id.street2')
    inv_zip = fields.Char('Bill to Zip', size=5,
                          related='partner_invoice_id.zip')
    inv_city = fields.Char('Bill to City', related='partner_invoice_id.city')
    inv_county = fields.Char(
        'Bill to County', related='partner_invoice_id.county')
    inv_state_id = fields.Many2one('res.country.state', string="Bill to State",
                                   domain="[('country_id', '=?', country_id)]",
                                   related='partner_invoice_id.state_id')
    shp_street = fields.Char('Ship to Street',
                             related='partner_shipping_id.street')
    shp_street2 = fields.Char('Ship to Street2',
                              related='partner_shipping_id.street2')
    shp_zip = fields.Char('Ship to Zip', size=5,
                          related='partner_shipping_id.zip')
    shp_city = fields.Char('Ship to City', related='partner_shipping_id.city')
    shp_county = fields.Char('Ship to County',
                             related='partner_shipping_id.county')
    shp_state_id = fields.Many2one('res.country.state', string="Ship to State",
                                   ondelete='restrict',
                                   domain="[('country_id', '=?', country_id)]",
                                   related='partner_shipping_id.state_id')
    country_id = fields.Many2one(
        'res.country', string="Ship to Country")
    drop_location_id = fields.Many2one(
        'drop.location', string='Drop Off Location')
    message_len = fields.Integer(
        'Message Length')
    portal_order_view = fields.Boolean(default=False)
    total_qty = fields.Integer('Total Quantity')
    portal_view = fields.Boolean(default=False)
    route_truck_driver = fields.Char()
    tax_calc = fields.Float()
    tax_amount_view = fields.Float(digits='Product Price')
    total_discount_view = fields.Float()
    po_no = fields.Char('PO #')
    sale_po_date = fields.Date('PO Date')
    sell_all_item = fields.Boolean(string="Sell All Products")
    contain_service_product = fields.Boolean(
        help="Become true when there is any service product in orderline")
    service_invoiced = fields.Boolean(string="Service Invoiced",
                                      help="Become true when invoice created for service products")
    print = fields.Boolean(string='TO Be Printed')
    customer_user_id = fields.Many2one(
        'res.users', default=lambda self: self.env.user)
    change_address_wizard = fields.Boolean(
        string='Change address', default=True)
    tax_type = fields.Selection(
        [('sales', 'Sales Tax'), ('scheduled', 'Scheduled Tax')], 'Tax Type',
        default='sales')
    schedule_tax_id = fields.Many2one('schedule.tax')
    commitment_date = fields.Date('Delivery Date',
                                  states={'draft': [('readonly', False)],
                                          'sent': [
                                              ('readonly', False)]},
                                  copy=False, readonly=True,
                                  help="This is the delivery date promised to the customer. "
                                       "If set, the delivery order will be scheduled based on "
                                       "this date rather than product lead times.")
    sale_order_state = fields.Selection([
        ('draft', 'Open'),
        ('sent', 'Order Sent'),
        ('sale', 'Confirmed'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, default='draft')
    averigo_sale_order = fields.Boolean(default=True)
    add_button = fields.Boolean('Add')
    invoice_post_status = fields.Boolean("Post Status")
    invoice_id = fields.Many2one('account.move', string='Invoice No')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = "Quotation/Order Line"

    product_code = fields.Char(
        'Product Code', related='product_id.default_code', store=True)
    product_type = fields.Selection(
        related='product_id.product_type', readonly=True)
    bin_location_id = fields.Many2one('stock.location')
    bin_location_filter_ids = fields.Many2many(
        'stock.location')
    product_available_qty = fields.Float('On Hand', digits=dp.get_precision(
        'Product Unit of Measure'))
    tax_status = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], 'Taxable', default='yes')
    unit_price = fields.Float(
        string='Price', required=True, digits=dp.get_precision('Product Price'))
    discount_amount = fields.Float()
    weight = fields.Float('Weight')
    container_deposit_amount = fields.Float('Container Deposit')
    exclude_from_sale_order = fields.Boolean(
        help="Technical field used to exclude some lines from the order_line_ids tab in the form view.")
    tax_price = fields.Float()
    diff_tax_amount = fields.Float()
    diff_container_amount = fields.Float('Diff Container')
    diff_discount = fields.Float('Diff Discount')
    container_amount_unit = fields.Float(
        store=True)
    discount_amount_unit = fields.Float(
        store=True)
    tax_amount_unit = fields.Float(
        store=True)
    product_cost = fields.Float(
        related='product_id.standard_price', string='Product Cost', store=True)
    gross_margin = fields.Float('GM %')
    convert_check = fields.Boolean('convert')
    desc = fields.Text('Description')
    internal_msg = fields.Text('Internal Message')
    sale_uom_ids = fields.Many2many('uom.uom')


class SaleOrderHold(models.Model):
    _name = 'hold.reason'

    name = fields.Char()
    operator_id = fields.Many2one(
        'res.company', string='Operator', index=True,
        default=lambda s: s.env.company.id)


class SaleOrderClosed(models.Model):
    _name = 'closed.reason'

    name = fields.Char()
    operator_id = fields.Many2one(
        'res.company', string='Operator', index=True,
        default=lambda s: s.env.company.id)


class DropOffLocation(models.Model):
    _name = 'drop.location'
    _description = 'Drop Off Location'
    _rec_name = 'desc'
    """Drop Location"""

    operator_id = fields.Many2one(
        'res.company', string='Operator', index=True,
        default=lambda s: s.env.company.id)
    code = fields.Char('Code')
    desc = fields.Char('Location')
    note = fields.Text()


class PickingNotes(models.TransientModel):
    _name = 'picking.notes'

    name = fields.Char('Notes')


class ProductConfirmation(models.TransientModel):
    _name = 'product.confirmation'

    name = fields.Char(default='Product Confirmation')
    # product_ids = fields.Many2many('product.product','product_id' ,string="Product")
    partner_id = fields.Many2one('res.partner', string="Customer")
