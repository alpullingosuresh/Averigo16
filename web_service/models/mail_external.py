from odoo import models, fields


class MailExternal(models.Model):
    _name = 'mail.external'
    _description = 'Mail External'

    subject = fields.Char(string='Subject', required=True)
    to_email = fields.Char(string='To', required=True)
    body = fields.Text(string='Body', required=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    product_id = fields.Many2one('product.product', string='Product')
    upc_code = fields.Char(string='UPC Code')
    user_name = fields.Char(string='User Name')
    operator_id = fields.Many2one('res.company', string='Operator')
    company_id = fields.Many2one('res.company', string='Company')
    market_name = fields.Char(string='Market Name')

    _rec_name = 'subject'
