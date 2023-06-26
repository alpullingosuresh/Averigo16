from odoo import models, fields


class QuickUpdate(models.Model):
    _name = 'quick.update'
    _description = "Update Location"
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(string="Name", default="New")
    sequence = fields.Char(string="Sequence")
    micro_market_id = fields.Many2one('stock.warehouse', string="Micro Market",
                                      domain=[('location_type', '=',
                                               'micro_market')],
                                      ondelete='restrict')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 domain=[('is_customer', '=', True),
                                         ('parent_id', '=', False),
                                         ('type', '=', 'contact')])
    partner_ids = fields.Many2many('res.partner')
    categ_id = fields.Many2one('product.category', 'Product Category',
                               ondelete='restrict')
    search_by = fields.Many2one('ir.model.fields', domain=[
        ('model', '=', 'product.micro.market'),
        ('ttype', 'in', ('char', 'float', 'many2one', 'integer')),
        ('name', 'in', ('categ_id', 'product_code', 'min_qty',
                        'max_qty', 'name'))], string="Search By")
    condition = fields.Selection(
        [('=', 'Is'), ('!=', 'Is Not'), ('ilike', 'Contains'),
         (" ilike '{cond_str}%'", 'Starts With')], string="Condition")
    string = fields.Char(string="String")
    product_ids = fields.One2many('product.micro.market.update',
                                  'quick_update_id', string="Products")
    change_prod_count = fields.Integer(string="Products Updated")
    update_count = fields.Integer(string="Updated Count",
                                  store=True)
    scrap_ids = fields.Many2many('stock.scrap',
                                 ondelete='restrict')
    picking_ids = fields.Many2many('stock.picking',
                                   ondelete='restrict')
    inventory_ids = fields.Many2many("stock.inventory",
                                     string="Inventory Adjustment",
                                     ondelete='restrict')
    state = fields.Selection(
        [('draft', 'Draft'), ('updated', 'Updated & Reconciled')],
        string="Status", default='draft')
    product_fetched = fields.Boolean(string="Product Fetched", default=False)

    operator_id = fields.Many2one('res.company', string="Operator",
                                  default=lambda
                                      self: self.env.user.company_id,
                                  ondelete='restrict')
    user_id = fields.Many2one('res.users', string='Owner', readonly=False,
                              default=lambda self: self.env.user.id)
