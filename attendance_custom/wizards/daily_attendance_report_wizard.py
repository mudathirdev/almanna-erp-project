# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DailyAttendanceReportWizard(models.TransientModel):
    _name = 'attendance_custom.daily_report_wizard'

    date = fields.Date("Date", required=1)

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date': self.date,
            },
        }
        return self.env.ref('attendance_custom.daily_attendance_report').report_action(self, data=data)
