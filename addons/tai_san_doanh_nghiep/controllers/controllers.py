# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json


class TaiSanController(http.Controller):

    def _get_cors_headers(self):
        return [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Credentials', 'true'),
            ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ]

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data, default=str),
            content_type='application/json',
            status=status,
            headers=self._get_cors_headers(),
        )

    def _set_db(self, dbname):
        if request.db != dbname:
            request.session.db = dbname

    @http.route('/api/tai_san/<dbname>', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def list_tai_san(self, dbname, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)
            assets = request.env['tai_san'].sudo().search([])

            data = []
            for a in assets:
                data.append({
                    "id": a.id,
                    "ma_tai_san": a.ma_tai_san,
                    "ten_tai_san": a.ten_tai_san,
                    "vi_tri": a.vi_tri,
                })

            return self._json_response({
                "status": "success",
                "message": "Lấy danh sách tài sản thành công",
                "data": data,
                "total": len(data),
            })
        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e),
            }, status=500)