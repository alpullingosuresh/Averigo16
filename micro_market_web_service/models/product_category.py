from odoo import fields, models


class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'mail.thread', 'mail.activity.mixin']

    category_code = fields.Char(copy=False)
    category_image = fields.Image()
    cate_image = fields.Binary()
    category_image_1920 = fields.Image(max_width=840, max_height=840)
    category_desc = fields.Text('Description')
    enable_front_desk = fields.Boolean(track_visibility="onchange")
    operator_id = fields.Many2one('res.company', string='Operator',
                                  required=True,
                                  default=lambda self: self.env.company)
    available_outside = fields.Boolean(default=False,
                                       track_visibility="onchange")
    update_image = fields.Char(default='0')

    _sql_constraints = [("category_code", "unique(category_code, operator_id)",
                         "The code you entered is already taken, please try a "
                         "new one"),
                        ("product_category_name_operator_unique",
                         "unique(name, operator_id)",
                         "There is an existing category with same name")]
