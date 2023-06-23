from odoo import models, fields


class AdditionalTax(models.Model):
    _name = "additional.tax"
    _inherit = 'mail.thread'
    _description = 'Additional Tax'

    """Additional Tax"""

    name = fields.Char(default='Additional Taxes')
    operator_id = fields.Many2one('res.company',
                                  default=lambda s: s.env.company.id)
    additional_tax_label_1 = fields.Char('Additional Tax Label 1')
    additional_tax_label_2 = fields.Char('Additional Tax Label 2')
    additional_tax_label_3 = fields.Char('Additional Tax Label 3')
    tax_rate_1 = fields.Float('Tax Rate')
    tax_rate_2 = fields.Float('Tax Rate')
    tax_rate_3 = fields.Float('Tax Rate')
