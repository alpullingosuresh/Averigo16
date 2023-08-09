from odoo import models, fields


class WonActionWizard(models.TransientModel):
    _name = "won.action.wizard"

    crm_id = fields.Many2one('crm.lead')
    crm_stages = fields.Selection(
        [('new', 'New'), ('site_survey', 'Site Survey'),
         ('proposal', 'Proposal'), ('agreement', 'Agreement'),
         ('sow', 'SOW')], 'Stages', required=True)
