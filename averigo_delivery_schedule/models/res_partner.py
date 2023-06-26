from odoo import fields, models, api


class DeliverySmartAction(models.Model):
    _inherit = 'res.partner'

    delivery_schedule_count = fields.Integer(
        string="Delivery Schedule Count", )
