from odoo import api, fields, models


class TransactionReport(models.TransientModel):
    _name = 'transaction.list.report'
    _inherit = ['transaction.list.report', 'recurring.parent']

    contact_ids = fields.Many2many('res.partner', string="Contacts")
    show_name = fields.Boolean(string="Show Name")
    show_account_nickname = fields.Boolean(string="Show Account Nickname")
    show_beacon = fields.Boolean(string="Show Beacon")
    show_averigo_login = fields.Boolean(string="Show Averigo Login")
    show_item_number = fields.Boolean(string="Show Item Number")
    show_product_category = fields.Boolean(string="Show Product Category")
