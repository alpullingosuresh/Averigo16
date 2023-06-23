from odoo import models, fields


class VendorListLine(models.TransientModel):
    _name = 'vendor.list.line'

    vendor_no = fields.Char(string="Vendor #")
    vendor_id = fields.Many2one('res.partner')
    vendor_name = fields.Char(string="Vendor Name")
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    state = fields.Char()
    country = fields.Char()
    address = fields.Text(string="Address", store=True)
    contact_name = fields.Char(string="Contact Name")
    contact_phone = fields.Char(string="Contact Phone #")
    credit_limit = fields.Monetary(string="Credit Limit",
                                   currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id)
    terms_id = fields.Many2one(
        related='vendor_id.property_supplier_payment_term_id')
    terms = fields.Char(string="Terms", store=True, related='terms_id.name')
    report_id = fields.Many2one('vendor.list.report')


class VendorListReport(models.TransientModel):
    _name = 'vendor.list.report'

    name = fields.Char()
    active_status = fields.Selection(
        [('active', 'Active'), ('archived', 'Archived')])
    is_1099 = fields.Boolean(string="1099 Vendor")
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id)
    report_lines = fields.One2many('vendor.list.line', 'report_id')
    report_length = fields.Integer(default=0)

