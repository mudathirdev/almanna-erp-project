# -*- coding: utf-8 -*-
{
    'name': "Attendance Custom",

    'summary': """
        Attendance Custom.
    """,

    'author': "Mudathir",

    # for the full list
    'category': 'Human Resources',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web_widget_colorpicker', 'report_xlsx', 'hr', 'hr_zk_attendance'],
    'external_dependencies': {'python': ['webcolors']},
    # always loaded
    'data': [
        'views/hr_department.xml',
        'wizards/daily_attendance_report_wizard_views.xml',
        'wizards/periodic_attendance_report_wizard_views.xml',
        'wizards/biometric_daily_attendance_report_wizard_views.xml',
        'wizards/biometric_periodic_attendance_report_wizard_views.xml',
        'reports/daily_attendance_report.xml',
        'reports/periodic_attendance_report.xml',
        'reports/biometric_daily_attendance_report.xml',
        'reports/biometric_periodic_attendance_report.xml'
    ],
}
