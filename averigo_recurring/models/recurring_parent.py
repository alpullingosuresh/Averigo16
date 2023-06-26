from odoo import models


class RecurringParent(models.TransientModel):
    _name = 'recurring.parent'

    # def create_record(self):
    #     pass

    # @api.model
    # def create(self, values):
    #     active_id = self._context.get('active_id')
    #     active_model = self._context.get('active_model')
    #     if active_id and active_model == 'transaction.recurring':
    #         recurring_id = self.env['transaction.recurring'].browse(active_id)
    #         recurring_id.filters = json.dumps(values)
    #         if 'contact_ids' in values and values['contact_ids']:
    #             recipient_ids = self.env['res.partner'].browse(values['contact_ids'][0][2])
    #             for recipient_id in recipient_ids:
    #                 if not recipient_id.email:
    #                     raise UserError(_('There is no email for the user %s') % recipient_id.name)
    #             recurring_id.write({'recipient_ids': values['contact_ids']})
    #     return super(RecurringParent, self).create(values)
