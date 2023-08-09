from odoo import models, fields


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    attachment_view_bool = fields.Char("Preview", store=True)
