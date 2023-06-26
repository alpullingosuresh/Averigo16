from odoo import  fields, models


class PartnerCheck(models.Model):
    _name = 'res.partner.check'
    _rec_name = 'check_number'
    _description = 'Check Accounts'

    check_bank_id = fields.Many2one('res.bank', string='Check Bank')
    check_bank_account_id = fields.Many2one('res.partner.bank',
                                            string='Check Bank Account')
    check_number = fields.Char('Check No', required=True)
    check_date = fields.Date(required=True, default=fields.Date.context_today)
    check_amount = fields.Float('Check Amount', digits="Account")
    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one('res.partner', 'Check Holder',
                                 ondelete='cascade', index=True,
                                 domain=['|', ('is_company', '=', True),
                                         ('parent_id', '=', False)])
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company,
                                 ondelete='cascade')
    is_vendor = fields.Boolean('Is Vendor')
    is_customer = fields.Boolean('Is Customer')
    is_advance = fields.Boolean('Is Advance Payment',
                                help="This is an advance payment check")
