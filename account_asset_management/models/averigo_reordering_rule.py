from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ReorderingRule(models.Model):
    _name = "reordering.rule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Reordering Rule"
    _check_company_auto = True

    name = fields.Char('Name', copy=False, required=True, readonly=True,
                       default=lambda self: self.env[
                           'ir.sequence'].next_by_code('reordering.rule'))
    active = fields.Boolean('Active', default=True,
                            help="If the active field is set to False, it will allow you to hide the orderpoint without removing it.")
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse',
                                   check_company=True, ondelete="cascade",
                                   required=True)
    location_id = fields.Many2one('stock.location', 'Location',
                                  ondelete="cascade", required=True,
                                  check_company=True)
    product_id = fields.Many2one('product.product', 'Product',
                                 ondelete='cascade', required=True,
                                 check_company=True,
                                 domain="[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure',
                                  related='product_id.uom_id',
                                  readonly=True, required=True,
                                  default=lambda self: self._context.get(
                                      'product_uom', False))
    product_uom_name = fields.Char(string='Product unit of measure label',
                                   related='product_uom.name', readonly=True)

    product_min_qty = fields.Float('Minimum Quantity',
                                   digits='Product Unit of Measure',
                                   required=True,
                                   help="When the virtual stock equals to or goes below the Min Quantity specified for this field, Odoo generates "
                                        "a procurement to bring the forecasted quantity to the Max Quantity.")
    product_max_qty = fields.Float('Maximum Quantity',
                                   digits='Product Unit of Measure',
                                   required=True,
                                   help="When the virtual stock goes below the Min Quantity, Odoo generates "
                                        "a procurement to bring the forecasted quantity to the Quantity specified as Max Quantity.")
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    allowed_location_ids = fields.One2many(comodel_name='stock.location')
    is_parts_reorder = fields.Boolean('Equipment Parts Reorder')
