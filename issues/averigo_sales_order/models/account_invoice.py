from odoo import fields, models


class AccountMoveInvoice(models.Model):
    _inherit = 'account.move'

    sale_id = fields.Many2one('sale.order', string="Order #")
    is_sale = fields.Boolean(help="This is sale invoice")
    is_refund = fields.Boolean(help="This is refund invoice")
    is_service_invoice = fields.Boolean(help="This is a service invoice")
    amount_total_view_sign = fields.Float(digits='Product Price')
    route_id = fields.Many2one('route.route', string='Route')
    partner_invoice_id = fields.Many2one('res.partner',
                                         string='Billing Address',
                                         readonly=True,
                                         states={'draft': [('readonly', False)],
                                                 'sent': [('readonly', False)],
                                                 'sale': [('readonly', False)]},
                                         domain="[('id', 'in', partner_invoice_ids)]")
    partner_invoice_ids = fields.Many2many('res.partner', 'partners_rel',
                                           'invoice_id', 'partner_invoice_id')
    partner_shipping_ids = fields.Many2many('res.partner', 'partner_rel',
                                            'shipping_id',
                                            'partner_shipping_id')
    inv_street = fields.Char('Bill to Street',
                             related='partner_invoice_id.street')
    inv_street2 = fields.Char('Bill to Street2',
                              related='partner_invoice_id.street2')
    inv_zip = fields.Char('Bill to Zip', size=5,
                          related='partner_invoice_id.zip')
    inv_city = fields.Char('Bill to City', related='partner_invoice_id.city')
    inv_county = fields.Char('Bill to County',
                             related='partner_invoice_id.county')
    inv_state_id = fields.Many2one('res.country.state', string="Bill to State",
                                   related='partner_invoice_id.state_id', )
    shp_street = fields.Char('Ship to Street')
    shp_street2 = fields.Char('Ship to Street2')
    shp_zip = fields.Char('Ship to Zip', size=5)
    shp_city = fields.Char('Ship to City')
    shp_county = fields.Char('Ship to County')
    shp_state_id = fields.Many2one('res.country.state', string="Ship to State")
    change_address_wizard = fields.Boolean(string='Change address',
                                           default=True)
    tax_type = fields.Selection(
        [('sales', 'Sales Tax'), ('scheduled', 'Scheduled Tax')], 'Tax Type',
        default='sales')
    schedule_tax_id = fields.Many2one('schedule.tax')
    tax_calc = fields.Float()
    direct_invoice = fields.Boolean()
    inv_product_ids = fields.Many2many('product.product')
    is_return_picking = fields.Boolean('Returned Picking', store=True,
                                       help="This is used to give domain in sales return picking")
    packing_slip_id = fields.Many2one('stock.picking.batch')


class AccountMoveLineInvoice(models.Model):
    _inherit = 'account.move.line'
    _description = "Invoice/BIll Line"

    sale_line_id = fields.Many2one('sale.order.line', 'Sale Line')


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    user_id = fields.Many2one('res.users', string='Owner', readonly=False,
                              default=lambda self: self.env.user.id)
