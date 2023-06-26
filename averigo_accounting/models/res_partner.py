from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_account_receivable_id = fields.Many2one('account.account',
                                                     company_dependent=True,
                                                     string="Account Receivable",
                                                     domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=True)
    control_account_id = fields.Many2one('account.account',
                                         domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]")
    sales_discount_account_id = fields.Many2one('account.account',
                                                domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    advance_account_id = fields.Many2one('account.account',
                                         domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]")
    insurance_account_id = fields.Many2one('account.account',
                                           domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    sales_tax_liability_account_id = fields.Many2one('account.account',
                                                     domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    terms_discount_account_id = fields.Many2one('account.account',
                                                domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    shipping_handling_account_id = fields.Many2one('account.account',
                                                   domain="[('internal_type', '=', 'other'),('deprecated', '=', False)]")
    card_ids = fields.One2many('res.partner.card', 'partner_id', string='Banks')
    check_ids = fields.One2many('res.partner.check', 'partner_id',
                                string='Checks')
