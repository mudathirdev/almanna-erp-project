# -*- coding: utf-8 -*-
{
    'name': 'Sales Plan Report',
    'version': '11.0.1.0.0',
    'summary': 'Sales plan report',
    'author': 'Bashier Mustafa',
    'depends': ['sale'],
    'category': 'Sales',
    'demo': [],
    'data': ['views/stock_expiry_views.xml',
             'security/ir.model.access.csv',
             'report/stock_expiry_report.xml',
             'report/stock_report_template.xml'],
    'installable': True,
    'qweb': [],
}
