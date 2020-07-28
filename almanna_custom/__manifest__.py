# -*- coding: utf-8 -*-
{
    'name': "Almanna Special Customization",

    'summary': """
       Almanna Special Customization""",

    'description': """
        Almanna Special Customization
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','sale_stock','stock','contacts','hr','purchase'],

    # always loaded
    'data': [
	'security/almanna_security.xml',
    'data/almanna_data.xml',
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/stock_views.xml',
        'views/invoice_views.xml',
        'views/hr_views.xml',
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
