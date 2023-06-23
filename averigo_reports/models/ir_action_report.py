from odoo import fields, models


class IrActionsReport(models.Model):
    """ Inherited model to create fields for AveriGo report view """
    _inherit = 'ir.actions.report'

    show_in_report_menu = fields.Boolean(string="Show In Report Menu")
    show_in_portal = fields.Boolean(string="Show In Portal Report Menu")
    report_group = fields.Many2one('report.group', string="Report Group")
    action_type = fields.Char(string="Action Type")
    view_mode = fields.Selection([('tree', 'Tree'),
                                  ('form', 'Form'),
                                  ('graph', 'Graph'),
                                  ('pivot', 'Pivot'),
                                  ('calendar', 'Calendar'),
                                  ('diagram', 'Diagram'),
                                  ('gantt', 'Gantt'),
                                  ('kanban', 'Kanban'),
                                  ('search', 'Search'),
                                  ('qweb', 'QWeb')], string='Report View Mode')
    view_id = fields.Many2one('ir.ui.view', string='Report View Reference')
    target = fields.Selection(
        [('current', 'Current Window'), ('new', 'New Window'),
         ('inline', 'Inline Edit'), ('fullscreen', 'Full Screen'),
         ('main', 'Main action of Current Window')], default="current",
        string='Target Window')
    admin_report = fields.Boolean()
