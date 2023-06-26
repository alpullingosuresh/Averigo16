from odoo import models, fields, api


class AverigoIrModel(models.Model):
    _inherit = 'ir.model'

    averigo_model = fields.Boolean(string='Averigo Model',
                                   inverse='_inverse_averigo_model',
                                   store=True,
                                   help='Used to sort the models in averigo')
