from odoo import _, fields, models


class AccountAssetCompute(models.TransientModel):
    _name = "account.asset.compute"
    _description = "Compute Assets"

    date_end = fields.Date(string="Date", required=True,
                           default=fields.Date.today,
                           help="All depreciation lines prior to this date "
                                "will be automatically posted", )
    note = fields.Text()
