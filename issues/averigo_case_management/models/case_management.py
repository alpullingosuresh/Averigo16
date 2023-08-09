from odoo import models, fields


class CaseManagement(models.Model):
    _inherit = 'case.management'

    project_id = fields.Many2one('project.project', string='Project')

    account_close_case = fields.Integer(string="Account close case", )
    request_date = fields.Datetime('Request Date', default=fields.Datetime.now,
                                   help="Date requested for the maintenance to happen")
    machine_ids = fields.Many2one('account.asset', string="Equipment",
                                  track_visibility="onchange")
    serial_number = fields.Char(string="Equipment Serial Number",
                                related='machine_ids.serial_no')

    location_dest_id = fields.Many2one('stock.location',
                                       string="Equipment Location",
                                       related='machine_ids.machine_location_id')
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
    partner_id = fields.Many2one('res.partner', string="Customer", store=True)
    route_id = fields.Many2one('route.route', string="Route",
                               related='machine_ids.route_id')
    phone = fields.Char(string="Phone", related='partner_id.phone', deault=None)
    mobile = fields.Char(string="Mobile", related='partner_id.mobile')

    in_progress = fields.Boolean(string="case in progress")

    confirm_without_parts = fields.Boolean(string="Confirm without parts")
    confirm_without_return = fields.Boolean(
        string="Confirm without parts return")

    case_notes = fields.One2many('casemanagement.notes', 'origin_id',
                                 String="Notes")

    subject = fields.Char(string='Subject')

    serial_no = fields.Char(string="Serial No", related='machine_ids.serial_no')
    machine_type_id = fields.Many2one('account.asset.type',
                                      related='machine_ids.machine_type_id')


class CaseMangementNotes(models.Model):
    _name = "casemanagement.notes"
    _order = "created_on desc"

    message = fields.Char("Message")
    company_id = fields.Many2one('res.company', 'Operator',
                                 default=lambda self: self.env.company)
    created_on = fields.Datetime("Created Date", default=fields.Datetime.now())
    origin_id = fields.Many2one('case.management', "origin_case")
