from odoo import models, fields


class UTMCampaign(models.Model):
    _inherit = 'utm.campaign'
    _description = "Campaigns"

    name = fields.Char(string='Campaign Name', required=True, translate=True)
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True)
    parent_id = fields.Many2one('utm.campaign', string='Parent')
    user_id = fields.Many2one('res.users', string='Campaign Owner',
                              required=True, default=lambda self: self.env.uid)
    start_date = fields.Date('Start Date', default=fields.Date.today)
    end_date = fields.Date('End Date')
    type_id = fields.Many2one('utm.source', string='Campaign Type')
    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id')
    campaign_budget = fields.Monetary(string='Campaign Budget', default=0,
                                      currency_field="currency_id")
    campaign_spent = fields.Monetary(string='Money Spent', default=0,
                                     currency_field="currency_id")
    campaign_expect = fields.Monetary(string='Money Expect', default=0,
                                      currency_field="currency_id")
    description = fields.Text(size=1000)
