from odoo import models, fields
from odoo.addons.base.models.res_partner import _tz_get


class Stockwarehouse(models.Model):
    _inherit = 'stock.warehouse'
    timezone = fields.Selection(_tz_get, string='Timezone', default=lambda self: self._context.get('tz'))
