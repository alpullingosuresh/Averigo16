from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_manager = fields.Many2one('hr.employee')
    contact_fname = fields.Char('Contact First Name')
    contact_lname = fields.Char('Contact Last Name')
    credit_limit = fields.Float('Credit Limit')
    return_period = fields.Integer('Return Period')
    days = fields.Char(default='days')
    buy_all = fields.Boolean('Buy All Products', default=True)
    vendor_approve = fields.Boolean('Vendor Approved', default=True)
    vendor_1099 = fields.Boolean('1099 Vendor', default=False)
    customer_id = fields.Char('Customer #', default=False)
    federal_tax = fields.Char('Federal Tax Id')
    check_memo = fields.Text('Check Memo')
