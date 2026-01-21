from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    _order = 'ho_va_ten asc, tuoi desc'

    nhan_vien_id = fields.Char("Mã định danh", required=True)
    ho_va_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    nguoi_xac_nhan = fields.Char("Người xác nhận")
    lich_su_cong_tac = fields.One2many("lich_su_cong_tac",
                                       inverse_name="nhan_vien_id",
                                       string="Danh sách lịch sử công tác")
    quan_ly_bang_cap = fields.One2many("quan_ly_bang_cap",
                                       inverse_name="nhan_vien_id",
                                       string="Danh sách bàng cấp")
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", stoge=True)
    anh = fields.Binary("Ảnh")

    # relation, fields new
    don_vi_id = fields.Many2one("don_vi", string="Đơn vị")
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban")
    dang_hoat_dong = fields.Boolean(string="Trạng thái hoạt động của nhân viên", default=True)

    # dat_phong_ids = fields.One2many(
    #     'dat_phong',
    #     'nhan_vien_id',
    #     string="Lịch đặt phòng"
    # )
    # tai_san_ids = fields.One2many('tai_san','nhan_vien_id', string="Tài sản")

    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self):
        today = datetime.today()
        for record in self:
            if record.ngay_sinh:
                birth_date = fields.Date.from_string(record.ngay_sinh)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.tuoi = age
            else:
                record.tuoi = 0  # or None if you prefer

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được dưới 18")
