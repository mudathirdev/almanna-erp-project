# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrDepartment(models.Model):
    """
    Inherit HR department model to add color field
    """
    _inherit = 'hr.department'

    color = fields.Char("Color")
    sequence = fields.Integer("Sequence")
