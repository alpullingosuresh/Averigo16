from odoo import models, fields


class ICEReportWizard(models.TransientModel):
    _name = 'ice.report'

    name = fields.Char(default="Market Data Export (MDE) Report")
    division_ids = fields.Many2many('res.division', string="Divisions")
    start_date = fields.Date(string="From")
    end_date = fields.Date(string="To")
    report_length = fields.Integer(string="Report Length")
    report_lines = fields.One2many('ice.report.line', 'report_id')
    micro_market_ids = fields.Many2many('stock.warehouse', )
    categ_ids = fields.Many2many('product.category', string="Categories")


class ICEReportLines(models.TransientModel):
    _name = 'ice.report.line'

    report_id = fields.Many2one('ice.report')
    store = fields.Char(string="Store")
    mei_no = fields.Char(string="Mapping #")
    upc = fields.Char(string="UPC")
    product_name = fields.Char(string="Name")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    price = fields.Monetary(string="Price")
    initial = fields.Integer()
    fills = fields.Integer(string="Fills")
    waste = fields.Integer(string="Waste")
    sold = fields.Integer(string="Sold")
    closing = fields.Integer(string="Closing Level")
    route = fields.Char(string="Route")
    customer_no = fields.Char(string="Customer #")
    store_no = fields.Char(string="Store #")
    difference = fields.Integer()
