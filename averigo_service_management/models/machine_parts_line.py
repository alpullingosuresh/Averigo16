from odoo import models, fields


class MachinePartsLine(models.Model):
    _name = 'machine.parts.line'
    _description = "Machine parts Line"

    product_id = fields.Many2one('product.product', string="Parts",
                                 required=True)
    quantity = fields.Integer('Quantity', required=True)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id',
                             string="Unit Of Measure", required=True)
    case_id = fields.Many2one('case.management', string="Case")
    damaged_parts_case_id = fields.Many2one('case.management',
                                            string="Damaged Parts Case")

    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 required=True,
                                 default=lambda self: self.env.company)
    machine_id = fields.Many2one('account.asset', string="Machine")
    machine_domain_ids = fields.Many2many('account.asset')
    unit_price = fields.Float('Unit Price')
    location_id = fields.Many2one('stock.location', string="Source Location",
                                  required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string="Source",
                                   required=True,
                                   domain="[('location_type', '=', 'view')]")
    location_dest_id = fields.Many2one('stock.location', 'Destination location',
                                       required=True)
    move_id = fields.Many2one('stock.move', "Move")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'),
         ('cancel', 'Cancelled')],
        'Status', copy=False, default='draft')
    machine_parts_ids = fields.Many2many('product.product')
    parts_move = fields.Selection([('in', 'In'), ('out', 'Out')],
                                  string="Parts Move", required=True)
