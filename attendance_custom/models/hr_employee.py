# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    attendance_ids = fields.One2many('hr.attendance', 'employee_id')
    machine_attendance_ids = fields.One2many('zk.machine.attendance', 'employee_id')
