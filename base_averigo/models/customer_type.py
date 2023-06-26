from odoo import models, fields


class CustomerType(models.Model):
    _name = 'res.customer.type'
    _rec_name = 'customer_type_name'
    _description = 'Customer Type'

    customer_type_id = fields.Char(size=2, required = True)
    customer_type_name = fields.Char(required = True)
