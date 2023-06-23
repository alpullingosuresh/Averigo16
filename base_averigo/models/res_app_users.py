from odoo import fields, models


class ResAppUsers(models.Model):
    _name = 'res.app.users'
    _description = "App Users"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean('Active', default=True)
    email = fields.Char(string="Email", required=True)
    mobile = fields.Char(string="Mobile")
    zip = fields.Char()
    phone = fields.Char(string="Phone", size=120)
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    county = fields.Char()
    state_id = fields.Many2one('res.country.state', string="Fed. State")
    country_id = fields.Many2one('res.country', string="Country")
    end_user = fields.Boolean(default=False)
    code = fields.Char(string="Code")
    devicetoken = fields.Char(string="DeviceToken")
    last_session_id = fields.Many2one('user.session.history',
                                      strin="Last Session")
    last_session_date = fields.Datetime(related="last_session_id.session_date",
                                        string="Last Login")
    lastname = fields.Char('Last Name')
    device_udid = fields.Char('Device UDID')
    nickname = fields.Char('Nick Name')
    product_related_mailid = fields.Char('Related EMail',
                                         help="Product related mail")
    enable_sms = fields.Selection([('N', 'Y'), ('N', 'N')],
                                  string='Enable SMS', default="N")
    enabel_newsletter = fields.Selection([('Y', 'Yes'), ('N', 'No')],
                                         string='Enable Newsletter',
                                         default="N")
    password = fields.Char('Password')
    app_related_mailid = fields.Char('APP Related Email',
                                     help="app related mail id")
    item_reconcile = fields.Selection([('Y', 'Y'), ('N', 'N')],
                                      string='Item Reconcile', default="N")
    usertype = fields.Selection([('N', 'Normal User'), ('E', 'Employee')],
                                string='Item Reconcile', default="N")
    service_name = fields.Char('Service Name')
    companyacro = fields.Char('Companyacro')
    adminemaillist = fields.Char('Admin Email List')
    company_name = fields.Char('Company Name')
    profile_image = fields.Boolean('Profile Image')
    item_receive = fields.Selection([('Y', 'Y'), ('N', 'N')],
                                    string='Item Receive', default="N")
    item_add = fields.Selection([('Y', 'Y'), ('N', 'N')], string='Add Item',
                                default="N")
    otp = fields.Integer('OTP')
    password_reset_request = fields.Boolean(default=False)
    devicetype = fields.Char('DeviceType')
    last_visted = fields.Many2one('stock.warehouse')
    is_imported = fields.Boolean('Imported User', default=False)


class AppUserPasswordReset(models.TransientModel):
    _name = "app.user.pwd.reset"
    _description = "App User Password Reset"

    app_user_id = fields.Many2one("res.app.users", string="App User")
    user_name = fields.Char(String="User Name", related="app_user_id.name")
    user_email = fields.Char(String="Email", related="app_user_id.email")
    new_password = fields.Char(String="New Password")
    confirm_pwd = fields.Char(string="Confirm Password")
    check_match = fields.Boolean()
