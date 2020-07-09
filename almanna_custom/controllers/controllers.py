# -*- coding: utf-8 -*-
from odoo import http

# class AlmannaCustom(http.Controller):
#     @http.route('/almanna_custom/almanna_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almanna_custom/almanna_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almanna_custom.listing', {
#             'root': '/almanna_custom/almanna_custom',
#             'objects': http.request.env['almanna_custom.almanna_custom'].search([]),
#         })

#     @http.route('/almanna_custom/almanna_custom/objects/<model("almanna_custom.almanna_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almanna_custom.object', {
#             'object': obj
#         })