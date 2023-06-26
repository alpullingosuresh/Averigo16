import logging

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    """inherit crm.lead model to add averigo specific fields"""
    _inherit = 'crm.lead'
    _order = 'create_date desc'

    first_name = fields.Char(string="First Name", size=78, required=True)
    middle_name = fields.Char(string="Middle Name", size=78)
    last_name = fields.Char(string="Last Name", size=78, required=True)
    partner_name = fields.Char(string="Company Name", size=78, required=False)
    user_id = fields.Many2one('res.users', string="Lead Owner", required=True)
    status = fields.Many2one('crm.lead.status', string="Status")
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=10,
                                 index=True,
                                 domain="[('is_customer', '=', True),('parent_id', '=', False),('type', '=', 'contact')]",
                                 help="Linked partner (optional). Usually "
                                      "created when converting the lead. You "
                                      "can find a partner by its Name, TIN, "
                                      "Email or Internal Reference.")

    _sql_constraints = [
        ('check_probability', 'check(probability >= 0 and probability <= 100)',
         'The probability of closing the deal should be between 0% and 100%')
    ]


class CRMLeadStatus(models.Model):
    """CRM lead status model, records of this model will be selected
     as status"""
    _name = 'crm.lead.status'
    _description = "CRM Lead Status"

    name = fields.Char("Status")
    company_id = fields.Many2one('res.company', string="Operator",
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True)


class CRMTeam(models.Model):
    """inherit crm.Team model to add averigo specific help"""
    _inherit = 'crm.team'

    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id)


class CalendarEvents(models.Model):
    _inherit = 'calendar.event'

    operator_id = fields.Many2one('res.company', string='Operator', index=True,
                                  default=lambda s: s.env.company.id)
    activity_type = fields.Many2many("mail.activity.type")
    employees = fields.Many2many('hr.employee', string='Truck Drivers')
    employee_contacts = fields.Many2many('res.partner',
                                         relation='calendar_event_employee_contacts',
                                         domain=[('is_customer', '=', False),
                                                 ('is_vendor', '=', False),
                                                 ('type', '=', 'contact')]
                                         )
    customers = fields.Many2many('res.partner',
                                 relation='res_partner_calendar_event_customer',
                                 domain=[('is_customer', '=', True),
                                         ('parent_id', '=', False),
                                         ('type', '=', 'contact')])
    customer_contacts = fields.Many2many('res.partner',
                                         relation='res_partner_calendar_event_contact_customer',
                                         domain=[('is_customer', '=', True),
                                                 ('parent_id', '!=', False),
                                                 ('type', '=', 'contact')])
    show_customer_contact = fields.Boolean()


class ResPartnerTitle(models.Model):
    _inherit = 'res.partner.title'
    _description = 'Contact Title'

    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
    active = fields.Boolean(default=True)


class Tag(models.Model):
    _inherit = 'crm.lead.tag'
    _description = "CRM Tags"

    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
