# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>))
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.averigo_sales_order.models.stock_picking import StockPickingDate


def action_assign(self):
    """ Create transit picking for Delivery order"""
    res = super(StockPickingDate, self).action_assign()
    if self.delivery_order:
        if sum(self.move_ids_without_package.mapped('picking_qty')) == 0:
            raise UserError(_('Cannot Pick, Picking quantities are not given.'))
        if 'from_packslip' in self.env.context and not self.env.context.get("from_packslip"):
            picking_type = self.env['stock.picking.type'].search(
                [('warehouse_id', '=', self.warehouse_id.id), ('code', '=', 'internal')])
            vals = {
                'sale_id': self.sale_id.id,
                'origin': self.origin,
                'partner_id': self.partner_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.transit_location_id.id,
                'picking_type_id': picking_type.id,
                'delivery_order': False,
                'transit_picking': True,
                'transit_picking_id': self.id,
            }
            transit_picking = self.env['stock.picking'].create(vals)
            lines = self.move_ids_without_package
            move_line = []
            for line in lines:
                # giving value to ordered and picked qty
                line.ordered_qty = line.product_uom_qty
                line.picked_qty = line.picking_qty

                # creating transit picking move
                move_vals = {
                    'origin': line.origin,
                    'sale_line_id': line.sale_line_id.id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_uom': line.product_uom.id,
                    'product_uom_qty': line.picking_qty,
                    'picking_qty': line.picking_qty,
                    'picking_id': transit_picking.id,
                    'location_id': line.location_id.id,
                    'location_dest_id': self.transit_location_id.id,
                }
                transit_picking_move = self.env['stock.move'].create(move_vals)
                move_lines = (0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'location_id': self.transit_location_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'qty_done': line.picking_qty,
                    'picked_qty': line.picking_qty,
                })
                move_line.append(move_lines)
            transit_picking.action_confirm()
            transit_picking.action_assign()
            transit_picking.action_done()
            transit_picking.write({
                'sale_id': self.sale_id.id,
            })
            self.move_line_ids_without_package.unlink()
            self.move_line_ids_without_package = [(5, 0, 0)] + move_line
            self.state = 'assigned'
        for move_line in self.move_ids_without_package:
            move_line.state = 'assigned'
        if self.sale_id and self.picking_type_id.code == 'outgoing' and not self.transit_picking and not self.return_picking:
            account_move = self.prepare_account_move()
            account_move = self.env['account.move'].create(account_move)
            picking_lines = self.move_ids_without_package.filtered(lambda s: s.state != 'cancel')
            for line in picking_lines:
                invoice_move_line = {
                    'product_id': line.product_id.id,
                    'product_uom_id': line.sale_line_id.product_uom.id,
                    'quantity': line.sale_line_id.product_uom_qty,
                    'price_unit': line.sale_line_id.unit_price,
                    'sale_line_id': line.sale_line_id.id,
                    'container_deposit_amount': line.sale_line_id.container_amount_unit,
                    'sales_tax_amount': line.sale_line_id.tax_amount_unit,
                    'discount_amount': line.sale_line_id.discount_amount_unit,
                    'cp_code': line.sale_line_id.cp_code,
                }
                account_move.invoice_line_ids = [(0, 0, invoice_move_line), ]
                account_move._onchange_invoice_line_ids()
            service_product_invoice = self.env['account.move'].search(
                [('is_service_invoice', '=', True), ('sale_id', '=', self.sale_id.id)])
            sales_service_products = self.sale_id.order_line.filtered(lambda s: s.product_id.product_type == 'service')
            if not service_product_invoice:
                for service_product in sales_service_products:
                    service_invoice_move_line = {
                        'product_id': service_product.product_id.id,
                        'product_uom_id': service_product.product_uom.id,
                        'quantity': service_product.product_qty,
                        'price_unit': service_product.unit_price,
                        'sale_line_id': service_product.id,
                        'container_deposit_amount': service_product.container_amount_unit,
                        'sales_tax_amount': service_product.tax_amount_unit,
                        'discount_amount': service_product.discount_amount_unit,
                        'cp_code': service_product.cp_code,
                    }
                    account_move.invoice_line_ids = [(0, 0, service_invoice_move_line), ]
                    account_move._onchange_invoice_line_ids()
            tax_line = account_move.line_ids.filtered(lambda s: s.tax_line_id.id is not False)
            invoice_lines = account_move.invoice_line_ids
            container_deposit_amount = 0
            sales_tax_amount = 0
            discount_amount = 0
            for invoice_line in invoice_lines:
                container_deposit_amount += invoice_line.quantity * invoice_line.container_deposit_amount
                sales_tax_amount += invoice_line.quantity * invoice_line.sales_tax_amount
                discount_amount += invoice_line.quantity * invoice_line.discount_amount
            account_move.tax_amount_view = sales_tax_amount
            account_move.total_container_deposit = container_deposit_amount
            account_move.total_discount = discount_amount
            # extra_amount_line = {
            #     'name': 'Extra amount',
            #     'quantity': 1,
            #     'price_unit': account_move.shipping_handling + account_move.insurance - account_move.total_discount,
            #     'exclude_from_invoice_tab': True,
            #     'extra_amount_line': True,
            # }
            # account_move.invoice_line_ids = [(0, 0, extra_amount_line), ]
            # account_move._onchange_invoice_line_ids()
            discount_amount_line = {
                'name': 'Discount',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': - account_move.total_discount,
                'exclude_from_invoice_tab': True,
                'discount_amount_line': True,
                # 'account_id': discount_account_id,
            }
            # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
            account_move.invoice_line_ids = [(0, 0, discount_amount_line), ]
            account_move._onchange_invoice_line_ids()
            insurance_amount_line = {
                'name': 'Insurance',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': account_move.insurance,
                'exclude_from_invoice_tab': True,
                'insurance_amount_line': True,
                # 'account_id': insurance_account_id
            }
            # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
            account_move.invoice_line_ids = [(0, 0, insurance_amount_line), ]
            account_move._onchange_invoice_line_ids()
            shipping_handling_amount_line = {
                'name': 'S & H',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': account_move.shipping_handling,
                'exclude_from_invoice_tab': True,
                'shipping_handling_amount_line': True,
                # 'account_id': shipping_handling_account_id
            }
            # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
            account_move.invoice_line_ids = [(0, 0, shipping_handling_amount_line), ]
            account_move._onchange_invoice_line_ids()
            container_deposit_line = {
                'name': 'Container Deposit amount',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': container_deposit_amount,
                'exclude_from_invoice_tab': True,
                'container_deposit_line': True,
            }
            account_move.invoice_line_ids = [(0, 0, container_deposit_line), ]
            account_move._onchange_invoice_line_ids()
            if not tax_line:
                tax_line_val = {
                    'name': 'Tax',
                    'quantity': 1,
                    'partner_id': account_move.partner_id.id,
                    'price_unit': sales_tax_amount,
                    'exclude_from_invoice_tab': True,
                    'tax_amount_line': True,
                }
                account_move.invoice_line_ids = [(0, 0, tax_line_val), ]
                account_move._onchange_invoice_line_ids()
            container_line_edit = account_move.line_ids.filtered(lambda s: s.container_deposit_line is True)
            # extra_line_edit = account_move.line_ids.filtered(lambda s: s.extra_amount_line is True)
            discount_line_edit = account_move.line_ids.filtered(lambda s: s.discount_amount_line is True)
            insurance_line_edit = account_move.line_ids.filtered(lambda s: s.insurance_amount_line is True)
            shipping_handling_line_edit = account_move.line_ids.filtered(
                lambda s: s.shipping_handling_amount_line is True)
            tax_line_edit = account_move.line_ids.filtered(lambda s: s.tax_amount_line is True)
            invoice_line_account = account_move.invoice_line_ids
            invoice_line_account = invoice_line_account and invoice_line_account[0]
            tax_account_id = account_move.partner_id.sales_tax_liability_account_id.id
            if not tax_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.sales_tax_liability_account_id:
                    tax_account_id = default_receivable.sales_tax_liability_account_id.id
                else:
                    tax_account_id = invoice_line_account.account_id.id
            container_line_edit.account_id = tax_account_id
            # extra_line_edit.account_id = invoice_line_account.account_id
            discount_account_id = account_move.partner_id.sales_discount_account_id.id
            if not discount_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.sales_discount_account_id:
                    discount_account_id = default_receivable.sales_discount_account_id.id
                else:
                    discount_account_id = invoice_line_account.account_id.id
            discount_line_edit.account_id = discount_account_id
            insurance_account_id = account_move.partner_id.insurance_account_id.id
            if not insurance_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.insurance_account_id:
                    insurance_account_id = default_receivable.insurance_account_id.id
                else:
                    insurance_account_id = invoice_line_account.account_id.id
            insurance_line_edit.account_id = insurance_account_id
            shipping_handling_account_id = account_move.partner_id.shipping_handling_account_id.id
            if not shipping_handling_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.s_h_account_id:
                    shipping_handling_account_id = default_receivable.s_h_account_id.id
                else:
                    shipping_handling_account_id = invoice_line_account.account_id.id
            shipping_handling_line_edit.account_id = shipping_handling_account_id
            tax_line_edit.account_id = tax_account_id
            new_invoice_line = account_move.invoice_line_ids
            for new_line in new_invoice_line:
                new_line.sale_line_id.invoice_lines = [(4, new_line.id)]
            # account_move.action_post()
    if self.invoice_pick:
        lines = self.move_ids_without_package
        move_line = []
        for line in lines:
            # giving value to ordered and picked qty
            line.ordered_qty = line.product_uom_qty
            line.picked_qty = line.picking_qty
            move_lines = (0, 0, {
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'qty_done': line.picking_qty,
                'picked_qty': line.picking_qty,
            })
            move_line.append(move_lines)
        self.move_line_ids_without_package.unlink()
        self.move_line_ids_without_package = [(5, 0, 0)] + move_line
        self.state = 'assigned'
        for move_line in self.move_ids_without_package:
            move_line.state = 'assigned'
        if self.sale_id and self.picking_type_id.code == 'outgoing' and not self.transit_picking and not self.return_picking:
            account_move = self.prepare_account_move()
            account_move = self.env['account.move'].create(account_move)
            picking_lines = self.move_ids_without_package.filtered(lambda s: s.state != 'cancel')
            for line in picking_lines:
                invoice_move_line = {
                    'product_id': line.product_id.id,
                    'product_uom_id': line.sale_line_id.product_uom.id,
                    'quantity': line.sale_picking_qty,
                    'price_unit': line.sale_line_id.unit_price,
                    'sale_line_id': line.sale_line_id.id,
                    'container_deposit_amount': line.sale_line_id.container_amount_unit,
                    'sales_tax_amount': line.sale_line_id.tax_amount_unit,
                    'discount_amount': line.sale_line_id.discount_amount_unit,
                    'cp_code': line.sale_line_id.cp_code,
                }
                account_move.invoice_line_ids = [(0, 0, invoice_move_line), ]
                account_move._onchange_invoice_line_ids()
            service_product_invoice = self.env['account.move'].search(
                [('is_service_invoice', '=', True), ('sale_id', '=', self.sale_id.id)])
            sales_service_products = self.sale_id.order_line.filtered(lambda s: s.product_id.product_type == 'service')
            if not service_product_invoice:
                for service_product in sales_service_products:
                    service_invoice_move_line = {
                        'product_id': service_product.product_id.id,
                        'product_uom_id': service_product.product_uom.id,
                        'quantity': service_product.product_qty,
                        'price_unit': service_product.unit_price,
                        'sale_line_id': service_product.id,
                        'container_deposit_amount': service_product.container_amount_unit,
                        'sales_tax_amount': service_product.tax_amount_unit,
                        'discount_amount': service_product.discount_amount_unit,
                        'cp_code': service_product.cp_code,
                    }
                    account_move.invoice_line_ids = [(0, 0, service_invoice_move_line), ]
                    account_move._onchange_invoice_line_ids()
            tax_line = account_move.line_ids.filtered(lambda s: s.tax_line_id.id is not False)
            invoice_lines = account_move.invoice_line_ids
            container_deposit_amount = 0
            sales_tax_amount = 0
            discount_amount = 0
            for invoice_line in invoice_lines:
                container_deposit_amount += invoice_line.quantity * invoice_line.container_deposit_amount
                sales_tax_amount += invoice_line.quantity * invoice_line.sales_tax_amount
                discount_amount += invoice_line.quantity * invoice_line.discount_amount
            account_move.tax_amount_view = sales_tax_amount
            account_move.total_container_deposit = container_deposit_amount
            account_move.total_discount = discount_amount
            # extra_amount_line = {
            #     'name': 'Extra amount',
            #     'quantity': 1,
            #     'price_unit': account_move.shipping_handling + account_move.insurance - account_move.total_discount,
            #     'exclude_from_invoice_tab': True,
            #     'extra_amount_line': True,
            # }
            # account_move.invoice_line_ids = [(0, 0, extra_amount_line), ]
            # account_move._onchange_invoice_line_ids()
            discount_amount_line = {
                'name': 'Discount',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': - account_move.total_discount,
                'exclude_from_invoice_tab': True,
                'discount_amount_line': True,
                # 'account_id': discount_account_id,
            }
            # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
            account_move.invoice_line_ids = [(0, 0, discount_amount_line), ]
            account_move._onchange_invoice_line_ids()
            insurance_amount_line = {
                'name': 'Insurance',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': account_move.insurance,
                'exclude_from_invoice_tab': True,
                'insurance_amount_line': True,
                # 'account_id': insurance_account_id
            }
            # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
            account_move.invoice_line_ids = [(0, 0, insurance_amount_line), ]
            account_move._onchange_invoice_line_ids()
            shipping_handling_amount_line = {
                'name': 'S & H',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': account_move.shipping_handling,
                'exclude_from_invoice_tab': True,
                'shipping_handling_amount_line': True,
                # 'account_id': shipping_handling_account_id
            }
            # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
            account_move.invoice_line_ids = [(0, 0, shipping_handling_amount_line), ]
            account_move._onchange_invoice_line_ids()
            container_deposit_line = {
                'name': 'Container Deposit amount',
                'quantity': 1,
                'partner_id': account_move.partner_id.id,
                'price_unit': container_deposit_amount,
                'exclude_from_invoice_tab': True,
                'container_deposit_line': True,
            }
            account_move.invoice_line_ids = [(0, 0, container_deposit_line), ]
            account_move._onchange_invoice_line_ids()
            if not tax_line:
                tax_line_val = {
                    'name': 'Tax',
                    'quantity': 1,
                    'partner_id': account_move.partner_id.id,
                    'price_unit': sales_tax_amount,
                    'exclude_from_invoice_tab': True,
                    'tax_amount_line': True,
                }
                account_move.invoice_line_ids = [(0, 0, tax_line_val), ]
                account_move._onchange_invoice_line_ids()
            container_line_edit = account_move.line_ids.filtered(lambda s: s.container_deposit_line is True)
            # extra_line_edit = account_move.line_ids.filtered(lambda s: s.extra_amount_line is True)
            discount_line_edit = account_move.line_ids.filtered(lambda s: s.discount_amount_line is True)
            insurance_line_edit = account_move.line_ids.filtered(lambda s: s.insurance_amount_line is True)
            shipping_handling_line_edit = account_move.line_ids.filtered(
                lambda s: s.shipping_handling_amount_line is True)
            tax_line_edit = account_move.line_ids.filtered(lambda s: s.tax_amount_line is True)
            invoice_line_account = account_move.invoice_line_ids
            invoice_line_account = invoice_line_account and invoice_line_account[0]
            tax_account_id = account_move.partner_id.sales_tax_liability_account_id.id
            if not tax_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.sales_tax_liability_account_id:
                    tax_account_id = default_receivable.sales_tax_liability_account_id.id
                else:
                    tax_account_id = invoice_line_account.account_id.id
            container_line_edit.account_id = tax_account_id
            # extra_line_edit.account_id = invoice_line_account.account_id
            discount_account_id = account_move.partner_id.sales_discount_account_id.id
            if not discount_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.sales_discount_account_id:
                    discount_account_id = default_receivable.sales_discount_account_id.id
                else:
                    discount_account_id = invoice_line_account.account_id.id
            discount_line_edit.account_id = discount_account_id
            insurance_account_id = account_move.partner_id.insurance_account_id.id
            if not insurance_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.insurance_account_id:
                    insurance_account_id = default_receivable.insurance_account_id.id
                else:
                    insurance_account_id = invoice_line_account.account_id.id
            insurance_line_edit.account_id = insurance_account_id
            shipping_handling_account_id = account_move.partner_id.shipping_handling_account_id.id
            if not shipping_handling_account_id:
                default_receivable = self.env['default.receivable'].search(
                    [('operator_id', '=', self.env.company.id)])
                if default_receivable.s_h_account_id:
                    shipping_handling_account_id = default_receivable.s_h_account_id.id
                else:
                    shipping_handling_account_id = invoice_line_account.account_id.id
            shipping_handling_line_edit.account_id = shipping_handling_account_id
            tax_line_edit.account_id = tax_account_id
            new_invoice_line = account_move.invoice_line_ids
            for new_line in new_invoice_line:
                new_line.sale_line_id.invoice_lines = [(4, new_line.id)]
            account_move.action_post()
    return res


