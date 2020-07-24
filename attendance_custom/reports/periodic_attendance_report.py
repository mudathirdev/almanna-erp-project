# -*- coding: utf-8 -*-
from odoo import models
from webcolors import rgb_to_hex
from datetime import datetime, timedelta
import base64
import io


class PeriodicAttendanceXLSX(models.AbstractModel):
    _name = 'report.attendance_custom.periodic_attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    # Function to convert odoo datetime string to a python date object
    def Ymd(self, datetime_string):
        str_date = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        str_date = datetime.strptime(str_date, "%Y-%m-%d")
        return str_date

    def generate_xlsx_report(self, workbook, data, attendances):
        row = 1

        # Setup sheet and data
        report_name = "PERIODIC ATTENDANCE REPORT"
        employees = self.env['hr.employee'].search([])
        # Parse date from and date to type date
        date_from = datetime.strptime(data['form']['date_from'], "%Y-%m-%d")
        date_to = datetime.strptime(data['form']['date_to'], "%Y-%m-%d")

        for employee in employees:
            employee.attendance_ids = \
                employee.attendance_ids.filtered(lambda a:
                                                 date_to >= self.Ymd(a.check_in) >= date_from)
            employee.attendance_ids = employee.attendance_ids.sorted(lambda r: r.employee_id.department_id.id)

        # Setup columns
        sheet = workbook.add_worksheet(report_name[:31])
        titles = workbook.add_format({'align': 'center', 'bold': True})
        center = workbook.add_format({'align': 'center'})
        t_heading = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#BD5B5B', 'border': 1})
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 25)

        # Headings and titles
        sheet.write('E1', 'HR DEPARTMENT', titles)
        sheet.write('E2', 'ATTENDANCE REPORT', titles)
        sheet.write('E4', "AVERAGE WORKING HOURS", titles)
        sheet.write('E4', 'FROM : ' + date_from.strftime("%d-%b") + ' TO : ' + date_to.strftime("%d-%b"), center)
        sheet.write_row('B7', ['Employee ID', 'Name', 'Job Title', 'Department'], t_heading)

        # Add company logo
        logo = self.env.user.sudo().company_id.logo
        imgdata = base64.b64decode(logo)
        image = io.BytesIO(imgdata)
        sheet.insert_image('B1', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image})
        sheet.insert_image('H1', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image})
        for obj in employees:
            if len(obj.attendance_ids) > 0:
                rgb_color = obj.department_id.color
                color = rgb_to_hex(eval(rgb_color[rgb_color.index('('):rgb_color.rindex(',') - 1] + ")")) \
                    if rgb_color else ''
                emp_id = workbook.add_format({'bg_color': '#F09481', 'align': 'center', 'border': 1})
                attendance = workbook.add_format({'bg_color': color, 'align': 'center', 'border': 1})
                time = workbook.add_format({'bg_color': 'silver', 'align': 'center', 'border': 1})
                sheet.write_row('B' + str(row + 7), [row], emp_id)
                sheet.write_row('C' + str(row + 7),
                                [obj.name,
                                 obj.job_id.name,
                                 obj.department_id.name], attendance)
                day_column = 5
                for attendance in obj.attendance_ids:
                    sheet.write_row(6, day_column, ['Enter', 'Exit', 'Working Hours'], t_heading)
                    sheet.write_row(row + 6, day_column,
                                    [datetime.strptime(attendance.check_in, "%Y-%m-%d %H:%M:%S").strftime('%H:%M'),
                                     datetime.strptime(attendance.check_out, "%Y-%m-%d %H:%M:%S").strftime('%H:%M'),
                                     round(attendance.worked_hours, 2)], time)
                    day_column += 3
                row += 1
