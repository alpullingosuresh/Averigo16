from odoo import models, fields, api, _


class ResGroupSecurity(models.Model):
    _inherit = 'res.groups'

    averigo_group_check = fields.Boolean(
        help="Used to give domain for the group security menu")
    operator_id = fields.Many2one('res.company')
    default_groups = fields.Boolean('Default Groups',
                                    help="This is to check the groups is "
                                         "default or not")
    active = fields.Boolean(default=True)
    select_all_write = fields.Boolean('Select All Write')
    select_all_create = fields.Boolean('Select All Create')
    select_all_delete = fields.Boolean('Select All Delete')
