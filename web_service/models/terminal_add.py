from odoo import api, fields, models


class TerminalAdd(models.Model):
    _name = 'terminal.add'
    _rec_name = 'rec'

    rec = fields.Text(default='Terminal Add')
    image = fields.Image(string='Image', required=True, copy=False)
    product_id = fields.Many2one('product.product', string="Product",
                                 copy=False)
    product_ids = fields.Many2many('product.product', string="Product",
                                   copy=False)
    active = fields.Boolean(string="Active", default=True)
    operator_ids = fields.Many2many('res.company',
                                    domain=[('is_main_company', '!=', True)],
                                    string="Operator")
    location = fields.Many2many('res.partner', 'location_res_partner_rel',
                                'product_id', 'partner_id',
                                string='Customer')
    partner_ids = fields.Many2many('res.partner', 'partner_partner_ids_rel')
    micro_market_id = fields.Many2many('stock.warehouse',
                                       'micro_market_warehouse_rel')
    market_ids = fields.Many2many('stock.warehouse', 'market_warehouse_rel')
    url = fields.Char('URL')
    banner_text = fields.Text()
    data_file = fields.Binary(string='Video', attachment=True)
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    image_update_count = fields.Text(default='0')
    product_template_image_ids = fields.One2many('advertisement.image',
                                                 'product_tmpl_id',
                                                 string="Extra Product Media",
                                                 copy=True)
    delay_time = fields.Integer(default='6')
    local_offer_url = fields.Char('Local Offers URL')


class AdvertisementImage(models.Model):
    _name = 'advertisement.image'
    _description = "Advertisement Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    Operator_id = fields.Many2one('res.company', 'Operator')
    product_tmpl_id = fields.Many2one('terminal.add', "Terminal Template",
                                      index=True)
    embed_code = fields.Char(compute="_compute_embed_code")
    can_image_1024_be_zoomed = fields.Boolean("Can Image 1024 be zoomed",
                                              store=True)
    first_image = fields.Integer(default=0)
    image_update_count = fields.Text(default='0')
