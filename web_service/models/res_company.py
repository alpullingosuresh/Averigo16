from odoo import models, fields
from odoo.addons.base.models.res_partner import _tz_get


class ResCompany(models.Model):
    _inherit = 'res.company'

    first_name = fields.Char()
    last_name = fields.Char()
    nick_name = fields.Char()
    enable_sms = fields.Boolean()
    pos_password = fields.Char()
    enable_newsletter = fields.Boolean()
    timezone = fields.Selection(_tz_get, string='Timezone', default=lambda self: self._context.get('tz'))


