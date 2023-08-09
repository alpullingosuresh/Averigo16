from odoo import models, fields


class ProposalActionWizard(models.TransientModel):
    _name = "previous.state.action.wizard"

    crm_id = fields.Many2one('crm.lead')
