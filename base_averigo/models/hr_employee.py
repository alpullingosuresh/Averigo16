from odoo import models, fields


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    first_name = fields.Char(tracking=True)
    last_name = fields.Char(tracking=True)
    employee_code = fields.Char()
    division_id = fields.Many2one('res.division', String='Work Address')
    street = fields.Char(related='address_home_id.street', readonly=False,
                         store=True)
    street2 = fields.Char(related='address_home_id.street2', readonly=False,
                          store=True)
    city = fields.Char(related='address_home_id.city', readonly=False,
                       store=True)
    zip = fields.Char(related='address_home_id.zip', readonly=False, store=True)
    state_id = fields.Many2one('res.country.state',
                               related='address_home_id.state_id',
                               readonly=False, store=True)
