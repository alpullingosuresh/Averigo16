from odoo import fields, models


class Route(models.Model):
    _name = 'route.route'
    _description = 'Delivery Route'
    """To create Route"""

    name = fields.Char()
    desc = fields.Char()
    truck_id = fields.Many2one('stock.warehouse',
                               domain="[('location_type', '=', 'transit')]")
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse',
                                   domain="[('location_type', '=', 'view')]")
    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id,
                                  readonly=True)


class RouteFrequency(models.Model):
    _name = 'route.frequency'
    _description = 'Delivery Route Frequency'
    """To create Route Frequency"""

    name = fields.Char()
    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id,
                                  readonly=True, invisible=True)
    color = fields.Char()
