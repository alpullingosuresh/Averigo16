from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vms_customer_id = fields.Char(string="VMS Customer")
