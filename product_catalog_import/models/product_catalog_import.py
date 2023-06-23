# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ProductCatalogImport(models.TransientModel):
    _name = 'product.catalog.import'
    _description = 'Import Product Catalog'

    attachment_ids = fields.Many2many('ir.attachment', string='Files',
                                      required=True)
