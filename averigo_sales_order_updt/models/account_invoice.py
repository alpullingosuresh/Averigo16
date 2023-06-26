from odoo import models, fields, api


class AccountMoveInvoiceInherit(models.Model):
    _inherit = 'account.move'

    country_id = fields.Many2one('res.country')
    shp_state_id = fields.Many2one('res.country.state',
                                   domain="[('country_id', '=?', country_id)]",
                                   string="Ship to State")
