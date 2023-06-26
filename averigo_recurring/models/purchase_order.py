from lxml import etree
from odoo.addons.base.models.ir_ui_view import (
    transfer_field_to_modifiers, transfer_node_to_modifiers, transfer_modifiers_to_node,
)

from odoo import models, fields, api


def setup_modifiers(node, field=None, context=None, in_tree_view=False):
    modifiers = {}
    if field is not None:
        transfer_field_to_modifiers(field, modifiers)
    transfer_node_to_modifiers(
        node, modifiers, context=context, in_tree_view=in_tree_view)
    transfer_modifiers_to_node(modifiers, node)


class PurchaseOrderRecurring(models.Model):
    _inherit = 'purchase.order'

    purchase_recurring = fields.One2many('transaction.recurring', 'purchase_id', string="Recurring")
    is_recurring = fields.Boolean('Is Recurring', default=False, copy=False)
    is_recurring_transaction = fields.Boolean('Is Recurring', default=False, copy=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(PurchaseOrderRecurring, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                              submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            recurring_groups = self.env['res.groups'].search([('averigo_group_check', '=', True)])
            recurring_menu = self.env.ref('averigo_recurring.menu_purchase_recurring')
            current_user = self.env.uid
            menu_access_all = []
            user_access_all = []
            for recurring_group in recurring_groups:
                menu_access = recurring_group.mapped('menu_access').ids
                menu_access_all.extend(menu_access)
                user_access = recurring_group.mapped('users').ids
                user_access_all.extend(user_access)
            if recurring_menu.id not in menu_access_all and current_user in user_access_all:
                for node in doc.xpath("//field[@name='is_recurring']"):
                    node.set('invisible', '1')
                    setup_modifiers(node)
                for node in doc.xpath("//label[@for='is_recurring']"):
                    node.set('invisible', '1')
                    setup_modifiers(node)
            if recurring_menu.id in menu_access_all and current_user in user_access_all:
                for node in doc.xpath("//field[@name='is_recurring']"):
                    node.set('invisible', '0')
                    setup_modifiers(node)
                for node in doc.xpath("//label[@for='is_recurring']"):
                    node.set('invisible', '0')
                    setup_modifiers(node)
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res