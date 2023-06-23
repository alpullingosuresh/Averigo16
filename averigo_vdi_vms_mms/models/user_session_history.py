from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class UserSessionHistory(models.Model):
    _inherit = 'user.session.history'

    vendsys_failed = fields.Boolean(string='VendSys Failed', default=False)
