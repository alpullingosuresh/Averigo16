from odoo import models, fields


class ImportFailLog(models.Model):
    _name = 'import.fail.log'
    _rec_name = 'attempt_id'
    _description = "Failed Imports"

    user = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    attempt_id = fields.Char()
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company.id)
    entity = fields.Char()
    success = fields.Integer(string="Successful Records")
