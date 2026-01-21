from odoo import models, fields, api

class LichSuCapPhat(models.Model):
    _name = 'lich_su_cap_phat'
    _description = 'Lịch sử cấp phát'

    ngay_cap = fields.Date(string='Ngày cấp', default=fields.Date.today, required=True)
    ngay_thu_hoi = fields.Date(string='Ngày thu hồi')

    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên được cấp', required=True)