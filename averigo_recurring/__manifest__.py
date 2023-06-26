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
    'name': 'AveriGo Recurring',
    'version': '16.0.1.0.0',
    'category': 'Tools',
    'author': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'summary': '',
    "description": """Averigo Recurring""",
    'depends': ['base', 'base_averigo', 'averigo_sales_order', 'mail',
                'averigo_transaction_report'],
    # 'data': [
    #     'security/ir.model.access.csv',
    #     'security/data.xml',
    #     'security/security.xml',
    #     'views/averigo_recurring.xml',
    #     'views/sale_order.xml',
    #     'views/purchase_order.xml',
    #     'views/account_move.xml',
    #     'views/res_partner.xml',
    #     'views/stock_warehouse_views.xml',
    #     'views/recurring_view.xml',
    #     'views/dashboard_view.xml',
    # ],
    # 'qweb': [
    #     "static/src/xml/recurring_dashboard.xml"
    # ],
    'installable': True,
    'auto_install': False,
}
