from odoo.exceptions import UserError
from odoo import fields, models, _


class CaseManagementStage(models.Model):
    _name = "case.management.stage"
    _description = "Case Management Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage Name", required=True, translate=True)
    description = fields.Html(translate=True, sanitize_style=True)
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    unattended = fields.Boolean(string="Unattended")
    closed = fields.Boolean(string="Closed")
    mail_template_id = fields.Many2one(comodel_name="mail.template", string="Email Template",
                                       domain=[("model", "=", "case.management")],
                                       help="If set an email will be sent to the customer when the case "
                                            "reaches this step.")
    fold = fields.Boolean(string="Folded in Kanban",
                          help="This stage is folded in the kanban view when there are no records in that stage "
                               "to display.")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company)
    default = fields.Boolean('Default Stage', help="This is used to restrict the deletion of stage")

