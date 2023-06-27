from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    case_management_ids = fields.One2many(comodel_name="case.management",
                                          inverse_name="partner_id",
                                          string="Related Cases")

    case_management_count = fields.Integer(string="Case count")
    case_management_active_count = fields.Integer(
        string="Case active count")
    case_management_count_string = fields.Char(string="Cases")
    customer_case_count = fields.Integer()
    case_ids = fields.One2many('case.management', 'partner_id',
                               string="Preventive Cases",
                               domain=[("is_preventive", "=", True)])
