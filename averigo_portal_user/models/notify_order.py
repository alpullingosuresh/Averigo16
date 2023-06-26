from odoo import models, fields, api, modules


class SaleNotification(models.Model):
    _name = 'notify.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Portal Notification"

    user_id = fields.Many2many('res.users', 'activity_user_id_rel')
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
    name = fields.Char('Name')
    summary = fields.Char(string='Summary')
    image = fields.Image('Image')
    portal_notify = fields.Boolean(default=False)
    send_all = fields.Boolean(default=False)
    date_start = fields.Datetime('Start Date',
                                 default=lambda self: fields.Datetime.now())
    date_end = fields.Datetime('End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
    ], string='Status', readonly=True, copy=False, store=True, index=True,
        tracking=3, default='draft')


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = "Planned Activities"

    user_id = fields.Many2one('res.users', 'user_rel', string='Assigned to',
                              default=False,
                              index=True, required=True)
    multiple_users = fields.Many2many('res.users', 'multiple_user_rel',
                                      store=True,
                                      domain="['|', "
                                             "('user_type', '=', 'operator'), "
                                             "('user_type', '=', 'admin')]")
    display_names = fields.Char(string="Display Names")
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')


class MailActivityMixin(models.AbstractModel):
    _inherit = 'mail.activity.mixin'

    activity_user_ids = fields.Many2many(
        'res.users', string='Responsible User',
        related='activity_ids.multiple_users', readonly=False,
        search='_search_activity_user_ids',
        default=lambda self: self.env.user,
        groups="base.group_user")
