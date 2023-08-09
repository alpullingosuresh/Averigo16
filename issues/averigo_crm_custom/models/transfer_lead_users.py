from odoo import fields, models


class TransferLeadUsers(models.Model):
    _name = 'transfer.lead.users'

    name = fields.Char(default="Transfer Access users")
    transfer_user_ids = fields.One2many('transfer.access.users',
                                        'user_details_id', invisible=True,
                                        store=True)


class TransferAccessUsers(models.Model):
    _name = 'transfer.access.users'

    user_details_id = fields.Many2one('transfer.lead.users')
    company_id = fields.Many2one('res.company', string='Operator')
    user_ids = fields.Many2many('res.users', string='Users')


class DefaultLeadAssignUsers(models.Model):
    _name = 'default.lead.assign.users'

    name = fields.Char(default="Default Lead Assign users")
    default_user_ids = fields.One2many('transfer.assign.users',
                                       'user_details_id', invisible=True,
                                       store=True)


class TransferAssignUsers(models.Model):
    _name = 'transfer.assign.users'

    user_details_id = fields.Many2one('default.lead.assign.users')
    company_id = fields.Many2one('res.company', string='Operator')
    user_id = fields.Many2one('res.users', string='Users')
