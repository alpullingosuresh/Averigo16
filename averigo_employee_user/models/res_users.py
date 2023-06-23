from odoo import fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    purchase_limit = fields.Float()
    is_manager = fields.Boolean()


class HrEmployeePublicInherit(models.Model):
    _inherit = 'hr.employee.public'

    first_name = fields.Char(compute="_compute_name")
    last_name = fields.Char(compute="_compute_name")
