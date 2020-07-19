# -*- coding: utf-8 -*-
from odoo import models
from webcolors import rgb_to_hex
from datetime import datetime
import base64
import io


class AttendanceXLSX(models.AbstractModel):
    _name = 'report.attendance_custom.daily_attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, attendances):
        row = 1

        # Setup sheet and data
        report_name = "DAILY ATTENDANCE REPORT"
        attendances = self.env['hr.attendance'].search([], order='department_id DESC')

        attendances = attendances.filtered(lambda attend:
                                           datetime.strptime(attend.check_in, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
                                           == data['form']['date'])
        attendances = attendances.sorted(lambda r: r.department_id.id)
        print(attendances)
        # Setup columns
        sheet = workbook.add_worksheet(report_name[:31])
        titles = workbook.add_format({'align': 'center', 'bold': True})
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 20)

        # Headings and titles
        sheet.write('E1', 'HR DEPARTMENT', titles)
        sheet.write('E2', 'DAILY ATTENDANCE REPORT', titles)
        sheet.write('E4', 'DATE : ' + data['form']['date'], titles)
        sheet.write_row('B6', ['#', 'Name', 'Job Title', 'Department', 'Enter', 'Exit', 'Worked hours'], titles)

        # Add company logo
        logo = self.env.user.sudo().company_id.logo
        imgdata = base64.b64decode(logo)
        image = io.BytesIO(imgdata)
        sheet.insert_image('B1', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image})
        sheet.insert_image('H1', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image, 'x_offset': 50})

        for obj in attendances:
            rgb_color = obj.employee_id.department_id.color
            color = rgb_to_hex(eval(rgb_color[rgb_color.index('('):rgb_color.rindex(',') - 1] + ")"))
            attendance = workbook.add_format({'bg_color': color, 'align': 'center'})
            sheet.write_row('B' + str(row + 6),
                            [row,
                             obj.employee_id.name,
                             obj.employee_id.job_id.name,
                             obj.employee_id.department_id.name,
                             datetime.strptime(obj.check_in, "%Y-%m-%d %H:%M:%S").strftime('%H:%M:%S'),
                             datetime.strptime(obj.check_out, "%Y-%m-%d %H:%M:%S").strftime('%H:%M:%S'),
                             round(obj.worked_hours, 2)],
                            attendance)
            row += 1
