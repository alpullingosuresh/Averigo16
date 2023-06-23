from odoo import models, fields


class UTMMixin(models.AbstractModel):
    _inherit = 'utm.mixin'

    source_id = fields.Many2one('utm.source', 'Campaign Type',
                                help="This is the source of the link, e.g. Search , another domain, or name of email list")
