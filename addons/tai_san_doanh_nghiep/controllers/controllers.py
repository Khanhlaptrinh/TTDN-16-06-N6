# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request, Response
from odoo.exceptions import ValidationError
import json
from datetime import datetime


class TaiSanDoanhNghiepController(http.Controller):

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

    # ========== GET - Lấy danh sách tất cả tài sản ==========
    @http.route('/api/tai_san/<dbname>', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def list_tai_san(self, dbname, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)
            domain = []

            if kwargs.get('loai_tai_san'):
                domain.append(('loai_tai_san', '=', kwargs['loai_tai_san']))

            if kwargs.get('tinh_trang'):
                domain.append(('tinh_trang', '=', kwargs['tinh_trang']))

            if kwargs.get('nhan_vien_id'):
                domain.append(('nhan_vien_id', '=', int(kwargs['nhan_vien_id'])))

            if kwargs.get('ma_tai_san'):
                domain.append(('ma_tai_san', 'ilike', kwargs['ma_tai_san']))

            if kwargs.get('ten_tai_san'):
                domain.append(('ten_tai_san', 'ilike', kwargs['ten_tai_san']))

            if kwargs.get('vi_tri'):
                domain.append(('vi_tri', 'ilike', kwargs['vi_tri']))

            if kwargs.get('tu_ngay_mua'):
                try:
                    tu_ngay = datetime.strptime(kwargs['tu_ngay_mua'], '%Y-%m-%d')
                    domain.append(('ngay_mua', '>=', tu_ngay.strftime('%Y-%m-%d')))
                except ValueError:
                    pass

            if kwargs.get('den_ngay_mua'):
                try:
                    den_ngay = datetime.strptime(kwargs['den_ngay_mua'], '%Y-%m-%d')
                    domain.append(('ngay_mua', '<=', den_ngay.strftime('%Y-%m-%d')))
                except ValueError:
                    pass

            if kwargs.get('tu_gia_tri'):
                try:
                    domain.append(('gia_tri', '>=', float(kwargs['tu_gia_tri'])))
                except ValueError:
                    pass

            if kwargs.get('den_gia_tri'):
                try:
                    domain.append(('gia_tri', '<=', float(kwargs['den_gia_tri'])))
                except ValueError:
                    pass

            order = kwargs.get('order', 'id desc')

            tai_sans = request.env['tai_san'].sudo().search(domain, order=order)

            data = []
            for tai_san in tai_sans:
                data.append({
                    "id": tai_san.id,
                    "ma_tai_san": tai_san.ma_tai_san,
                    "ten_tai_san": tai_san.ten_tai_san,
                    "loai_tai_san": tai_san.loai_tai_san,
                    "loai_tai_san_label": dict(tai_san._fields['loai_tai_san'].selection).get(tai_san.loai_tai_san, ''),
                    "gia_tri": tai_san.gia_tri,
                    "ngay_mua": str(tai_san.ngay_mua) if tai_san.ngay_mua else None,
                    "tinh_trang": tai_san.tinh_trang,
                    "tinh_trang_label": dict(tai_san._fields['tinh_trang'].selection).get(tai_san.tinh_trang, '') if tai_san.tinh_trang else None,
                    "vi_tri": tai_san.vi_tri,
                    "nhan_vien_quan_ly": {
                        "id": tai_san.nhan_vien_id.id if tai_san.nhan_vien_id else None,
                        "ho_va_ten": tai_san.nhan_vien_id.ho_va_ten if tai_san.nhan_vien_id else None,
                        "email": tai_san.nhan_vien_id.email if tai_san.nhan_vien_id else None,
                        "phong_ban": tai_san.nhan_vien_id.phong_ban_id.ten_phong_ban if tai_san.nhan_vien_id and tai_san.nhan_vien_id.phong_ban_id else None
                    },
                    "so_luong_cap_phat": len(tai_san.lich_su_cap_phat),
                    "so_luong_muon_tra": len(tai_san.muon_tra),
                    "so_luong_bao_tri": len(tai_san.bao_tri_sua_chua)
                })

            return self._json_response({
                "status": "success",
                "message": "Lấy danh sách tài sản thành công",
                "data": data,
                "total": len(data)
            })

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)

    @http.route('/api/lich_su_cap_phat/<dbname>', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def list_lich_su_cap_phat(self, dbname, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            domain = []

            if kwargs.get('tai_san_id'):
                domain.append(('tai_san_id', '=', int(kwargs['tai_san_id'])))

            if kwargs.get('nhan_vien_id'):
                domain.append(('nhan_vien_id', '=', int(kwargs['nhan_vien_id'])))

            if kwargs.get('tu_ngay_cap'):
                try:
                    tu_ngay = datetime.strptime(kwargs['tu_ngay_cap'], '%Y-%m-%d')
                    domain.append(('ngay_cap', '>=', tu_ngay.strftime('%Y-%m-%d')))
                except ValueError:
                    pass

            if kwargs.get('den_ngay_cap'):
                try:
                    den_ngay = datetime.strptime(kwargs['den_ngay_cap'], '%Y-%m-%d')
                    domain.append(('ngay_cap', '<=', den_ngay.strftime('%Y-%m-%d')))
                except ValueError:
                    pass

            if kwargs.get('chua_thu_hoi') == 'true':
                domain.append(('ngay_thu_hoi', '=', False))

            if kwargs.get('da_thu_hoi') == 'true':
                domain.append(('ngay_thu_hoi', '!=', False))

            order = kwargs.get('order', 'ngay_cap desc')

            lich_su_cap_phats = request.env['lich_su_cap_phat'].sudo().search(domain, order=order)

            data = []
            for lich_su in lich_su_cap_phats:
                so_ngay_da_cap = None
                if lich_su.ngay_cap:
                    if lich_su.ngay_thu_hoi:
                        try:
                            ngay_cap = fields.Date.from_string(lich_su.ngay_cap)
                            ngay_thu_hoi = fields.Date.from_string(lich_su.ngay_thu_hoi)
                            so_ngay_da_cap = (ngay_thu_hoi - ngay_cap).days
                        except:
                            pass
                    else:
                        try:
                            ngay_cap = fields.Date.from_string(lich_su.ngay_cap)
                            today = fields.Date.today()
                            so_ngay_da_cap = (today - ngay_cap).days
                        except:
                            pass

                data.append({
                    "id": lich_su.id,
                    "ngay_cap": str(lich_su.ngay_cap) if lich_su.ngay_cap else None,
                    "ngay_thu_hoi": str(lich_su.ngay_thu_hoi) if lich_su.ngay_thu_hoi else None,
                    "trang_thai": "da_thu_hoi" if lich_su.ngay_thu_hoi else "dang_su_dung",
                    "trang_thai_label": "Đã thu hồi" if lich_su.ngay_thu_hoi else "Đang sử dụng",
                    "so_ngay_da_cap": so_ngay_da_cap,
                    "tai_san": {
                        "id": lich_su.tai_san_id.id if lich_su.tai_san_id else None,
                        "ma_tai_san": lich_su.tai_san_id.ma_tai_san if lich_su.tai_san_id else None,
                        "ten_tai_san": lich_su.tai_san_id.ten_tai_san if lich_su.tai_san_id else None,
                        "loai_tai_san": lich_su.tai_san_id.loai_tai_san if lich_su.tai_san_id else None,
                        "gia_tri": lich_su.tai_san_id.gia_tri if lich_su.tai_san_id else None,
                        "tinh_trang": lich_su.tai_san_id.tinh_trang if lich_su.tai_san_id else None
                    },
                    "nhan_vien": {
                        "id": lich_su.nhan_vien_id.id if lich_su.nhan_vien_id else None,
                        "ho_va_ten": lich_su.nhan_vien_id.ho_va_ten if lich_su.nhan_vien_id else None,
                        "email": lich_su.nhan_vien_id.email if lich_su.nhan_vien_id else None,
                        "so_dien_thoai": lich_su.nhan_vien_id.so_dien_thoai if lich_su.nhan_vien_id else None,
                        "phong_ban": lich_su.nhan_vien_id.phong_ban_id.ten_phong_ban if lich_su.nhan_vien_id and lich_su.nhan_vien_id.phong_ban_id else None,
                        "chuc_vu": lich_su.nhan_vien_id.chuc_vu_id.ten_chuc_vu if lich_su.nhan_vien_id and lich_su.nhan_vien_id.chuc_vu_id else None
                    }
                })

            return self._json_response({
                "status": "success",
                "message": "Lấy danh sách lịch sử cấp phát thành công",
                "data": data,
                "total": len(data)
            })

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)
