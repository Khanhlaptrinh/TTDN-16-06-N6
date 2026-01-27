# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools import convert_file
from odoo.tools.safe_eval import json


# class TaiSanDoanhNghiep(http.Controller):
    # @http.route(['/api/tai_san_doanh_nghiep/<dbname>/<int:id>'], type='http', auth="public", methods=['GET'], csrf=False)
    # def tai_san_handler(self):
    #     if request.httprequest.method == 'OPTIONS':
    #         return Response(
    #             status=200,
    #             headers=[
    #                 ('Access-Control-Allow-Origin', 'http://localhost:3000'),
    #                 ('Access-Control-Allow-Credentials', 'true'),
    #                 ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
    #                 ('Access-Control-Allow-Headers', 'Content-Type'),
    #             ]
    #         )
    #     else:
    #         try:
    #             if request.db != dbname:
    #                 request.session.db = dbname
    #
    #             rec = request.env['tai_san'].sudo().browse(id)
    #
    #             if not rec.exists():
    #                 return Response(
    #                     json.dumps({
    #                         "status": "error",
    #                         "message": "Tai San not fount"
    #                     }),
    #                     content_type = 'application/json',
    #                     status = 404
    #                 )
    #             data = {
    #                 "status": "ok",
    #                 "id": rec.
    #             }
