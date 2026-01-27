# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json


class PhongHopController(http.Controller):

    @http.route('/api/phong_hop/<dbname>/<int:id>', type='http', auth='public', methods=['GET'], csrf=False)
    def phong_hop_handler(self, dbname, id, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(
                status=200,
                headers=[
                    ('Access-Control-Allow-Origin', 'http://localhost:3000'),
                    ('Access-Control-Allow-Credentials', 'true'),
                    ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
                    ('Access-Control-Allow-Headers', 'Content-Type'),
                ]
            )
        try:
            # check db
            if request.db != dbname:
                request.session.db = dbname

            rec = request.env['phong_hop'].sudo().browse(id)

            if not rec.exists():
                return Response(
                    json.dumps({
                        "status": "error",
                        "message": "Phong hop not found"
                    }),
                    content_type='application/json',
                    status=404
                )

            data = {
                "status": "ok",
                "id": rec.id,
                "ten_phong_hop": rec.ten_phong_hop,
                "vi_tri": rec.vi_tri,
                "suc_chua": rec.suc_chua,
                "mo_ta": rec.mo_ta,
                "thoi_gian_toi_da": rec.thoi_gian_toi_da,
                "don_vi": {
                    "id": rec.don_vi_id.ma_don_vi if rec.don_vi_id else None,
                    "ten": rec.don_vi_id.ten_don_vi if rec.don_vi_id else None
                },
                "dat_phong_list": [
                    {
                        "ten_dat_phong": dp.ten_dat_phong,
                        "thoi_gian_bat_dau": dp.thoi_gian_bat_dau,
                        "thoi_gian_ket_thuc": dp.thoi_gian_ket_thuc,
                        "muc_dich": dp.muc_dich,
                        "trang_thai": dp.trang_thai,
                    }
                    for dp in rec.dat_phong_list
                ],
                "tai_san_list": [
                    {
                        "id": ts.ma_tai_san,
                        "ten_tai_san": ts.ten_tai_san,
                    }
                    for ts in rec.tai_san_list
                ]
            }

            return Response(
                json.dumps(data, default=str),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            return Response(
                json.dumps({
                    "status": "error",
                    "message": str(e)
                }),
                content_type='application/json',
                status=500
            )

    @http.route(['/api/list_phong_hop/<dbname>'], type='http', auth='public', methods=['GET'], csrf=False)
    def list_phong_hop_handler(self, dbname, **kwargs):
        try:
            if request.db != dbname:
                request.session.db = dbname

            phong_hops = request.env['phong_hop'].sudo().search([])

            data = []
            for phong_hop in phong_hops:
                data.append({
                    "ten_phong_hop": phong_hop.ten_phong_hop,
                    "vi_tri": phong_hop.vi_tri,
                    "suc_chua": phong_hop.suc_chua,
                    "thoi_gian_toi_da": phong_hop.thoi_gian_toi_da,
                })

            return Response(
                json.dumps({
                    "status": "ok",
                    "data": data
                }, default=str),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            return Response(
                json.dumps({
                    "status": "error",
                    "message": str(e)
                }),
                content_type='application/json',
                status=500
            )


    # @http.route(['/api/add_to_phong_hop/<dbname>'], type='http', auth='public', methods=['POST'], csrf=False)
    # def add_to_phong_hop_handler(self, dbname, **kwargs):
    #     try:
    #         if request.db != dbname:
    #             request.session.db = dbname
    #
    #         rec = request.env['phong_hop'].sudo().create({})
    #
    #
