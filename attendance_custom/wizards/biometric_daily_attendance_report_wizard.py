# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BiometricDailyAttendanceReportWizard(models.TransientModel):
    _name = 'attendance_custom.biometric_daily_report_wizard'

    date = fields.Date("Date", required=1)

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date': self.date,
            },
        }
        return self.env.ref('attendance_custom.biometric_daily_attendance_report').report_action(self, data=data)
