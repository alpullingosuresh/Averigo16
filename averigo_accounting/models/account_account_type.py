# from odoo import fields, models
#
#
# class AccountAccountType(models.Model):
#     _inherit = "account.account.type"
#
#     range_from = fields.Integer(translate=True)
#     range_to = fields.Integer(translate=True)
#     bind_to = fields.Selection([
#         ('cash', 'Cash'),
#         ('bank', 'Bank'),
#         ('writ_off', 'Write Off')],
#         default='cash', index=True)
