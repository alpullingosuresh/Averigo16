from odoo import fields, models


class UsersActivity(models.Model):
    _name = 'res.users.activity'
    _description = 'User activity'

    user_id = fields.Many2one('res.users', 'User')
    user_uid = fields.Char('User UID')


class Users(models.Model):
    _inherit = 'res.users'

    otp = fields.Char('Otp', help="Suspicious Login Otp")


class UserOtp(models.Model):
    _name = 'res.users.otp'

    user_id = fields.Many2one('res.users', string='user')
    otp = fields.Char(sting="otp")


class LoginAttempt(models.Model):
    _name = 'res.users.login.attempt'
    _description = 'User Login Attempt'

    user_id = fields.Many2one('res.users', 'User', help="Login User Id")
    status = fields.Selection([('failed', 'Failed'), ('success', 'Success')],
                              'Status', help="status of login attempt")
    failed_reason = fields.Char('Failed Reason',
                                help="Failed Reason of login attempt")
    location = fields.Char('Location',
                           help="location of user when attempting the login")
    ip_address = fields.Char('IP Address', help="Ip of user when login")
    login_time = fields.Datetime('Login Time', help="Login time of user")
    timezone = fields.Char('TimeZone',
                           help="Timezone of user when attempting the login")
    platform = fields.Char('Platform', help="Operating system of user when "
                                            "attempting the login")
    browser = fields.Text('Browser',
                          help="browse of user when attempting the login")
