from odoo import fields, models


class SendReconcileReport(models.Model):
    _name = 'reconcile.report'
    to_email = fields.Char()
    app_version = fields.Char()
    session_id = fields.Char()
    market_id = fields.Many2one(
        'stock.warehouse')
    user_id = fields.Many2one(
        'res.user')
    user_email = fields.Char()
    reconciliation_ids = fields.One2many('inventory.reconcile.line',
                                         'reconciliation_id', tracking=True)
    process_status = fields.Selection(
        [('new', 'New'), ('processing', 'Ongoing'), ('done', 'Completed')],
        default='new')


class ReconcileReportStore(models.Model):
    _name = 'inventory.reconcile.line'

    reconciliation_id = fields.Many2one('reconcile.report', index=True)
    item_name = fields.Char()
    start_qty = fields.Integer()
    add_qty = fields.Integer()
    end_qty = fields.Integer()
    item_status = fields.Char()
    p_name = fields.Char()
    product_id = fields.Many2one(
        'product.product')
    process_status = fields.Selection(
        [('new', 'New'), ('processing', 'Ongoing'), ('done', 'Completed')],
        default='new')
