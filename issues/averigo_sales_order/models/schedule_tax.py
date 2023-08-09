from odoo import models, fields


class ScheduleTax(models.Model):
    _name = 'schedule.tax'
    _inherit = 'mail.thread'
    _description = 'Scheduled Tax'

    """Scheduled Tax"""

    name = fields.Char()
    operator_id = fields.Many2one('res.company',
                                  default=lambda s: s.env.company.id)
    country_id = fields.Many2one('res.country', string="Country")
    zip = fields.Char('Zip', size=5, tracking=True)
    city = fields.Char('City', tracking=True)
    county = fields.Char('County', tracking=True)
    state_id = fields.Many2one('res.country.state', string="State",
                               domain="[('country_id', '=', country_id)]",
                               tracking=True)
    state_percentage = fields.Float(string="State %", tracking=True)
    city_percentage = fields.Float(string="City %", tracking=True)
    county_percentage = fields.Float(string="County %", tracking=True)
    excise_percentage = fields.Float(string="Excise %", tracking=True)
    total_tax = fields.Float(string="Total Tax %", store=True)
