{
    'name': 'Custody Request',
    'version': '1.0',
    'author': 'Abdelwhab ALim',
    'data': [

        'security/security_view.xml',
        'security/ir.model.access.csv',
        'views/custody_request_view.xml',
        'views/employee_view.xml',
        'reports/custody_report.xml',
    ],
    'depends': ['base','hr','account','hr_payroll','analytic',],




    'installable': True,
    'application': True,






}
