# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PhongHop(models.Model):
    _name = "phong_hop"
    _description = "Phòng họp"

    ten_phong_hop = fields.Char(string="Tên phòng họp", required=True)
    vi_tri = fields.Char(string="Vị trí phòng họp", required=True)
    suc_chua = fields.Integer(string="Sức chứa trong phòng", required=True)
    mo_ta = fields.Text(string="Mô tả phòng họp", required=True)

    don_vi_id = fields.Many2one("don_vi", string="Đơn vị phòng họp", required=True)
    dat_phong_list = fields.One2many("dat_phong", "phong_hop_id")


