from odoo import  fields, models

class CustomerContract(models.Model):
    _name = 'customer.contract'
    _description = 'Customer Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Contract Reference', required=True)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 tracking=True,
                                 check_company=True)
    date_start = fields.Date('Start Date', required=True,
                             default=fields.Date.today,
                             help="Start date of the contract.")
    date_end = fields.Date('End Date',
                           help="End date of the contract (if it's a fixed-term contract).")
    advantages = fields.Text('Advantages')
    attachment_ids = fields.Many2many('ir.attachment', 'contract_attachment_rel', 'contract_id', 'attachment_id',
                                      string='Attachments', track_visibility="onchange")
    notes = fields.Text('Notes')
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('close', 'Expired'),
        ('cancel', 'Cancelled')
    ], string='Status', group_expand='_expand_states', copy=False,
        tracking=True, help='Status of the contract', default='draft')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company,
                                 required=True)
    """
        kanban_state:
            * draft + green = "Incoming" state (will be set as Open once the contract has started)
            * open + red = "Pending" state (will be set as Closed once the contract has ended)
            * red = Shows a warning on the employees kanban view
    """
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')
    ], string='Kanban State', default='normal', tracking=True, copy=False)
    currency_id = fields.Many2one(string="Currency",
                                  related='company_id.currency_id',
                                  readonly=True)

