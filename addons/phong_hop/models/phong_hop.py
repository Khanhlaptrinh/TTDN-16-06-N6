# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PhongHop(models.Model):
    _name = "phong_hop"
    _description = "Phòng họp"

    ten_phong_hop = fields.Char(string="Tên phòng họp", required=True)
    vi_tri = fields.Char(string="Vị trí phòng họp", required=True)
    suc_chua = fields.Integer(string="Sức chứa trong phòng", required=True)
    mo_ta = fields.Text(string="Mô tả phòng họp", required=True)
    thoi_gian_toi_da = fields.Float(
        string="Thời gian đặt tối đa (giờ)",
        default=4
    )

    don_vi_id = fields.Many2one("don_vi", string="Đơn vị phòng họp", required=True)
    dat_phong_list = fields.One2many("dat_phong", "phong_hop_id")

    tai_san_list = fields.Many2many("tai_san", "tai_san_trong_phong_rel", "phong_hop_id", "tai_san_id",
                                    string="Thiết bị trong phòng")

    @api.onchange('ten_phong_hop')
    def _onchange_ten_phong_hop(self):
        if self.ten_phong_hop:
            self.mo_ta = f"Phòng : {self.ten_phong_hop}"
