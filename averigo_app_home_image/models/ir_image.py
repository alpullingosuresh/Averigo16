import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class IRImage(models.Model):
    _name = 'ir.image'
    _description = 'Hoe Screen Image'
    _order = 'create_date desc'

    name = fields.Char()
    image = fields.Binary(string='Image', required=True)
    active = fields.Boolean(string="Active", default=True)
    operator_id = fields.Many2many('res.company', 'ir_image_res_company_rel',
                                   'image_id', 'company_id',
                                   domain=[('is_main_company', '!=', True)],
                                   string="Operator")
    location = fields.Many2many('res.partner', 'ir_image_res_partner_rel',
                                'image_id', 'partner_id',
                                domain=[('is_customer', '=', True)])
    micro_market_id = fields.Many2many('stock.warehouse',
                                       'ir_image_stock_warehouse_rel',
                                       'image_id', 'warehouse_id',
                                       domain=[('location_type', '=',
                                                'micro_market')])
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="Stop Date")
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="Stop Time")
    banner_text = fields.Text(string="Banner Text")
    mm_ids = fields.Many2many('stock.warehouse',
                              'ir_image_stock_warehouse_rel2', 'image_id2',
                              'warehouse_id2')
