# -*- coding: utf-8 -*-
import base64
import io
from datetime import datetime, timedelta

from webcolors import rgb_to_hex

from odoo import models


class PeriodicAttendanceXLSX(models.AbstractModel):
    _name = 'report.attendance_custom.periodic_attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    # Function to convert odoo datetime string to a python date object
    def Ymd(self, datetime_string):
        str_date = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        str_date = datetime.strptime(str_date, "%Y-%m-%d")
        return str_date

    def generate_xlsx_report(self, workbook, data, attendances):

        # Setup sheet and data
        report_name = "ATTENDANCE FROM " + str(data['form']['date_from']) + " TO " + data['form']['date_to']
        all_employees = self.env['hr.employee'].search([])
        # Parse date from and date to type date
        date_from = datetime.strptime(data['form']['date_from'], "%Y-%m-%d")
        date_to = datetime.strptime(data['form']['date_to'], "%Y-%m-%d")

        # Get all dates between the date from and date to dates
        dates = []
        delta = date_to - date_from  # as timedelta

        for i in range(delta.days + 1):
            day = date_from + timedelta(days=i)
            dates.append(day)

        employees = all_employees[:]
        employees = employees.sorted(lambda e: e.department_id.id)

        # Setup columns
        sheet = workbook.add_worksheet(report_name[:31])
        titles = workbook.add_format({'align': 'center', 'bold': True})
        center = workbook.add_format({'align': 'center'})
        t_heading = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#BD5B5B', 'border': 1,
                                         'valign': 'vcenter'})
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 25)

        # Add company logo
        logo = self.env.user.sudo().company_id.logo
        imgdata = base64.b64decode(logo)
        image = io.BytesIO(imgdata)
        sheet.insert_image(0, 1, 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image})

        # Print dates between date from and date to
        dates_column = 5
        dates_format = workbook.add_format({'align': 'center'})
        for a_date in dates:
            sheet.merge_range(6, dates_column, 6, dates_column + 1, a_date.strftime("%d-%b"), dates_format)
            sheet.set_column(dates_column + 2, dates_column + 2, 15)
            sheet.write_row(7, dates_column, ['Enter', 'Exit', 'Working Hours'], t_heading)
            dates_column += 3

        # Headings and titles
        sheet.merge_range(0, 2, 0, dates_column, 'HR DEPARTMENT', titles)
        sheet.merge_range(1, 2, 1, dates_column, 'ATTENDANCE REPORT', titles)
        sheet.merge_range(3, 2, 3, dates_column, "AVERAGE WORKING HOURS", titles)
        sheet.merge_range(5, 2, 5, dates_column, 'FROM : ' + date_from.strftime("%d-%b") + ' TO : ' + date_to.strftime("%d-%b"), center)
        sheet.write_row('B8', ['Employee \nID', 'Name', 'Job Title', 'Department'], t_heading)

        # Continue titles and company logo after days printed
        sheet.insert_image(0, dates_column, 'python.png', {'x_scale': 0.5, 'y_scale': 0.5, 'image_data': image})
        sheet.set_column(dates_column, dates_column, 11)
        sheet.write(7, dates_column, 'Average \nWorking \nHours', t_heading)
        sheet.set_row(7, 60)
        row = 1
        for obj in employees:
            employee_avg = 0
            num_days = 0
            total_hours = 0
            if len(obj.attendance_ids) > 0:
                rgb_color = obj.department_id.color
                color = '#FFFFFF'
                if len(rgb_color) > 1:
                    color = rgb_to_hex(eval(rgb_color[rgb_color.index('('):rgb_color.rindex(',')] + ")"))
                color = color.upper()
                emp_id = workbook.add_format({'bg_color': '#F09481', 'align': 'center', 'border': 1})
                attendance = workbook.add_format({'bg_color': color, 'align': 'center', 'border': 1})
                time = workbook.add_format({'bg_color': 'silver', 'align': 'center', 'border': 1})
                sheet.write_row('B' + str(row + 8), [row], emp_id)
                sheet.write_row('C' + str(row + 8),
                                [obj.name,
                                 obj.job_id.name or '-',
                                 obj.department_id.name], attendance)
                employee_attendance_ids = obj.attendance_ids.filtered(lambda a:
                                                                      date_to >= self.Ymd(a.check_in) >= date_from)
                day_column = 5
                for a_date in dates:
                    a_date_attendances = employee_attendance_ids.filtered(lambda attend:
                                                                          datetime.strptime(attend.check_in,
                                                                                            "%Y-%m-%d %H:%M:%S")
                                                                          .strftime('%Y-%m-%d') ==
                                                                          a_date.strftime("%Y-%m-%d") and
                                                                          datetime.strptime(attend.check_out,
                                                                                            "%Y-%m-%d %H:%M:%S")
                                                                          .strftime('%Y-%m-%d') ==
                                                                          a_date.strftime("%Y-%m-%d"))
                    if a_date_attendances:
                        first_check_in = a_date_attendances.sorted(lambda a: a.check_in)[0].check_in
                        first_check_in = datetime.strptime(first_check_in, "%Y-%m-%d %H:%M:%S").strftime('%H:%M')
                        last_check_out = a_date_attendances.sorted(lambda a: a.check_out)[-1].check_out
                        last_check_out = datetime.strptime(last_check_out, "%Y-%m-%d %H:%M:%S").strftime('%H:%M')
                        worked_hours = sum(a_date_attendances.mapped('worked_hours'))
                        num_days += 1
                        total_hours += worked_hours
                        sheet.write_row(row + 7, day_column,
                                        [first_check_in,
                                         last_check_out,
                                         round(worked_hours, 2)], time)
                    else:
                        sheet.write_row(row + 7, day_column, ['-', '-', '-'], time)
                    day_column += 3
                employee_avg = 0 if num_days == 0 or total_hours == 0 else total_hours / num_days
                employee_avg = round(employee_avg, 2)
                sheet.write(row + 7, dates_column, employee_avg, workbook.add_format({'align': 'center', 'border': 1}))
                row += 1
