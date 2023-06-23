from odoo import models, fields


class AdminFeaturedProducts(models.Model):
    _name = 'admin.featured.products'
    _rec_name = 'discount'
    _description = 'Admin Featured Products'

    image = fields.Binary(string='Image', required=True, copy=False)
    product_ids = fields.Many2many('product.product',
                                   'featured_product_product_rel',
                                   string="Product", copy=False)
    active = fields.Boolean(string="Active", default=True)
    operator_ids = fields.Many2many('res.company',
                                    'featured_product_operator_rel',
                                    domain=[('is_main_company', '!=', True)],
                                    string="Operator")
    partner_ids = fields.Many2many('res.partner','admin_featured_products_partner_rel')
    location = fields.Many2many('res.partner',
                                'admin_featured_products_res_partner_rel',
                                'product_id', 'partner_id',
                                string='Customer')
    micro_market_id = fields.Many2many('stock.warehouse',
                                       'admin_featured_product_stock_warehouse_rel',
                                       'product_id',
                                       'warehouse_id')
    market_ids = fields.Many2many('stock.warehouse', 'admin_featured_product_market_ids_rel')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="Stop Date")
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="Stop Time")
    discount = fields.Float(string="Discount %", copy=False)
    import_product_image = fields.Boolean(
        string="Import Image From Product Master")
    mm_ids = fields.Many2many('stock.warehouse',
                              'admin_featured_products_stock_warehouse_rel2',
                              'product_id2',
                              'warehouse_id2', copy=False)
    url = fields.Char('URL')
    banner_text = fields.Text()
    data_file = fields.Binary(string='Video', attachment=True)
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    start_time_display = fields.Float(string="Start Time")
    end_time_display = fields.Float(string="Stop Time")
    t_start_seconds = fields.Integer("Start Seconds")
    t_start_period = fields.Selection([('am', 'AM'), ('pm', 'PM')],
                                      default='am')
    t_end_seconds = fields.Integer("End Seconds")
    t_end_period = fields.Selection([('am', 'AM'), ('pm', 'PM')],
                                    default='am')
    time_format = fields.Selection(
        [('hm', 'HH:MM'), ('hms', 'HH:MM:SS'), ('imp', 'HH:MM AM/PM'),
         ('ims', 'HH:MM:SS AM/PM')],
        string="Time Format", related="company_id.time_format_selection")
    thumbnail_image = fields.Binary(string='Thumbnail Image', required=True,
                                    copy=False)
    banner_type = fields.Selection([
        ('url', 'Video URL'),
        ('image', 'Image'),
    ], default='image', required=True, )
    video_field = fields.Many2many('ir.attachment', 'pt_ir_attachment_rel',
                                   'pt_id', 'attach_id', limit=1,
                                   string="Attachment",
                                   required=True, ondelete='cascade')

    notification = fields.Boolean('Notification', default=False)
    send_notification = fields.Boolean(default=False)
    send_title = fields.Text(string="Notification Title")
    image_notification = fields.Image(string='Notification Image', copy=False)
    image_update_count = fields.Text(default='0')
    update_date = fields.Date(string="Update Date")
    product_associated = fields.Many2one('product.product',
                                         string="Image to Associate")
