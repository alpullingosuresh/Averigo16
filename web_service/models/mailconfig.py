from odoo import api, fields, models


class AveriGoMail(models.TransientModel):
    _name = 'aes.cipher'


class OperatorMail(models.TransientModel):
    _name = 'operator.mail'

    company_id = fields.Many2one(
        'res.company', 'Operator', required=True, index=True,
        default=lambda self: self.env.company)
    operator_id = fields.Many2one('res.company')
    user_name = fields.Char()
    upc_code = fields.Char()
    device = fields.Char()
    devicemanufacturer = fields.Char()
    deviceos = fields.Char()
    devicemodel = fields.Char()
    devicedatatime = fields.Char()
    market_name = fields.Char()
    deviceplatform = fields.Char()
    appversion = fields.Char()
    barcodeformat = fields.Char()
    to_email = fields.Text()
    product = fields.Many2one('product.product')
    # product_price = fields.Many2one('product.micro.market')
    subject = fields.Char()
    body = fields.Char()


class TerminalReceipt(models.TransientModel):
    _name = 'terminal.receipt'
    operator_id = fields.Many2one('res.company')
    company_id = fields.Many2one('res.company')
    to_email = fields.Char()


class MailServerDetails(models.Model):
    _name = 'res.mail.config'
    _inherit = 'mail.thread'
    _rec_name = 'notification_type'
    _description = 'mail server details'

    operator_id = fields.Many2one(
        'res.company', 'Operator', required=True, index=True,
        default=lambda self: self.env.company)
    notification_type = fields.Selection(
        [('terminal_offline', 'Terminal Offline/Online Notification'),
         ('feedback', 'Shopper Feedback'), ('barcode', 'Barcode Scan Failure'),
         ('inventory', 'Inventory Report')],
        string="Email Type", default='feedback', tracking=True)
    mail_host_user = fields.Char('Mail Host Name')
    mail_host_smtp = fields.Char('Mail Host SMTP')
    mail_host_pass = fields.Char('Mail Host Password')
    api_key_id = fields.Char('API Key Id')
    port_no = fields.Char('Port No')
    to_email = fields.Text('Send To')
    email_line_ids = fields.One2many('res.mail.notification', 'notification_id',
                                     tracking=True)


class EmailNotification(models.Model):
    _inherit = 'mail.thread'
    _name = 'res.mail.notification'
    notification_id = fields.Char('res.mail.config', index=True)
    user_id = fields.Char('User ID')
    employee_id = fields.Char('Employee ID')
    employee_name = fields.Char('Employee Name')
    email = fields.Char('Email', tracking=True)
    phone = fields.Char('Phone')


class FireBaseNotification(models.Model):
    _name = 'fire.base.notification'
    _rec_name = 'title'
    title = fields.Char('Notification Title', tracking=True)
    user_type = fields.Selection([('normal', 'All Users')],
                                 string="Send To", default='normal')
    content = fields.Char('Content')
    web_url = fields.Char('We URL')
    image = fields.Image('Image')
    sent = fields.Boolean('sent', copy=False)
    sent_date = fields.Datetime('sent', copy=False)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Sent')],
                             string="Status", default='draft', copy=False)


class NotificationSettings(models.Model):
    _name = 'notification.setup'
    _rec_name = 'notification_type'

    notification_type = fields.Selection([('special', 'Special  Notification'),
                                          (
                                              'featured',
                                              'Featured Notification')],
                                         string="Notification Type",
                                         default='special')
    notification_time = fields.Float('Notification Time')
