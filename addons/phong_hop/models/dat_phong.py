from odoo import api, fields, models

class DatPhong(models.Model):
    _name = 'dat_phong'
    _description = 'Đặt phòng'

    ten_dat_phong = fields.Char(string="Tên đặt phòng", required=True)
    thoi_gian_bat_dau = fields.Datetime(string="Thời gian bắt đầu đặt phòng", required=True)
    thoi_gian_ket_thuc = fields.Datetime(string="Thời gian kết thúc đặt phòng", required=True)
    muc_dich = fields.Char(string="Mục đích đặt phòng")
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành')
    ], default='draft')

    phong_hop_id = fields.Many2one("phong_hop", string="Phòng họp", required=True)
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên đặt phòng", required=True)
