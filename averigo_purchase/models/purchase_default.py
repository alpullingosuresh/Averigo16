from odoo import fields, models


class PurchaseDefault(models.Model):
    _name = 'purchase.default'
    _inherit = 'mail.thread'
    _description = 'Default Purchase'
    """Default value in Purchase"""

    name = fields.Char(default='Purchase Setup')
    vendor_no_sequence = fields.Boolean('Generate Vendor #', tracking=True,
                                        default=True)
    starting_vendor_no = fields.Integer('Starting Vendor #', tracking=True)
    purchase_manager = fields.Many2one('hr.employee', tracking=True)
    payment_term = fields.Many2one('account.payment.term',
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', operator_id)]",
                                   tracking=True)
    ship_via = fields.Many2one('ship.via', tracking=True)
    operator_id = fields.Many2one('res.company',
                                  default=lambda s: s.env.company.id)
    exist_vendor = fields.Boolean()
    warehouse_id = fields.Many2one('stock.warehouse', tracking=True,
                                   domain="[('location_type', '=', 'view')]")

