from odoo import models, fields, api


class ResUsersGroup(models.Model):
    _inherit = 'res.users'

    averigo_groups_id = fields.Many2many('res.groups',
                                         'res_groups_averigo_users_rel', 'uid',
                                         'gid',
                                         string='Averigo Groups')
    averigo_groups_id_new = fields.Many2many('res.groups',
                                             'res_groups_averigo_users_rel_new',
                                             string='Averigo Groups New')
    averigo_groups_id_rem = fields.Many2many('res.groups',
                                             'res_groups_averigo_users_rel_rem',
                                             string='Averigo Groups Deleted')
    group_security_menu = fields.Boolean('Security Menu',
                                         help="This is to give access to the "
                                              "security menu")

