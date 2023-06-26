from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountAssetLine(models.Model):
    _name = "account.asset.line"
    _description = "Asset depreciation table line"
    _order = "type, line_date"

    name = fields.Char(string="Depreciation Name", size=64, readonly=True)
    asset_id = fields.Many2one(comodel_name="account.asset", string="Asset",
                               required=True, ondelete="cascade")
    previous_id = fields.Many2one(comodel_name="account.asset.line",
                                  string="Previous Depreciation Line",
                                  readonly=True, )
    parent_state = fields.Selection(related="asset_id.state",
                                    string="State of Asset", readonly=True)
    depreciation_base = fields.Monetary(related="asset_id.depreciation_base",
                                        string="Depreciation Base",
                                        readonly=True)
    amount = fields.Monetary(string="Amount", digits="Account", required=True)
    remaining_value = fields.Monetary(digits="Account",
                                      string="Next Period Depreciation",
                                      store=True, )
    depreciated_value = fields.Monetary(digits="Account",
                                        string="Amount Already Depreciated",
                                        store=True, )
    line_date = fields.Date(string="Date", required=True)
    line_days = fields.Integer(string="Days", readonly=True)
    move_id = fields.Many2one(comodel_name="account.move",
                              string="Depreciation Entry", readonly=True)
    move_check = fields.Boolean(string="Posted",
                                store=True)
    type = fields.Selection(
        selection=[("create", "Depreciation Base"),
                   ("depreciate", "Depreciation"),
                   ("remove", "Asset Removal"), ],
        readonly=True, default="depreciate", )
    init_entry = fields.Boolean(string="Initial Balance Entry",
                                help="Set this flag for entries of previous fiscal years "
                                     "for which Odoo has not generated accounting entries.", )
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 required=True, readonly=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  related="company_id.currency_id",
                                  string="Company Currency", store=True,
                                  readonly=True, )
