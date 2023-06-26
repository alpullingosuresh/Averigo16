{
    "name": "Averigo Delivery Scheduling",
    "summary": "Averigo Accounting",
    "version": "13.0.0.1",
    "category": "",
    "website": "http://www.cybrosys.com",
    "description": """Averigo Delivery Scheduling""",
    "author": "Cybrosys Techno Solutions Pvt Ltd.",
    "license": "LGPL-3",
    "depends": [
        'base', 'base_averigo', 'calendar', 'averigo_sales_order',
        'averigo_crm',
    ],
    # "data": [
    #     'security/ir.model.access.csv',
    #     'security/security.xml',
    #     'views/delivery_schedule.xml',
    #     'views/res_partner.xml',
    #     'views/assets.xml',
    # ],
    # 'qweb': ['static/src/xml/delivery_calendar.xml'],
    "installable": True,
    "application": True,
}
