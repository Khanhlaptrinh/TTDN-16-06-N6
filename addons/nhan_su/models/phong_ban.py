from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = "Phòng Ban"
    _rec_name = 'ten_phong_ban'

    ten_phong_ban = fields.Char(string="Tên phòng ban", required=True)
    don_vi_id = fields.Many2one("don_vi", string="Đơn vị", required=True)
    quan_ly_id = fields.Many2one("nhan_vien", string="Trưởng phòng", required=True)
