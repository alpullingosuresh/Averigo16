from odoo import models, fields


class OTPRegister(models.Model):
    _name = 'otp.register'
    _description = 'Store otp'
    otp = fields.Char('OTP')
    user_id = fields.Many2one('res.app.users', 'User Id')
    create_time = fields.Datetime()


class TokenRegister(models.Model):
    _name = 'token.register'
    _description = 'Store Access Token'
    key = fields.Char('Key')
    user_id = fields.Many2one('res.app.users', 'User Id')
    create_time = fields.Datetime()


class ReconcileJson(models.Model):
    _name = 'reconcile.inventory'
    _description = 'Store Reconcile Json'
    json_data = fields.Text('Json Input')


class ReconcileInventory(models.Model):
    _name = 'reconcile.reconcile'
    _description = 'Store Reconcile Json'
    json_data = fields.Text('Json Input')


class ReconcileUpdate(models.Model):
    _name = 'reconcile.update'
    _description = 'Store Reconcile Json'
    json_data = fields.Text('Json Input')
    posted = fields.Boolean(default=False)


class CheckoutJson(models.Model):
    _name = 'checkout.checkout'
    _description = 'Store Reconcile Json'
    json_data = fields.Text('Json Input')


class CheckoutFailure(models.Model):
    _name = 'checkout.failure'
    _description = 'Store Checkout failure data'
    json_data = fields.Text('Json Input')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    status = fields.Selection([('draft', 'Draft'), ('done', 'Received')],
                              default='draft', copy=False)
