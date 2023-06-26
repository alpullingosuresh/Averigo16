from odoo import  fields, models


class PartnerCreditCard(models.Model):
    _name = 'res.partner.card'
    _rec_name = 'card_number'
    _description = 'Card Accounts'

    bank_id = fields.Many2one('res.bank', string='Bank')
    card_type = fields.Selection(
        [('master_card', 'Master Card'), ('visa', 'Visa')], string='Card Type',
        default='master_card')
    card_number = fields.Char('Card #', required=True)
    card_name = fields.Char('Name', required=True)
    card_expiry = fields.Date(required=True, default=fields.Date.context_today)
    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one('res.partner', 'Card Holder',
                                 ondelete='cascade', index=True,
                                 domain=['|', ('is_company', '=', True),
                                         ('parent_id', '=', False)])
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company,
                                 ondelete='cascade')
    is_vendor = fields.Boolean('Is Vendor')
    is_customer = fields.Boolean('Is Customer')
