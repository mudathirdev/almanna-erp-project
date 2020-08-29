# -*- coding: utf-8 -*-
import base64
import io
from datetime import datetime

from webcolors import rgb_to_hex

from odoo import models
from odoo.fields import Datetime as ODT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class AbsenceXLSX(models.AbstractModel):
    _name = 'report.attendance_custom.daily_absence_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, attendances):
        row = 1

        # Setup sheet and data
        report_name = datetime.today().strftime("%Y-%m-%d") + "DAILY ABSENCE REPORT"
        attendances = self.env['zk.machine.attendance'].search([])

        attendances = attendances.filtered(lambda attend:
                                           ODT.context_timestamp(attend,
                                                                 ODT.from_string(attend.punching_time)).strftime(
                                               '%Y-%m-%d')
                                           == data['form']['date'])

        employees = self.env['hr.employee'].sudo().search([])
        employees = employees.filtered(lambda e: e.id not in attendances.mapped('employee_id.id'))
        employees = employees.sorted(lambda e: e.department_id.sequence if e.department_id else 1000)

        # Setup columns
        sheet = workbook.add_worksheet(report_name[:31])
        titles = workbook.add_format({'align': 'center', 'bold': True})
        t_heading = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#BD5B5B', 'border': 1})
        sheet.set_column('C:C', 35)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 35)

        # Headings and titles
        sheet.merge_range(0, 1, 0, 4, 'HR DEPARTMENT', titles)
        sheet.merge_range(1, 1, 1, 4, 'DAILY ABSENCE REPORT', titles)
        sheet.merge_range(3, 1, 3, 4, 'DATE : ' + data['form']['date'], titles)
        sheet.write_row('B6', ['Emp ID', 'Name', 'Job Title', 'Department'], t_heading)

        for obj in employees:
            rgb_color = obj.department_id.color
            color = '#FFFFFF'
            if not rgb_color:
                rgb_color = "rgba(255,0,0,1)"
            if len(rgb_color) > 1:
                color = rgb_to_hex(eval(rgb_color[rgb_color.index('('):rgb_color.rindex(',')] + ")"))
            color = color.upper()
            emp_id = workbook.add_format({'bg_color': '#F09481', 'align': 'center', 'border': 1})
            attendance = workbook.add_format({'bg_color': color, 'align': 'center', 'border': 1})
            sheet.write_row('B' + str(row + 6), [row], emp_id)
            sheet.write_row('C' + str(row + 6),
                            [obj.name,
                             obj.job_id.name or '-',
                             obj.department_id.name or '-'], attendance)
            row += 1
