# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
from odoo.exceptions import ValidationError
import json
from datetime import datetime


class DatPhongController(http.Controller):

    def _get_cors_headers(self):
        return [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Credentials', 'true'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ]

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data, default=str),
            content_type='application/json',
            status=status,
            headers=self._get_cors_headers()
        )

    def _set_db(self, dbname):
        if request.db != dbname:
            request.session.db = dbname

    @http.route('/api/dat_phong/<dbname>', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def list_dat_phong(self, dbname, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)
            domain = []

            if kwargs.get('phong_hop_id'):
                domain.append(('phong_hop_id', '=', int(kwargs['phong_hop_id'])))

            if kwargs.get('nhan_vien_id'):
                domain.append(('nhan_vien_id', '=', int(kwargs['nhan_vien_id'])))

            if kwargs.get('trang_thai'):
                domain.append(('trang_thai', '=', kwargs['trang_thai']))

            if kwargs.get('tu_ngay'):
                try:
                    tu_ngay = datetime.strptime(kwargs['tu_ngay'], '%Y-%m-%d')
                    domain.append(('thoi_gian_bat_dau', '>=', tu_ngay.strftime('%Y-%m-%d 00:00:00')))
                except ValueError:
                    pass

            if kwargs.get('den_ngay'):
                try:
                    den_ngay = datetime.strptime(kwargs['den_ngay'], '%Y-%m-%d')
                    domain.append(('thoi_gian_bat_dau', '<=', den_ngay.strftime('%Y-%m-%d 23:59:59')))
                except ValueError:
                    pass

            if kwargs.get('ten_dat_phong'):
                domain.append(('ten_dat_phong', 'ilike', kwargs['ten_dat_phong']))

            order = kwargs.get('order', 'thoi_gian_bat_dau desc')

            dat_phongs = request.env['dat_phong'].sudo().search(domain, order=order)

            data = []
            for dat_phong in dat_phongs:
                data.append({
                    "id": dat_phong.id,
                    "ten_dat_phong": dat_phong.ten_dat_phong,
                    "thoi_gian_bat_dau": str(dat_phong.thoi_gian_bat_dau) if dat_phong.thoi_gian_bat_dau else None,
                    "thoi_gian_ket_thuc": str(dat_phong.thoi_gian_ket_thuc) if dat_phong.thoi_gian_ket_thuc else None,
                    "muc_dich": dat_phong.muc_dich,
                    "trang_thai": dat_phong.trang_thai,
                    "trang_thai_label": dict(dat_phong._fields['trang_thai'].selection).get(dat_phong.trang_thai, ''),
                    "phong_hop": {
                        "id": dat_phong.phong_hop_id.id if dat_phong.phong_hop_id else None,
                        "ten_phong_hop": dat_phong.phong_hop_id.ten_phong_hop if dat_phong.phong_hop_id else None,
                        "vi_tri": dat_phong.phong_hop_id.vi_tri if dat_phong.phong_hop_id else None,
                        "suc_chua": dat_phong.phong_hop_id.suc_chua if dat_phong.phong_hop_id else None
                    },
                    "nhan_vien": {
                        "id": dat_phong.nhan_vien_id.id if dat_phong.nhan_vien_id else None,
                        "ho_va_ten": dat_phong.nhan_vien_id.ho_va_ten if dat_phong.nhan_vien_id else None,
                        "email": dat_phong.nhan_vien_id.email if dat_phong.nhan_vien_id else None,
                        "so_dien_thoai": dat_phong.nhan_vien_id.so_dien_thoai if dat_phong.nhan_vien_id else None,
                        "phong_ban": dat_phong.nhan_vien_id.phong_ban_id.ten_phong_ban if dat_phong.nhan_vien_id and dat_phong.nhan_vien_id.phong_ban_id else None
                    },
                    "thoi_gian_dat": self._calculate_duration(dat_phong.thoi_gian_bat_dau, dat_phong.thoi_gian_ket_thuc)
                })

            return self._json_response({
                "status": "success",
                "message": "Lấy danh sách đặt phòng thành công",
                "data": data,
                "total": len(data)
            })

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)

    def _calculate_duration(self, thoi_gian_bat_dau, thoi_gian_ket_thuc):
        """Tính thời gian đặt phòng (giờ)"""
        if thoi_gian_bat_dau and thoi_gian_ket_thuc:
            try:
                duration = (thoi_gian_ket_thuc - thoi_gian_bat_dau).total_seconds() / 3600
                return round(duration, 2)
            except:
                return None
        return None

    @http.route('/api/dat_phong/<dbname>', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def create_dat_phong(self, dbname, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            if hasattr(request, 'jsonrequest'):
                data = request.jsonrequest
            else:
                import json as json_lib
                data = json_lib.loads(request.httprequest.data.decode('utf-8')) if request.httprequest.data else {}

            required_fields = ['ten_dat_phong', 'phong_hop_id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]

            if missing_fields:
                return self._json_response({
                    "status": "error",
                    "message": f"Thiếu các trường bắt buộc: {', '.join(missing_fields)}"
                }, status=400)

            phong_hop = request.env['phong_hop'].sudo().browse(data['phong_hop_id'])
            if not phong_hop.exists():
                return self._json_response({
                    "status": "error",
                    "message": "Phòng họp không tồn tại"
                }, status=400)

            if data.get('nhan_vien_id'):
                nhan_vien = request.env['nhan_vien'].sudo().browse(data['nhan_vien_id'])
                if not nhan_vien.exists():
                    return self._json_response({
                        "status": "error",
                        "message": "Nhân viên không tồn tại"
                    }, status=400)

            dat_phong = request.env['dat_phong'].sudo().create({
                'ten_dat_phong': data['ten_dat_phong'],
                'phong_hop_id': data['phong_hop_id'],
                'nhan_vien_id': data.get('nhan_vien_id'),
                'thoi_gian_bat_dau': data['thoi_gian_bat_dau'],
                'thoi_gian_ket_thuc': data['thoi_gian_ket_thuc'],
                'muc_dich': data.get('muc_dich'),
                'trang_thai': data.get('trang_thai', 'draft')
            })

            return self._json_response({
                "status": "success",
                "message": "Tạo đặt phòng thành công",
                "data": {
                    "id": dat_phong.id,
                    "ten_dat_phong": dat_phong.ten_dat_phong,
                    "phong_hop": dat_phong.phong_hop_id.ten_phong_hop,
                    "trang_thai": dat_phong.trang_thai
                }
            }, status=201)

        except ValidationError as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=400)

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)
