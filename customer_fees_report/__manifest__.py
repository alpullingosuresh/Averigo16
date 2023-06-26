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
    'name': 'Customer Fees Report',
    'version': '16.0.1.0',
    'category': 'Reports',
    'author': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'summary': '',
    "description": """""",
    'depends': ['base_averigo', 'averigo_reports', 'averigo_sales_order',
                'micro_market', 'stock'],
    # 'data': [
    #     'security/ir.model.access.csv',
    #     'security/security.xml',
    #     'data/data.xml',
    #     'views/customer_fees_views.xml',
    #     'views/fees_views.xml',
    #     'views/micro_market.xml',
    #     'views/product_category.xml',
    #     'views/static.xml',
    #     'wizard/wizard.xml',
    #     'wizard/location_fees_update.xml',
    #     'wizard/transaction_fees_update.xml',
    # ],
    'installable': True,
    'auto_install': False,
}
