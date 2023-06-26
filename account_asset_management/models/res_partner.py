from odoo import api, fields, models, _


class ResPartnerMachine(models.Model):
    _inherit = "res.partner"

    machine_ids = fields.One2many('account.asset', 'location_partner_id',
                                  string="Equipment",
                                  domain=[('location_type', '=', 'order')])
    machine_count = fields.Integer(compute='_compute_machine_count')
