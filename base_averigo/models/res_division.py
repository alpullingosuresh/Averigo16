from odoo import models, fields


class ResDivision(models.Model):
    _name = 'res.division'
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Branch"

    name = fields.Char(string="Branch Name", required=True)
    company_id = fields.Many2one('res.company', 'Operator', required=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True)
    zip = fields.Char(size=5)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    county = fields.Char()
    state_id = fields.Many2one('res.country.state', string="Fed. State")
    country_id = fields.Many2one('res.country', string="Country")
    division_address = fields.Char(string="Address")
    primary_division = fields.Boolean(string="Primary Branch")


class PartnerDeleteWizard(models.TransientModel):
    _name = 'partner.delete.wizard'
    _description = "Partner Delete Wizard"

    partner_ids = fields.Many2many('res.partner', string="Partners")
