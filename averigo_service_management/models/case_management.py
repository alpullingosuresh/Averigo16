from datetime import datetime

from odoo import models, fields, _


class CaseManagement(models.Model):
    _name = 'case.management'
    _description = "Case Management"
    _rec_name = "number"
    _order = "number desc"
    _mail_post_access = "read"
    _inherit = ["mail.thread.cc", "mail.activity.mixin"]

    number = fields.Char(string="Case number", default="/", readonly=True)
    name = fields.Char(string="Title")

    employee_ids = fields.Many2many('hr.employee', 'employee_case_rael',
                                    'case_id', 'emp_id', string='Employees',
                                    track_visibility="onchange")
    employee_id = fields.Many2many('hr.employee', 'employee_id_case_rel',string='Employe',
                                   track_visibility="always")
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 domain="[('is_customer', '=', True),('parent_id', '=', False)]")
    nick_name = fields.Char(related='partner_id.nick_name', string='Nick Name')
    partner_name = fields.Char(string="Contact Name")
    partner_email = fields.Char(string="Email")
    stage_id = fields.Many2one(comodel_name="case.management.stage",
                               string="Stage", copy=False,
                               group_expand="_read_group_stage_ids",
                               ondelete="restrict", index=True,
                               track_visibility='onchange')
    stage_name = fields.Char(related='stage_id.name', string="Stage Name")
    last_stage_update = fields.Datetime(string="Last Stage Update",
                                        default=fields.Datetime.now)
    assigned_date = fields.Datetime(string="Assigned Date")
    closed_date = fields.Datetime(string="Closed Date")
    closed = fields.Boolean(related="stage_id.closed", store=True)
    unattended = fields.Boolean(related="stage_id.unattended")
    tag_ids = fields.Many2many(comodel_name="case.management.tag",
                               string="Tags")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 required=True,
                                 default=lambda self: self.env.company)
    channel_id = fields.Many2one(comodel_name="case.management.channel",
                                 string="Channel",
                                 help="Channel indicates where the source of a case"
                                      "comes from (it could be a phone call, an email...)")
    category_id = fields.Many2one(comodel_name="case.management.category",
                                  string="Category")
    type_id = fields.Many2one(comodel_name="case.management.type",
                              string="Type")
    # type = fields.Selection(selection=TRANSFER_TYPE, string="Type")
    # type = fields.Many2one('case.management.type', string="Type")
    priority = fields.Selection(
        selection=[("0", _("Low")), ("1", _("Medium")), ("2", _("High")),
                   ("3", _("Very High"))], string="Priority", default="1")
    attachment_ids = fields.One2many(comodel_name="ir.attachment",
                                     inverse_name="res_id",
                                     domain=[
                                         ("res_model", "=", "case.management")],
                                     string="Media Attachments")
    color = fields.Integer(string="Color Index")
    kanban_state = fields.Selection(
        selection=[("normal", "Default"), ("done", "Ready for next stage"),
                   ("blocked", "Blocked")], string="Kanban State")
    active = fields.Boolean(default=True)
    route_id = fields.Many2one('route.route', string='Route')
    case_description = fields.Html('Case Description')
    resolution = fields.Html('Resolution Comment')
    internal_comment = fields.Html('Internal Comment')
    subject_id = fields.Many2one('case.subject', string="Subject")
    reported_by = fields.Char('Reported By',
                              default=lambda self: self.env.user.name)
    reported_phone = fields.Char('Phone',
                                 default=lambda self: self.env.user.phone)
    reported_email = fields.Char('Email')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=5)
    city = fields.Char('City')
    county = fields.Char('County')
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    machine_ids = fields.Many2one('account.asset', string="Equipment")
    # maintenance_team_id = fields.Many2one('asset.maintenance.team', string='Maintenance Team')
    request_date = fields.Date('Request Date',
                               default=fields.Date.context_today,
                               help="Date requested for the maintenance to happen")
    planned_hours = fields.Float("Planned Hours",
                                 help='It is the time planned to achieve the case.')
    issue_type_ids = fields.Many2many('issue.type', 'issue_type_case_rel',
                                      string="Issue Type", store="1")
    # analytic_account_active = fields.Boolean("Analytic Account", related='project_id.analytic_account_id.active',
    #                                          readonly=True)
    remaining_hours = fields.Float("Remaining Hours", store=True, readonly=True,
                                   help="Total remaining time, can be re-estimated periodically by the assignee of the case.")
    effective_hours = fields.Float("Hours Spent", compute_sudo=True, store=True,
                                   help="Computed using the sum of the case work done.")
    total_hours_spent = fields.Float("Total Hours", store=True,
                                     help="Computed as: Time Spent")
    progress = fields.Float("Progress", store=True, group_operator="avg",
                            help="Display progress of current case.")
    timesheet_ids = fields.One2many('account.analytic.line', 'case_id',
                                    'Timesheets')
    send_email = fields.Boolean('Send Notification Email')
    parts_line_ids = fields.One2many('machine.parts.line', 'case_id',
                                     string="Machine Parts", ondelete='cascade')
    damaged_parts_line_ids = fields.One2many('machine.parts.line',
                                             'damaged_parts_case_id',
                                             relation='damaged_machine_parts_machine_id_case_id',
                                             string="Damaged Parts",
                                             ondelete='cascade')
    location_id = fields.Many2one('stock.location', string="Source Location")
    warehouse_id = fields.Many2one('stock.warehouse', string="Source",
                                   domain="[('location_type', '=', 'view')]")
    location_dest_id = fields.Many2one('stock.location', 'Destination location')
    created_picking = fields.Boolean('Created Picking', store=True)
    picking_ids = fields.Many2many('stock.picking', string="Picking",
                                   copy=False)
    invoice_id = fields.Many2one('account.move', string="Invoice", copy=False)
    created_invoice = fields.Boolean('Created Invoice', copy=False)
    picking_count = fields.Integer()
    invoice_count = fields.Integer()
    destination_location_filter_ids = fields.Many2many('stock.location',
                                                       'dest_stock_location_rel',
                                                       string="Destination Location Filter")
    is_preventive = fields.Boolean()
    portal_state = fields.Selection(
        selection=[("draft", "Draft"), ("open", "Open"), ("closed", "Closed")],
        string="Status", copy=False)
    is_opend_case = fields.Boolean(string='Is Opend Case')
    open_from = fields.Char(string='Open From')
    is_billable = fields.Boolean(string='Billable')

    is_closed_case = fields.Boolean(string='Is Closed Case')
    is_running_case = fields.Boolean(string='Is Running Case')
    is_cancel_case = fields.Boolean(string='Is Cancel Case')
    account_name = fields.Char(string='Account Name', store=True)
    cancelled_case = fields.Boolean(string="case cancelled")

    # Report Fields
    # report_id = fields.Many2one('case.report', string='Report')
    reported_date = fields.Date(string='Reported Date')
    currency_id = fields.Many2one('res.currency', default=lambda
        self: self.env.company.currency_id.id)
    collected = fields.Monetary(string='Collected', track_visibility='onchange')
    refunded = fields.Monetary(string='Refunded', track_visibility='onchange')
    closed_id = fields.Many2one('res.users', string='Closed By')
    hide_fields = fields.Boolean(string='Hide Fields')
    case_stages_ids = fields.Many2many('case.management.stage',
                                       'case_stages_stage_rel',
                                       string='Case Stages', store=True, )
    account_open_case = fields.Integer(string="Account open case")
    machine_cases = fields.Integer(string="Machine cases")
    case_history_count = fields.Integer(string="Case History")
    history_message_ids = fields.Many2many('mail.message',
                                           'history_message_rel',
                                           string="Case History")
