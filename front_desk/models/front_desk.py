
from odoo import models, fields


class ResAppUsers(models.Model):
    _inherit = 'res.app.users'

    emp_code = fields.Char(string="Employee Ref. Code")


class FrontDesk(models.Model):
    _name = 'front.desk'
    _description = "Front Desk/Employee Discount"
    _rec_name = 'sequence'
    _order = 'create_date desc'

    sequence = fields.Char(sstring="Desk Id",
                           copy=False)
    active = fields.Boolean(string="Active", default=True)
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        string="Micro Market",
                                        domain=[('location_type', '=',
                                                 'micro_market')],
                                        ondelete='restrict')
    partner_id = fields.Many2one('res.partner', string="Bill To Customer",
                                 ondelete='restrict')
    partner_ids = fields.Many2many('res.partner', compute='compute_partner_ids')
    user_ids = fields.Many2many('res.app.users', string="App Users")
    desk_type = fields.Selection(
        [('employee', 'Employee'), ('front', 'Front Desk')],
        string="Desk Type", default="employee")
    discount = fields.Float(string="Discount")
    allow_all = fields.Boolean(string="Allow All Category Items")
    banner_text = fields.Text(string="Banner Text")
    banner_image = fields.Binary(string="Banner Image")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Confirmed')],
                             string="Status", default='draft')
    operator_id = fields.Many2one('res.company', string="Operator",
                                  default=lambda
                                      self: self.env.user.company_id)
    user_line = fields.One2many('front.desk.line', 'front_desk_id', string="User List",
                                copy=False)


class FrontDeskLine(models.Model):
    _name = 'front.desk.line'
    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char()
    employee_id = fields.Char()
    front_desk_id = fields.Many2one('front.desk', "Front Desk Template", index=True)
    app_user = fields.Many2one('res.app.users', string="User",
                               ondelete='restrict')
    disable_user = fields.Boolean(string="Disable", default=False)

