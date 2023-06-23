from odoo import fields, models


class UserSessionHistory(models.Model):
    _name = 'user.session.history'
    _rec_name = 'sequence'
    _description = "App User Session History"
    _order = 'create_date desc'

    sequence = fields.Char(string="Sequence")
    user_id = fields.Many2one('res.app.users', string="User")
    operator_id = fields.Many2one('res.company', string="Operator Name")
    location_id = fields.Many2one('res.partner', string="Location Name")
    micro_market_id = fields.Many2one('stock.warehouse',
                                      string="Micromarket Name")
    session_date = fields.Datetime(string="Login Date & Time")
    purchase_qty = fields.Integer(string="Purchase Quantity")
    purchase_value = fields.Float(string="Purchase Value")
    product_list = fields.One2many('session.product.list', 'session_id',
                                   string="Product Lists")
    move_id = fields.Many2one('account.move')
    tax_amount = fields.Float(string="Tax Amount")
    crv_tax = fields.Float(string="Container Deposit Amount")
    payment_method = fields.Char(string="Payment Method")
    card_last = fields.Char(string="Card Last")
    total_trans_amount = fields.Float()
    total_crv_amount = fields.Float()
    total_sales_amount = fields.Float()
    uniqueidentifier = fields.Char()
    room_no = fields.Char()
    membership_number = fields.Char("Memership Number")
    hosttransactionid = fields.Char()
    processstatus = fields.Char()
    cash_amount = fields.Float()


class SessionProductList(models.Model):
    _name = 'session.product.list'
    _description = 'Session Products List'

    session_id = fields.Many2one('user.session.history', string="Session ID")
    product_id = fields.Many2one('product.product', string="Product")
    qty = fields.Integer(string="Quantity")
    product_uom_id = fields.Many2one('uom.uom',
                                     string='Unit of Measure', readonly=True)
    price = fields.Float(string="Price")
    net_price = fields.Float(string="Net")
    tax_amount = fields.Float(string="Tax Amount")
    crv_tax = fields.Float(string="Container Deposit Amount")
    featured = fields.Char()
    list_price = fields.Float(string="List Price")
    special = fields.Char()
    user_type = fields.Char()
