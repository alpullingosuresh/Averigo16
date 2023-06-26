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


{
    'name': 'AveriGo Security',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'summary': '',
    "description": """""",
    'depends': ['base', 'base_averigo', 'averigo_sales_order',
                'averigo_marketing_campaign', 'averigo_crm',
                'averigo_portal_user', 'single_product_master', 'micro_market',
                'sendgrid_email', 'quick_update',
                'front_desk', 'averigo_payroll_credit', 'web_service',
                'averigo_purchase', 'averigo_accounting',
                'master_search', 'averigo_product_opening_stock',
                'averigo_featured_products',
                'averigo_app_featured_products', 'averigo_delivery_schedule',
                'averigo_create_not_exist',
                'averigo_recurring', 'averigo_sales_return'],
    # 'data': [
    #     'security/security.xml',
    #     'security/ir.model.access.csv',
    #     'data/data.xml',
    #     'views/res_groups.xml',
    #     'views/ir_ui_menu.xml',
    #     'views/invoice_views.xml',
    #     'views/crm_views.xml',
    #     'views/followers_views.xml',
    #     'wizard/wizard_view.xml',
    #     'views/res_users.xml',
    #     'views/ir_ui_menu_view.xml',
    # ],
    'installable': True,
    'auto_install': False,
}
