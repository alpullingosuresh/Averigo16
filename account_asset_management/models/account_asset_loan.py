from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountLoanLine(models.Model):
    _name = "account.loan.line"
    _description = "Asset Loan Table Line"
    _order = "type, line_date"

    name = fields.Char(string="Loan Name", size=64, readonly=True)
    asset_id = fields.Many2one(comodel_name="account.asset",
                               string="Equipment", required=True,
                               ondelete="cascade")
    previous_id = fields.Many2one(comodel_name="account.loan.line",
                                  string="Previous Loan Line",
                                  readonly=True, )
    parent_state = fields.Selection(related="asset_id.state",
                                    string="State of Equipment", readonly=True)
    loan_base = fields.Float(related="asset_id.loan_base", string="Loan Base",
                             readonly=True)
    amount = fields.Float(string="Loan Amount", digits="Account",
                          required=True)
    remaining_value = fields.Float(digits="Account",
                                   string="Next Period Depreciation",
                                   store=True, )
    loan_value = fields.Float(digits="Account", string="Loan Already Paid",
                              store=True)
    line_date = fields.Date(string="Date", required=True)
    line_days = fields.Integer(string="Days", readonly=True)
    move_id = fields.Many2one(comodel_name="account.move", string="Loan Entry",
                              readonly=True)
    move_check = fields.Boolean(string="Entry Posted", store=True)
    type = fields.Selection(
        selection=[("create", "Depreciation Base"), ("loan", "Loan"),
                   ("remove", "Asset Removal"), ],
        readonly=True, default="loan")
    init_entry = fields.Boolean(string="Initial Balance Entry",
                                help="Set this flag for entries of previous fiscal years "
                                     "for which Odoo has not generated accounting entries.", )
    payment_id = fields.Many2one('account.payment')
