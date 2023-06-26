from odoo import models, fields, api


class InvoiceSign(models.Model):
    _inherit = 'account.move'

    signature = fields.Binary('Signature', copy=False,
                              attachment=True, )
