from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    enable_store_order_export = fields.Boolean(
        string="Enable Store Order Export", default=False)
    last_promise_exported = fields.Char(string="Last Exported Promise Date")
    last_exported_count = fields.Integer(string="Last Exported Count")


class ResMailConfig(models.Model):
    _inherit = 'res.mail.config'

    notification_type = fields.Selection(
        selection_add=[('export_store_order', 'Store Order Export')])