StockPickingDate.action_assign = action_assign


# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#
#     def action_assign(self):
#         """ Create transit picking for Delivery order"""
#         res = super(StockPicking, self).action_assign()
#         if self.delivery_order:
#             if sum(self.move_ids_without_package.mapped('picking_qty')) == 0:
#                 raise UserError(_('Cannot Pick, Picking quantities are not given.'))
#             picking_type = self.env['stock.picking.type'].search(
#                 [('warehouse_id', '=', self.warehouse_id.id), ('code', '=', 'internal')])
#             vals = {
#                 'sale_id': self.sale_id.id,
#                 'origin': self.origin,
#                 'partner_id': self.partner_id.id,
#                 'location_id': self.location_id.id,
#                 'location_dest_id': self.transit_location_id.id,
#                 'picking_type_id': picking_type.id,
#                 'delivery_order': False,
#                 'transit_picking': True,
#                 'transit_picking_id': self.id,
#             }
#             transit_picking = self.env['stock.picking'].create(vals)
#             lines = self.move_ids_without_package
#             move_line = []
#             for line in lines:
#                 # giving value to ordered and picked qty
#                 line.ordered_qty = line.product_uom_qty
#                 line.picked_qty = line.picking_qty
#
#                 # creating transit picking move
#                 move_vals = {
#                     'origin': line.origin,
#                     'sale_line_id': line.sale_line_id.id,
#                     'product_id': line.product_id.id,
#                     'name': line.name,
#                     'product_uom': line.product_uom.id,
#                     'product_uom_qty': line.picking_qty,
#                     'picking_qty': line.picking_qty,
#                     'picking_id': transit_picking.id,
#                     'location_id': line.location_id.id,
#                     'location_dest_id': self.transit_location_id.id,
#                 }
#                 transit_picking_move = self.env['stock.move'].create(move_vals)
#                 move_lines = (0, 0, {
#                     'product_id': line.product_id.id,
#                     'product_uom_id': line.product_uom.id,
#                     'location_id': self.transit_location_id.id,
#                     'location_dest_id': self.location_dest_id.id,
#                     'qty_done': line.picking_qty,
#                     'picked_qty': line.picking_qty,
#                 })
#                 move_line.append(move_lines)
#             transit_picking.action_confirm()
#             transit_picking.action_assign()
#             transit_picking.action_done()
#             transit_picking.write({
#                 'sale_id': self.sale_id.id,
#             })
#             self.move_line_ids_without_package.unlink()
#             self.move_line_ids_without_package = [(5, 0, 0)] + move_line
#             self.state = 'assigned'
#             for move_line in self.move_ids_without_package:
#                 move_line.state = 'assigned'
#             if self.sale_id and self.picking_type_id.code == 'outgoing' and not self.transit_picking and not self.return_picking:
#                 account_move = self.prepare_account_move()
#                 account_move = self.env['account.move'].create(account_move)
#                 picking_lines = self.move_ids_without_package.filtered(lambda s: s.state != 'cancel')
#                 for line in picking_lines:
#                     invoice_move_line = {
#                         'product_id': line.product_id.id,
#                         'product_uom_id': line.sale_line_id.product_uom.id,
#                         'quantity': line.sale_line_id.product_uom_qty,
#                         'price_unit': line.sale_line_id.unit_price,
#                         'sale_line_id': line.sale_line_id.id,
#                         'container_deposit_amount': line.sale_line_id.container_amount_unit,
#                         'sales_tax_amount': line.sale_line_id.tax_amount_unit,
#                         'discount_amount': line.sale_line_id.discount_amount_unit,
#                         'cp_code': line.sale_line_id.cp_code,
#                     }
#                     account_move.invoice_line_ids = [(0, 0, invoice_move_line), ]
#                     account_move._onchange_invoice_line_ids()
#                 service_product_invoice = self.env['account.move'].search(
#                     [('is_service_invoice', '=', True), ('sale_id', '=', self.sale_id.id)])
#                 sales_service_products = self.sale_id.order_line.filtered(lambda s: s.product_id.product_type == 'service')
#                 if not service_product_invoice:
#                     for service_product in sales_service_products:
#                         service_invoice_move_line = {
#                             'product_id': service_product.product_id.id,
#                             'product_uom_id': service_product.product_uom.id,
#                             'quantity': service_product.product_qty,
#                             'price_unit': service_product.unit_price,
#                             'sale_line_id': service_product.id,
#                             'container_deposit_amount': service_product.container_amount_unit,
#                             'sales_tax_amount': service_product.tax_amount_unit,
#                             'discount_amount': service_product.discount_amount_unit,
#                             'cp_code': service_product.cp_code,
#                         }
#                         account_move.invoice_line_ids = [(0, 0, service_invoice_move_line), ]
#                         account_move._onchange_invoice_line_ids()
#                 tax_line = account_move.line_ids.filtered(lambda s: s.tax_line_id.id is not False)
#                 invoice_lines = account_move.invoice_line_ids
#                 container_deposit_amount = 0
#                 sales_tax_amount = 0
#                 discount_amount = 0
#                 for invoice_line in invoice_lines:
#                     container_deposit_amount += invoice_line.quantity * invoice_line.container_deposit_amount
#                     sales_tax_amount += invoice_line.quantity * invoice_line.sales_tax_amount
#                     discount_amount += invoice_line.quantity * invoice_line.discount_amount
#                 account_move.tax_amount_view = sales_tax_amount
#                 account_move.total_container_deposit = container_deposit_amount
#                 account_move.total_discount = discount_amount
#                 # extra_amount_line = {
#                 #     'name': 'Extra amount',
#                 #     'quantity': 1,
#                 #     'price_unit': account_move.shipping_handling + account_move.insurance - account_move.total_discount,
#                 #     'exclude_from_invoice_tab': True,
#                 #     'extra_amount_line': True,
#                 # }
#                 # account_move.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 # account_move._onchange_invoice_line_ids()
#                 discount_amount_line = {
#                     'name': 'Discount',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': - account_move.total_discount,
#                     'exclude_from_invoice_tab': True,
#                     'discount_amount_line': True,
#                     # 'account_id': discount_account_id,
#                 }
#                 # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 account_move.invoice_line_ids = [(0, 0, discount_amount_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 insurance_amount_line = {
#                     'name': 'Insurance',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': account_move.insurance,
#                     'exclude_from_invoice_tab': True,
#                     'insurance_amount_line': True,
#                     # 'account_id': insurance_account_id
#                 }
#                 # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 account_move.invoice_line_ids = [(0, 0, insurance_amount_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 shipping_handling_amount_line = {
#                     'name': 'S & H',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': account_move.shipping_handling,
#                     'exclude_from_invoice_tab': True,
#                     'shipping_handling_amount_line': True,
#                     # 'account_id': shipping_handling_account_id
#                 }
#                 # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 account_move.invoice_line_ids = [(0, 0, shipping_handling_amount_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 container_deposit_line = {
#                     'name': 'Container Deposit amount',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': container_deposit_amount,
#                     'exclude_from_invoice_tab': True,
#                     'container_deposit_line': True,
#                 }
#                 account_move.invoice_line_ids = [(0, 0, container_deposit_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 if not tax_line:
#                     tax_line_val = {
#                         'name': 'Tax',
#                         'quantity': 1,
#                         'partner_id': account_move.partner_id.id,
#                         'price_unit': sales_tax_amount,
#                         'exclude_from_invoice_tab': True,
#                         'tax_amount_line': True,
#                     }
#                     account_move.invoice_line_ids = [(0, 0, tax_line_val), ]
#                     account_move._onchange_invoice_line_ids()
#                 container_line_edit = account_move.line_ids.filtered(lambda s: s.container_deposit_line is True)
#                 # extra_line_edit = account_move.line_ids.filtered(lambda s: s.extra_amount_line is True)
#                 discount_line_edit = account_move.line_ids.filtered(lambda s: s.discount_amount_line is True)
#                 insurance_line_edit = account_move.line_ids.filtered(lambda s: s.insurance_amount_line is True)
#                 shipping_handling_line_edit = account_move.line_ids.filtered(
#                     lambda s: s.shipping_handling_amount_line is True)
#                 tax_line_edit = account_move.line_ids.filtered(lambda s: s.tax_amount_line is True)
#                 invoice_line_account = account_move.invoice_line_ids
#                 invoice_line_account = invoice_line_account and invoice_line_account[0]
#                 tax_account_id = account_move.partner_id.sales_tax_liability_account_id.id
#                 if not tax_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.sales_tax_liability_account_id:
#                         tax_account_id = default_receivable.sales_tax_liability_account_id.id
#                     else:
#                         tax_account_id = invoice_line_account.account_id.id
#                 container_line_edit.account_id = tax_account_id
#                 # extra_line_edit.account_id = invoice_line_account.account_id
#                 discount_account_id = account_move.partner_id.sales_discount_account_id.id
#                 if not discount_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.sales_discount_account_id:
#                         discount_account_id = default_receivable.sales_discount_account_id.id
#                     else:
#                         discount_account_id = invoice_line_account.account_id.id
#                 discount_line_edit.account_id = discount_account_id
#                 insurance_account_id = account_move.partner_id.insurance_account_id.id
#                 if not insurance_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.insurance_account_id:
#                         insurance_account_id = default_receivable.insurance_account_id.id
#                     else:
#                         insurance_account_id = invoice_line_account.account_id.id
#                 insurance_line_edit.account_id = insurance_account_id
#                 shipping_handling_account_id = account_move.partner_id.shipping_handling_account_id.id
#                 if not shipping_handling_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.s_h_account_id:
#                         shipping_handling_account_id = default_receivable.s_h_account_id.id
#                     else:
#                         shipping_handling_account_id = invoice_line_account.account_id.id
#                 shipping_handling_line_edit.account_id = shipping_handling_account_id
#                 tax_line_edit.account_id = tax_account_id
#                 new_invoice_line = account_move.invoice_line_ids
#                 for new_line in new_invoice_line:
#                     new_line.sale_line_id.invoice_lines = [(4, new_line.id)]
#                 # account_move.action_post()
#         if self.invoice_pick:
#             lines = self.move_ids_without_package
#             move_line = []
#             for line in lines:
#                 # giving value to ordered and picked qty
#                 line.ordered_qty = line.product_uom_qty
#                 line.picked_qty = line.picking_qty
#                 move_lines = (0, 0, {
#                     'product_id': line.product_id.id,
#                     'product_uom_id': line.product_uom.id,
#                     'location_id': self.location_id.id,
#                     'location_dest_id': self.location_dest_id.id,
#                     'qty_done': line.picking_qty,
#                     'picked_qty': line.picking_qty,
#                 })
#                 move_line.append(move_lines)
#             self.move_line_ids_without_package.unlink()
#             self.move_line_ids_without_package = [(5, 0, 0)] + move_line
#             self.state = 'assigned'
#             for move_line in self.move_ids_without_package:
#                 move_line.state = 'assigned'
#             if self.sale_id and self.picking_type_id.code == 'outgoing' and not self.transit_picking and not self.return_picking:
#                 account_move = self.prepare_account_move()
#                 account_move = self.env['account.move'].create(account_move)
#                 picking_lines = self.move_ids_without_package.filtered(lambda s: s.state != 'cancel')
#                 for line in picking_lines:
#                     invoice_move_line = {
#                         'product_id': line.product_id.id,
#                         'product_uom_id': line.product_uom.id,
#                         'quantity': line.picked_qty,
#                         'price_unit': line.sale_line_id.unit_price,
#                         'sale_line_id': line.sale_line_id.id,
#                         'container_deposit_amount': line.sale_line_id.container_amount_unit,
#                         'sales_tax_amount': line.sale_line_id.tax_amount_unit,
#                         'discount_amount': line.sale_line_id.discount_amount_unit,
#                         'cp_code': line.sale_line_id.cp_code,
#                     }
#                     account_move.invoice_line_ids = [(0, 0, invoice_move_line), ]
#                     account_move._onchange_invoice_line_ids()
#                 service_product_invoice = self.env['account.move'].search(
#                     [('is_service_invoice', '=', True), ('sale_id', '=', self.sale_id.id)])
#                 sales_service_products = self.sale_id.order_line.filtered(lambda s: s.product_id.product_type == 'service')
#                 if not service_product_invoice:
#                     for service_product in sales_service_products:
#                         service_invoice_move_line = {
#                             'product_id': service_product.product_id.id,
#                             'product_uom_id': service_product.product_uom.id,
#                             'quantity': service_product.product_qty,
#                             'price_unit': service_product.unit_price,
#                             'sale_line_id': service_product.id,
#                             'container_deposit_amount': service_product.container_amount_unit,
#                             'sales_tax_amount': service_product.tax_amount_unit,
#                             'discount_amount': service_product.discount_amount_unit,
#                             'cp_code': service_product.cp_code,
#                         }
#                         account_move.invoice_line_ids = [(0, 0, service_invoice_move_line), ]
#                         account_move._onchange_invoice_line_ids()
#                 tax_line = account_move.line_ids.filtered(lambda s: s.tax_line_id.id is not False)
#                 invoice_lines = account_move.invoice_line_ids
#                 container_deposit_amount = 0
#                 sales_tax_amount = 0
#                 discount_amount = 0
#                 for invoice_line in invoice_lines:
#                     container_deposit_amount += invoice_line.quantity * invoice_line.container_deposit_amount
#                     sales_tax_amount += invoice_line.quantity * invoice_line.sales_tax_amount
#                     discount_amount += invoice_line.quantity * invoice_line.discount_amount
#                 account_move.tax_amount_view = sales_tax_amount
#                 account_move.total_container_deposit = container_deposit_amount
#                 account_move.total_discount = discount_amount
#                 # extra_amount_line = {
#                 #     'name': 'Extra amount',
#                 #     'quantity': 1,
#                 #     'price_unit': account_move.shipping_handling + account_move.insurance - account_move.total_discount,
#                 #     'exclude_from_invoice_tab': True,
#                 #     'extra_amount_line': True,
#                 # }
#                 # account_move.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 # account_move._onchange_invoice_line_ids()
#                 discount_amount_line = {
#                     'name': 'Discount',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': - account_move.total_discount,
#                     'exclude_from_invoice_tab': True,
#                     'discount_amount_line': True,
#                     # 'account_id': discount_account_id,
#                 }
#                 # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 account_move.invoice_line_ids = [(0, 0, discount_amount_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 insurance_amount_line = {
#                     'name': 'Insurance',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': account_move.insurance,
#                     'exclude_from_invoice_tab': True,
#                     'insurance_amount_line': True,
#                     # 'account_id': insurance_account_id
#                 }
#                 # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 account_move.invoice_line_ids = [(0, 0, insurance_amount_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 shipping_handling_amount_line = {
#                     'name': 'S & H',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': account_move.shipping_handling,
#                     'exclude_from_invoice_tab': True,
#                     'shipping_handling_amount_line': True,
#                     # 'account_id': shipping_handling_account_id
#                 }
#                 # self.invoice_line_ids = [(0, 0, extra_amount_line), ]
#                 account_move.invoice_line_ids = [(0, 0, shipping_handling_amount_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 container_deposit_line = {
#                     'name': 'Container Deposit amount',
#                     'quantity': 1,
#                     'partner_id': account_move.partner_id.id,
#                     'price_unit': container_deposit_amount,
#                     'exclude_from_invoice_tab': True,
#                     'container_deposit_line': True,
#                 }
#                 account_move.invoice_line_ids = [(0, 0, container_deposit_line), ]
#                 account_move._onchange_invoice_line_ids()
#                 if not tax_line:
#                     tax_line_val = {
#                         'name': 'Tax',
#                         'quantity': 1,
#                         'partner_id': account_move.partner_id.id,
#                         'price_unit': sales_tax_amount,
#                         'exclude_from_invoice_tab': True,
#                         'tax_amount_line': True,
#                     }
#                     account_move.invoice_line_ids = [(0, 0, tax_line_val), ]
#                     account_move._onchange_invoice_line_ids()
#                 container_line_edit = account_move.line_ids.filtered(lambda s: s.container_deposit_line is True)
#                 # extra_line_edit = account_move.line_ids.filtered(lambda s: s.extra_amount_line is True)
#                 discount_line_edit = account_move.line_ids.filtered(lambda s: s.discount_amount_line is True)
#                 insurance_line_edit = account_move.line_ids.filtered(lambda s: s.insurance_amount_line is True)
#                 shipping_handling_line_edit = account_move.line_ids.filtered(
#                     lambda s: s.shipping_handling_amount_line is True)
#                 tax_line_edit = account_move.line_ids.filtered(lambda s: s.tax_amount_line is True)
#                 invoice_line_account = account_move.invoice_line_ids
#                 invoice_line_account = invoice_line_account and invoice_line_account[0]
#                 tax_account_id = account_move.partner_id.sales_tax_liability_account_id.id
#                 if not tax_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.sales_tax_liability_account_id:
#                         tax_account_id = default_receivable.sales_tax_liability_account_id.id
#                     else:
#                         tax_account_id = invoice_line_account.account_id.id
#                 container_line_edit.account_id = tax_account_id
#                 # extra_line_edit.account_id = invoice_line_account.account_id
#                 discount_account_id = account_move.partner_id.sales_discount_account_id.id
#                 if not discount_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.sales_discount_account_id:
#                         discount_account_id = default_receivable.sales_discount_account_id.id
#                     else:
#                         discount_account_id = invoice_line_account.account_id.id
#                 discount_line_edit.account_id = discount_account_id
#                 insurance_account_id = account_move.partner_id.insurance_account_id.id
#                 if not insurance_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.insurance_account_id:
#                         insurance_account_id = default_receivable.insurance_account_id.id
#                     else:
#                         insurance_account_id = invoice_line_account.account_id.id
#                 insurance_line_edit.account_id = insurance_account_id
#                 shipping_handling_account_id = account_move.partner_id.shipping_handling_account_id.id
#                 if not shipping_handling_account_id:
#                     default_receivable = self.env['default.receivable'].search(
#                         [('operator_id', '=', self.env.company.id)])
#                     if default_receivable.s_h_account_id:
#                         shipping_handling_account_id = default_receivable.s_h_account_id.id
#                     else:
#                         shipping_handling_account_id = invoice_line_account.account_id.id
#                 shipping_handling_line_edit.account_id = shipping_handling_account_id
#                 tax_line_edit.account_id = tax_account_id
#                 new_invoice_line = account_move.invoice_line_ids
#                 for new_line in new_invoice_line:
#                     new_line.sale_line_id.invoice_lines = [(4, new_line.id)]
#                 account_move.action_post()
#         return res
