# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
from odoo.exceptions import ValidationError
import json


class PhongHopController(http.Controller):

    def _get_cors_headers(self):
        """Trả về headers CORS"""
        return [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Credentials', 'true'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ]

    def _json_response(self, data, status=200):
        """Helper để trả về JSON response"""
        return Response(
            json.dumps(data, default=str),
            content_type='application/json',
            status=status,
            headers=self._get_cors_headers()
        )

    def _set_db(self, dbname):
        """Set database nếu cần"""
        if request.db != dbname:
            request.session.db = dbname

    # ========== GET - Lấy danh sách phòng họp ==========
    @http.route('/api/list_phong_hop/<dbname>', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def list_phong_hop(self, dbname, **kwargs):
        """API lấy danh sách tất cả phòng họp"""
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            # Lấy tham số filter (nếu có)
            domain = []
            if kwargs.get('don_vi_id'):
                domain.append(('don_vi_id', '=', int(kwargs['don_vi_id'])))
            if kwargs.get('ten_phong_hop'):
                domain.append(('ten_phong_hop', 'ilike', kwargs['ten_phong_hop']))

            phong_hops = request.env['phong_hop'].sudo().search(domain)

            data = []
            for phong_hop in phong_hops:
                data.append({
                    "id": phong_hop.id,
                    "ten_phong_hop": phong_hop.ten_phong_hop,
                    "vi_tri": phong_hop.vi_tri,
                    "suc_chua": phong_hop.suc_chua,
                    "mo_ta": phong_hop.mo_ta,
                    "thoi_gian_toi_da": phong_hop.thoi_gian_toi_da,
                    # tiện cho AI service filter theo đơn vị mà không cần gọi detail
                    "don_vi_id": phong_hop.don_vi_id.id if phong_hop.don_vi_id else None,
                    "don_vi": {
                        "id": phong_hop.don_vi_id.id if phong_hop.don_vi_id else None,
                        "ten": phong_hop.don_vi_id.ten_don_vi if phong_hop.don_vi_id else None
                    },
                    # tiện cho AI service chấm điểm theo thiết bị trong phòng
                    "tai_san_ids": phong_hop.tai_san_list.ids,
                    "so_luong_dat_phong": len(phong_hop.dat_phong_list),
                    "so_luong_tai_san": len(phong_hop.tai_san_list)
                })

            return self._json_response({
                "status": "success",
                "message": "Lấy danh sách phòng họp thành công",
                "data": data,
                "total": len(data)
            })

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)

    # ========== GET - Lấy chi tiết một phòng họp ==========
    @http.route('/api/phong_hop/<dbname>/<int:id>', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def get_phong_hop(self, dbname, id, **kwargs):
        """API lấy chi tiết một phòng họp theo ID"""
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            phong_hop = request.env['phong_hop'].sudo().browse(id)

            if not phong_hop.exists():
                return self._json_response({
                    "status": "error",
                    "message": "Không tìm thấy phòng họp"
                }, status=404)

            data = {
                "id": phong_hop.id,
                "ten_phong_hop": phong_hop.ten_phong_hop,
                "vi_tri": phong_hop.vi_tri,
                "suc_chua": phong_hop.suc_chua,
                "mo_ta": phong_hop.mo_ta,
                "thoi_gian_toi_da": phong_hop.thoi_gian_toi_da,
                "don_vi": {
                    "id": phong_hop.don_vi_id.id if phong_hop.don_vi_id else None,
                    "ten": phong_hop.don_vi_id.ten_don_vi if phong_hop.don_vi_id else None,
                    "ma_don_vi": phong_hop.don_vi_id.ma_don_vi if phong_hop.don_vi_id else None
                },
                "dat_phong_list": [
                    {
                        "id": dp.id,
                        "ten_dat_phong": dp.ten_dat_phong,
                        "thoi_gian_bat_dau": str(dp.thoi_gian_bat_dau) if dp.thoi_gian_bat_dau else None,
                        "thoi_gian_ket_thuc": str(dp.thoi_gian_ket_thuc) if dp.thoi_gian_ket_thuc else None,
                        "muc_dich": dp.muc_dich,
                        "trang_thai": dp.trang_thai,
                        "nhan_vien": {
                            "id": dp.nhan_vien_id.id if dp.nhan_vien_id else None,
                            "ho_va_ten": dp.nhan_vien_id.ho_va_ten if dp.nhan_vien_id else None
                        }
                    }
                    for dp in phong_hop.dat_phong_list
                ],
                "tai_san_list": [
                    {
                        "id": ts.id,
                        "ma_tai_san": ts.ma_tai_san,
                        "ten_tai_san": ts.ten_tai_san,
                        "loai_tai_san": ts.loai_tai_san,
                        "tinh_trang": ts.tinh_trang
                    }
                    for ts in phong_hop.tai_san_list
                ]
            }

            return self._json_response({
                "status": "success",
                "message": "Lấy thông tin phòng họp thành công",
                "data": data
            })

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)

    # ========== POST - Tạo mới phòng họp ==========
    @http.route('/api/phong_hop/<dbname>', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def create_phong_hop(self, dbname, **kwargs):
        """API tạo mới phòng họp"""
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            # Lấy dữ liệu từ request body
            if hasattr(request, 'jsonrequest'):
                data = request.jsonrequest
            else:
                # Nếu không có jsonrequest, thử parse từ params
                import json as json_lib
                data = json_lib.loads(request.httprequest.data.decode('utf-8')) if request.httprequest.data else {}

            # Kiểm tra các trường bắt buộc
            required_fields = ['ten_phong_hop', 'vi_tri', 'suc_chua', 'mo_ta', 'don_vi_id']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]

            if missing_fields:
                return self._json_response({
                    "status": "error",
                    "message": f"Thiếu các trường bắt buộc: {', '.join(missing_fields)}"
                }, status=400)

            # Kiểm tra don_vi_id có tồn tại không
            don_vi = request.env['don_vi'].sudo().browse(data['don_vi_id'])
            if not don_vi.exists():
                return self._json_response({
                    "status": "error",
                    "message": "Đơn vị không tồn tại"
                }, status=400)

            # Tạo dữ liệu để insert
            vals = {
                'ten_phong_hop': data['ten_phong_hop'],
                'vi_tri': data['vi_tri'],
                'suc_chua': int(data['suc_chua']),
                'mo_ta': data['mo_ta'],
                'don_vi_id': data['don_vi_id'],
                'thoi_gian_toi_da': float(data.get('thoi_gian_toi_da', 4))
            }

            # Xử lý tài sản (Many2many)
            if 'tai_san_ids' in data and data['tai_san_ids']:
                # Kiểm tra các tài sản có tồn tại không
                tai_san_ids = [int(id) for id in data['tai_san_ids']]
                tai_sans = request.env['tai_san'].sudo().browse(tai_san_ids)
                if len(tai_sans) != len(tai_san_ids):
                    return self._json_response({
                        "status": "error",
                        "message": "Một số tài sản không tồn tại"
                    }, status=400)
                vals['tai_san_list'] = [(6, 0, tai_san_ids)]

            # Tạo phòng họp
            phong_hop = request.env['phong_hop'].sudo().create(vals)

            return self._json_response({
                "status": "success",
                "message": "Tạo phòng họp thành công",
                "data": {
                    "id": phong_hop.id,
                    "ten_phong_hop": phong_hop.ten_phong_hop,
                    "vi_tri": phong_hop.vi_tri,
                    "suc_chua": phong_hop.suc_chua
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

    # ========== PUT - Cập nhật phòng họp ==========
    @http.route('/api/phong_hop/<dbname>/<int:id>', type='http', auth='public', methods=['PUT', 'OPTIONS'], csrf=False)
    def update_phong_hop(self, dbname, id, **kwargs):
        """API cập nhật phòng họp"""
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            phong_hop = request.env['phong_hop'].sudo().browse(id)

            if not phong_hop.exists():
                return self._json_response({
                    "status": "error",
                    "message": "Không tìm thấy phòng họp"
                }, status=404)

            # Lấy dữ liệu từ request body
            if hasattr(request, 'jsonrequest'):
                data = request.jsonrequest
            else:
                import json as json_lib
                data = json_lib.loads(request.httprequest.data.decode('utf-8')) if request.httprequest.data else {}

            # Chuẩn bị dữ liệu để cập nhật
            vals = {}

            if 'ten_phong_hop' in data:
                vals['ten_phong_hop'] = data['ten_phong_hop']
            if 'vi_tri' in data:
                vals['vi_tri'] = data['vi_tri']
            if 'suc_chua' in data:
                vals['suc_chua'] = int(data['suc_chua'])
            if 'mo_ta' in data:
                vals['mo_ta'] = data['mo_ta']
            if 'thoi_gian_toi_da' in data:
                vals['thoi_gian_toi_da'] = float(data['thoi_gian_toi_da'])
            if 'don_vi_id' in data:
                # Kiểm tra don_vi_id có tồn tại không
                don_vi = request.env['don_vi'].sudo().browse(data['don_vi_id'])
                if not don_vi.exists():
                    return self._json_response({
                        "status": "error",
                        "message": "Đơn vị không tồn tại"
                    }, status=400)
                vals['don_vi_id'] = data['don_vi_id']

            # Xử lý cập nhật tài sản (Many2many)
            if 'tai_san_ids' in data:
                if data['tai_san_ids'] is None:
                    # Xóa tất cả tài sản
                    vals['tai_san_list'] = [(5, 0, 0)]
                else:
                    # Kiểm tra các tài sản có tồn tại không
                    tai_san_ids = [int(tid) for tid in data['tai_san_ids']]
                    tai_sans = request.env['tai_san'].sudo().browse(tai_san_ids)
                    if len(tai_sans) != len(tai_san_ids):
                        return self._json_response({
                            "status": "error",
                            "message": "Một số tài sản không tồn tại"
                        }, status=400)
                    vals['tai_san_list'] = [(6, 0, tai_san_ids)]

            if not vals:
                return self._json_response({
                    "status": "error",
                    "message": "Không có dữ liệu để cập nhật"
                }, status=400)

            # Cập nhật phòng họp
            phong_hop.write(vals)

            return self._json_response({
                "status": "success",
                "message": "Cập nhật phòng họp thành công",
                "data": {
                    "id": phong_hop.id,
                    "ten_phong_hop": phong_hop.ten_phong_hop,
                    "vi_tri": phong_hop.vi_tri,
                    "suc_chua": phong_hop.suc_chua
                }
            })

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

    # ========== DELETE - Xóa phòng họp ==========
    @http.route('/api/phong_hop/<dbname>/<int:id>', type='http', auth='public', methods=['DELETE', 'OPTIONS'], csrf=False)
    def delete_phong_hop(self, dbname, id, **kwargs):
        """API xóa phòng họp"""
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=self._get_cors_headers())

        try:
            self._set_db(dbname)

            phong_hop = request.env['phong_hop'].sudo().browse(id)

            if not phong_hop.exists():
                return self._json_response({
                    "status": "error",
                    "message": "Không tìm thấy phòng họp"
                }, status=404)

            # Kiểm tra xem phòng họp có đang được sử dụng không (có đặt phòng)
            if phong_hop.dat_phong_list:
                # Kiểm tra có đặt phòng nào đang active không
                active_dat_phong = phong_hop.dat_phong_list.filtered(
                    lambda dp: dp.trang_thai in ['draft', 'confirmed']
                )
                if active_dat_phong:
                    return self._json_response({
                        "status": "error",
                        "message": "Không thể xóa phòng họp vì đang có đặt phòng chưa hoàn thành"
                    }, status=400)

            # Lưu thông tin trước khi xóa
            ten_phong_hop = phong_hop.ten_phong_hop

            # Xóa phòng họp
            phong_hop.unlink()

            return self._json_response({
                "status": "success",
                "message": f"Xóa phòng họp '{ten_phong_hop}' thành công"
            })

        except Exception as e:
            return self._json_response({
                "status": "error",
                "message": str(e)
            }, status=500)
