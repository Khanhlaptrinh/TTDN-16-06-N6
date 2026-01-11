from odoo import api, fields, models
from odoo.exceptions import ValidationError

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
    nhan_vien_id = fields.Many2one("nhan_vien",string="Nhân viên đặt phòng")
    @api.onchange('nhan_vien_id')
    def _onchange_nhan_vien_id(self):
        if self.nhan_vien_id and self.nhan_vien_id.don_vi_id:
            return {
                'domain': {
                    'phong_hop_id': [
                        ('don_vi_id', '=', self.nhan_vien_id.don_vi_id.id)
                    ]
                }
            }
        else:
            return {
                'domain': {
                    'phong_hop_id': []
                }
            }

    @api.constrains('phong_hop_id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_trung_lich(self):
        for rec in self:
            if rec.thoi_gian_bat_dau >= rec.thoi_gian_ket_thuc:
                raise ValidationError("Thời gian kết thúc phải lớn hơn thời gian bắt đầu")

            domain = [
                ('phong_hop_id', '=', rec.phong_hop_id.id),
                ('id', '!=', rec.id),
                ('thoi_gian_bat_dau', '<', rec.thoi_gian_ket_thuc),
                ('thoi_gian_ket_thuc', '>', rec.thoi_gian_bat_dau),
            ]
            if self.search_count(domain):
                raise ValidationError("Phòng họp đã được đặt trong khoảng thời gian này")

    @api.constrains('thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'phong_hop_id')
    def _check_thoi_gian_dat_phong(self):
        for rec in self:
            if rec.thoi_gian_bat_dau and rec.thoi_gian_ket_thuc and rec.phong_hop_id:
                duration = (rec.thoi_gian_ket_thuc - rec.thoi_gian_bat_dau).total_seconds() / 3600
                if duration > rec.phong_hop_id.thoi_gian_toi_da:
                    raise ValidationError(
                        f"Phòng {rec.phong_hop_id.ten_phong_hop} chỉ được đặt tối đa "
                        f"{rec.phong_hop_id.thoi_gian_toi_da} giờ."
                    )