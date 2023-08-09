from odoo import models, fields


class ProposalActionWizard(models.TransientModel):
    _name = "proposal.action.wizard"

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    crm = fields.Many2one('crm.lead')
    date = fields.Datetime('Date', default=fields.Datetime.now)
