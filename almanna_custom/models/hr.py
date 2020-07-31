# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hrEmployee(models.Model):
    _inherit = 'hr.employee'


    start_date = fields.Date('Start Date')
    colorpicker = fields.Char()

    emp_application_form_attach = fields.Binary(string="Application Form")
    cv_attach = fields.Binary(string="CV")
    app_medical_check_attach = fields.Binary(string="Appointment Medical Check-UP")

    edu_certif_attach_ids = fields.Many2many('ir.attachment',string="Educational Certificates",relation="edu_attachment")
    prev_exp_attach_ids = fields.Many2many('ir.attachment',string="Previous Experience",relation="prev_exp_attachment")
    
    military_id_attach = fields.Binary(string="Military ID Card")
    passport_id_attach = fields.Binary(string="ID")
    eight_colored_photo_emp_attach = fields.Binary(string="Colored Photos")
    social_insurance_attach = fields.Binary(string="Social Insurance Form & Number")
    driving_licences_attach = fields.Many2many('ir.attachment',string="Driving Licences",relation="dri_attachment")
    res_cert_attach = fields.Binary(string="Residential Certificate")
    
    marriage_cert_attach_ids =  fields.Many2many('ir.attachment',string="Marriage Certificates",relation="marriage_attachment")
    birth_certi_attach_ids = fields.Many2many('ir.attachment',string="Birth Cerificates",relation="birth_attachment")
    spouse_children_attach_ids = fields.Many2many('ir.attachment',string="Spouses and Children Photos",relation="spo_child_attachment")
    prev_exp_attach_ids = fields.Many2many('ir.attachment',string="Previous Experience Training/Certificates",relation="prev_exp_attachment")
    other_attach_ids = fields.Many2many('ir.attachment',string="Others Attachments",relation="other_attachment")