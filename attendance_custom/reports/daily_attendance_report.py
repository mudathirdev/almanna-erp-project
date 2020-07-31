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
        report_name = datetime.today().strftime("%Y-%m-%d") + "DAILY ATTENDANCE REPORT"
        attendances = self.env['hr.attendance'].search([])

        attendances = attendances.filtered(lambda attend:
                                           datetime.strptime(attend.check_in, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
                                           == data['form']['date'])
        attendances = attendances.sorted(lambda r: r.department_id.id)

        # Setup columns
        sheet = workbook.add_worksheet(report_name[:31])
        titles = workbook.add_format({'align': 'center', 'bold': True})
        t_heading = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#BD5B5B', 'border': 1})
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
        sheet.write_row('B6', ['Emp ID', 'Name', 'Job Title', 'Department', 'Enter', 'Exit', 'Worked hours'], t_heading)

        # Add company logo
        logo = self.env.user.sudo().company_id.logo
        imgdata = base64.b64decode(logo)
        image = io.BytesIO(imgdata)
        sheet.insert_image('B1', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image})
        sheet.insert_image('H1', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image, 'x_offset': 50})

        for obj in attendances:
            rgb_color = obj.employee_id.department_id.color
            color = '#FFFFFF'
            if len(rgb_color) > 1:
                color = rgb_to_hex(eval(rgb_color[rgb_color.index('('):rgb_color.rindex(',')] + ")"))
            color = color.upper()
            emp_id = workbook.add_format({'bg_color': '#F09481', 'align': 'center', 'border': 1})
            attendance = workbook.add_format({'bg_color': color, 'align': 'center', 'border': 1})
            time = workbook.add_format({'bg_color': 'silver', 'align': 'center', 'border': 1})
            sheet.write_row('B' + str(row + 6), [row], emp_id)
            sheet.write_row('C' + str(row + 6),
                            [obj.employee_id.name,
                             obj.employee_id.job_id.name or '-',
                             obj.employee_id.department_id.name], attendance)
            sheet.write_row('F' + str(row + 6),
                            [datetime.strptime(obj.check_in, "%Y-%m-%d %H:%M:%S").strftime('%H:%M'),
                             datetime.strptime(obj.check_out, "%Y-%m-%d %H:%M:%S").strftime('%H:%M'),
                             round(obj.worked_hours, 2)], time)
            row += 1
