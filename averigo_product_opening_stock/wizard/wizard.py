from odoo import models, fields


class PopupMessage(models.TransientModel):
    _name = 'popup.message'
    _description = "Popup Message After Opening Stock Entry Success"

    message = fields.Text()
