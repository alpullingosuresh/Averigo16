import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# List of move's fields that can't be modified if move is linked
# with a depreciation line
FIELDS_AFFECTS_ASSET_MOVE = {"journal_id", "date"}
# List of move line's fields that can't be modified if move is linked
# with a depreciation line
FIELDS_AFFECTS_ASSET_MOVE_LINE = {
    "credit",
    "debit",
    "account_id",
    "journal_id",
    "date",
    "asset_profile_id",
    "asset_id",
}


class AccountMove(models.Model):
    _inherit = "account.move"

    machine_bill = fields.Boolean('Equipment Bill', default=False)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    asset_profile_id = fields.Many2one(comodel_name="account.asset.profile",
                                       string="Asset Profile")
    asset_id = fields.Many2one(comodel_name="account.asset", string="Asset",
                               ondelete="restrict")
    asset_code = fields.Char('Asset Code')
    serial_no = fields.Char('Serial No')
