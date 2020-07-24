# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PeriodicAttendanceReportWizard(models.TransientModel):
    _name = 'attendance_custom.periodic_report_wizard'

    date_from = fields.Date("From", required=1)
    date_to = fields.Date("To", required=1)

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to
            },
        }
        return self.env.ref('attendance_custom.periodic_attendance_report').report_action(self, data=data)
