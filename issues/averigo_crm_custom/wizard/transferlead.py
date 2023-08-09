from odoo import models, fields


class TransferLeadWizard(models.TransientModel):
    _name = "transfer.lead.wizard"

    company_id = fields.Many2one('res.company', string="Operator")
