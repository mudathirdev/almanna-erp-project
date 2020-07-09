# -*- coding: utf-8 -*-
{
    'name': "PDC",

    'summary': """
        PDC Management""",

    'description': """
        This module allows you to manage customers and vendors post-dated checks
    """,

    'author': "Ahmed Ebaid",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_pdc_view.xml',
        'views/account_payment_view.xml',
        'wizard/invoice_payment_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
