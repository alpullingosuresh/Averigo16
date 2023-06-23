from odoo import models, fields


class ResDivision(models.Model):
    _inherit = 'res.division'

    vms_credential = fields.Many2one('vms.credentials',
                                     string="VMS Credential")
    enable_sync = fields.Boolean(string="VMS Sync", default=True,
                                 help="If turned off, data of this branch will"
                                      " not be synced with VMS")
    vms_branch_id = fields.Char(string="VMS Branch ID",
                                help="Add VMS Branch ID if specified by VMS")
