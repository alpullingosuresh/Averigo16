from odoo import models, fields


class FrontDesk(models.Model):
    _inherit = 'front.desk'

    import_file = fields.Binary('File', required=True)
    file_name = fields.Char()
    extension = fields.Char()
    add_existing = fields.Selection(
        [('link', 'Link It'), ('skip', 'Skip It'), ('error', 'Let me know')],
        string="If Found Duplicates", default='link')


class PrepaidPurchase(models.Model):
    _inherit = 'prepaid.purchase'

    import_file = fields.Binary('File', required=True)
    file_name = fields.Char()
    extension = fields.Char()
    add_existing = fields.Selection(
        [('link', 'Link It'), ('skip', 'Skip It'), ('error', 'Let me know')],
        string="If Found Duplicates", default='link')


class ResAppUsers(models.Model):
    _inherit = 'res.app.users'

    is_imported = fields.Boolean()
