from odoo import models, fields


class AverigoIrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    averigo_menu = fields.Boolean(help="used to add domain for listing menu")