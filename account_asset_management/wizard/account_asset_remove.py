import logging

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class AccountAssetRemove(models.TransientModel):
    _name = "account.asset.remove"
    _description = "Remove Asset"

    date_remove = fields.Date(string="Asset Removal Date", required=True,
                              default=fields.Date.today,
                              help="Removal date must be after the last "
                                   "posted entry in case of early removal", )
    force_date = fields.Date(string="Force accounting date")
    sale_value = fields.Float(string="Sale Value",
                              default=lambda self: self._default_sale_value())
    account_sale_id = fields.Many2one(comodel_name="account.account",
                                      string="Asset Sale Account",
                                      domain=[("deprecated", "=", False)],
                                      default=lambda self: self._default_account_sale_id(), )
    account_plus_value_id = fields.Many2one(comodel_name="account.account",
                                            string="Plus-Value Account",
                                            domain=[
                                                ("deprecated", "=", False)],
                                            default=lambda self: self._default_account_plus_value_id(), )
    account_min_value_id = fields.Many2one(comodel_name="account.account",
                                           string="Min-Value Account",
                                           domain=[("deprecated", "=", False)],
                                           default=lambda
                                               self: self._default_account_min_value_id(), )
    account_residual_value_id = fields.Many2one(comodel_name="account.account",
                                                string="Residual Value Account",
                                                domain=[("deprecated", "=",
                                                         False)],
                                                default=lambda self: self._default_account_residual_value_id(), )
    posting_regime = fields.Selection(
        selection=lambda self: self._selection_posting_regime(),
        string="Removal Entry Policy", required=True,
        default=lambda self: self._get_posting_regime(),
        help="Removal Entry Policy \n"
             "  * Residual Value: The non-depreciated value will be "
             "posted on the 'Residual Value Account' \n"
             "  * Gain/Loss on Sale: The Gain or Loss will be posted on "
             "the 'Plus-Value Account' or 'Min-Value Account' ", )
    note = fields.Text("Notes")
