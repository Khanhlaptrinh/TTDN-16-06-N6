# -*- coding: utf-8 -*-
# from odoo import http


# class PhongHop(http.Controller):
#     @http.route('/phong_hop/phong_hop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phong_hop/phong_hop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('phong_hop.listing', {
#             'root': '/phong_hop/phong_hop',
#             'objects': http.request.env['phong_hop.phong_hop'].search([]),
#         })

#     @http.route('/phong_hop/phong_hop/objects/<model("phong_hop.phong_hop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phong_hop.object', {
#             'object': obj
#         })
