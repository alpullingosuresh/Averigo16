from odoo import models, fields


class CustomerSaleOrder(models.Model):
    _inherit = 'sale.order'

    associated_product = fields.Boolean(string='Add Associated Products')
    total_product_quantity = fields.Integer(string='Total Quantity',
                                            readonly='True')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    asso_products = fields.Boolean()


class MultipleProducUoM(models.Model):
    _inherit = 'multiple.uom'

    name = fields.Char(string="Name", reqired=True)
