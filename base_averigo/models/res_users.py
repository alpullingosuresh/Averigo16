from odoo import  fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_type = fields.Selection([('admin', 'Admin'), ('operator', 'Operator'),
                                  ('customer', 'Customer')],
                                 string="User Type", default="admin")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    role_selection = fields.Selection([('na', 'N/A')])
    login = fields.Char(required=True, string="Username",
                        help="Used to log into the system")

    group_micro_market = fields.Boolean(string="Micromarkets", default=True)
    allow_all_mm = fields.Boolean(string="All Micromarkets", default=True)
    group_micro_market_access = fields.Many2many('access.permissions',
                                                 'res_users_micro_market_rel',
                                                 'user_id', 'mm_access_id',
                                                 string="Market Permissions")
    group_user_management = fields.Boolean(string="User Management",
                                           default=True)
    group_user_management_access = fields.Many2many('access.permissions',
                                                    'res_users_user_management_rel',
                                                    'user_id',
                                                    'user_management_id',
                                                    string="User Permissions")
    group_gpm = fields.Boolean(string="Global Product Management",
                               default=True)
    group_gpm_access = fields.Many2many('access.permissions',
                                        'res_users_gpm_access_rel',
                                        'user_id', 'gpm_id',
                                        string="GPM Permissions")
    group_home_screen_image = fields.Boolean(string="Home Screen Image",
                                             default=True)
    group_home_screen_image_access = fields.Many2many('access.permissions',
                                                      'res_users_home_screen_rel',
                                                      'user_id',
                                                      'home_screen_id',
                                                      string="Home Screen Image Permissions")

    group_portal_user = fields.Boolean(string="Portal Users",
                                       default=True)
    group_portal_user_access = fields.Many2many('access.permissions',
                                                'res_users_portal_access_rel',
                                                'user_id', 'portal_access_id',
                                                string="Portal Users Permissions")
    group_reports = fields.Boolean(string="Reports",
                                   default=True)
    group_reports_access = fields.Many2many('access.permissions',
                                            'res_users_report_rel',
                                            'user_id', 'report_access_id',
                                            string="Reports Permissions")
    group_operators = fields.Boolean(string="Operator Management",
                                     default=True)
    group_operators_access = fields.Many2many('access.permissions',
                                              'res_users_operator_rel',
                                              'user_id', 'operator_id',
                                              string="Operator Permissions")
    operator_ids = fields.Many2many('res.company', 'res_users_operators_rel',
                                    'user_id', 'operator_id',
                                    string="Operators")
    company_domain = fields.Char(string="Company Domain")
    micro_market_ids = fields.Many2many('stock.warehouse',
                                        'res_users_micro_market_user_rel',
                                        'user_id', 'ware_house_id',
                                        string="Micromarkets")

    group_company_info = fields.Boolean(string="Company Information",
                                        default=True)
    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Averigo')],
        'Notification', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Averigo: notifications appear in your Averigo Inbox")

    group_inventory = fields.Boolean(string="Inventory", default=True)
    group_hr = fields.Boolean(string="Human Resource", default=True)
    group_customer_care = fields.Boolean(string="Customer Care",
                                         default=True)
    group_users = fields.Boolean(string="Users", default=True)
    group_division = fields.Boolean(string="Branch", default=True)
    group_contract = fields.Boolean(string="Contract", default=True)
    group_operator_report = fields.Boolean(string="Report", default=True)
    menu_id = fields.Many2one('ir.ui.menu', string="Menu")
    menu_ids = fields.Many2many('ir.ui.menu', string="Menus")




class AccessPermissions(models.Model):
    _name = 'access.permissions'
    _description = "Access Permissions"

    name = fields.Char(string="Name", required=True)
