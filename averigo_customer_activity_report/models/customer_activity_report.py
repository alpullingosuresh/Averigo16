from odoo import fields, models


class ActivityReport(models.TransientModel):
    _name = 'averigo.customer.activity.report'

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    operator_ids = fields.Many2many('res.company', 'op_ids', string='Operator')
    type = fields.Selection([('open', 'Open Activity'), ('notes', 'Notes'),
                             ('closed', 'Closed Activity'),
                             ('events', 'Events')], default='open',
                            tracking=True, required=True)
    acc_name = fields.Many2one('res.partner', string='Account Name')
    assigned_to = fields.Many2many('res.users', 'ass_ids',
                                   string='Assigned To', index=True,
                                   domain="['|', "
                                          "('user_type', '=', 'operator'), "
                                          "('user_type', '=', 'admin')]")
    activity_type_id = fields.Many2one('mail.activity.type',
                                       string='Activity Type')
    from_date = fields.Date(string='From', default=fields.Date.context_today)
    activity_report_line_ids = fields.Many2many('activity.report.lines')
    to_date = fields.Date(string='To', default=fields.Date.context_today)
    report_length = fields.Integer()
    status = fields.Selection(
        [('overdue', 'Overdue'), ('today', 'Today'), ('planned', 'Planned')],
        'Status')
    created_user_ids = fields.Many2many('res.users', 'cre_ids',
                                        string='Created By',
                                        domain="['|', ('user_type', '=', 'operator'), ('user_type', '=', 'admin')]", )
    user_filter_ids = fields.Many2many('res.users', 'user_ids')


class ActivityReportLines(models.TransientModel):
    _name = 'activity.report.lines'
    _description = "Customer Retention Report"

    act_id = fields.Many2one('mail.activity')
    done_act_id = fields.Many2one('done.activity.datas')
    report_id = fields.Many2one('averigo.customer.activity.report')
    res_name = fields.Char(string='Name', readonly=True)
    acc_name = fields.Many2one('res.partner', string='Account Name')
    type = fields.Selection([('open', 'Open Activity'), ('notes', 'Notes'),
                             ('closed', 'Closed Activity'),
                             ('events', 'Events')], tracking=True,
                            required=True, store='True')
    act_create_date = fields.Datetime(string='Created Date', readonly=True)
    create_by = fields.Many2one('res.users', string='Created User',
                                readonly=True)
    # res_model_id = fields.Many2one(
    #     'ir.model', 'Model', index=True,
    #     domain=['&', ('is_mail_thread', '=', True), ('transient', '=', False)],
    #     help='Specify a model if the activity should be specific to a model'
    #          ' and not available when managing activities for other models.')
    activity_type_id = fields.Many2one(
        'mail.activity.type', string='Activity Type')
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    subject = fields.Char(string='Subject')
    date = fields.Date(string=' Due Date')
    status = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], 'Status')
    notes = fields.Html(string='Notes')
    desc = fields.Html(string='Description')
    event_desc = fields.Html(string='Description')
    start_date = fields.Datetime(string='Start Date', readonly=True)
    end_date = fields.Datetime(string='End Date', readonly=True)
    location = fields.Char(string='Location')
    attendees_ids = fields.Many2many('res.partner', string='Attendees')
    duration = fields.Float(string='Duration')


class DoneActivityDatas(models.Model):
    _name = 'done.activity.datas'

    res_name = fields.Char('Document Name', readonly=True)
    user_id = fields.Many2one(
        'res.users', 'Assigned to', index=True)
    activity_type_id = fields.Many2one(
        'mail.activity.type', string='Activity Type',
        domain="['|', ('res_model_id', '=', False), "
               "('res_model_id', '=', res_model_id)]",
        ondelete='restrict')
    date_deadline = fields.Date('Due Date', index=True)
    note = fields.Html('Note', sanitize_style=True)
    summary = fields.Char('Summary')
    act_create_date = fields.Date('Created Date', index=True)
    act_create_by = fields.Many2one('res.users', string='Created User',
                                    readonly=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    res_model = fields.Char(
        'Related Document Model',
        index=True, store=True, readonly=True)
    # activity_category = fields.Char(readonly=True)
    # activity_decoration = fields.Char(readonly=True)
