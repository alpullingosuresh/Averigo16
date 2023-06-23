from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    branch = fields.Integer(string="BranchID")
