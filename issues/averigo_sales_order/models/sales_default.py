from odoo import fields, models


class SalesDefault(models.Model):
    _name = 'sales.default'
    _inherit = 'mail.thread'
    _description = 'Default Sales'
    """Default value in sales"""

    name = fields.Char(default='Sales Setup')
    desc = fields.Boolean('Hide Description', default=True)
    customer_no_sequence = fields.Boolean('Generate Customer #', tracking=True,
                                          default=True)
    starting_customer_no = fields.Integer('Starting Customer #', tracking=True)
    operator_id = fields.Many2one('res.company',
                                  default=lambda s: s.env.company.id)
    product_subsidy = fields.Many2one('product.product',
                                      string='Subsidy Product')
    product_fuel = fields.Many2one('product.product', string='Fuel Charge')
    product_hazard = fields.Many2one('product.product', string='Hazard Fee')
    exist_customer = fields.Boolean()


class SugarTax(models.Model):
    _name = 'sugar.tax'
    _inherit = 'mail.thread'
    _description = 'Sugar Tax For Product'
    """Sugar Tax For Product"""

    name = fields.Char(default='Sugar Tax')
    operator_id = fields.Many2one('res.company',
                                  default=lambda s: s.env.company.id)
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string="Fed. State")
    county = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    amount = fields.Float()
    percentage = fields.Float()
