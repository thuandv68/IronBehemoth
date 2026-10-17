# Sổ đo lồng tiếng

> File dữ liệu của skill `long-tieng`. `lt_03` tự ghi mục "Sổ tốc độ đọc"; agent chính ghi mục "Số đo theo tập" sau
> mỗi tập. ⛔ Không sửa tay số đã ghi. Giữ nguyên các tiêu đề `## ` — script tìm theo đúng chữ.

## Số đo theo tập
Agent chính ghi một dòng mỗi ngôn ngữ sau mỗi tập (SKILL.md §5).

| Ngày | Tập | Ngôn ngữ | Khối đạt | Tỉ lệ lời/khung | Viết lại | Credit |
|---|---|---|---|---|---|---|
| 2026-10-16 | 001_king-tiger | tieng_tay_ban_nha | 51/51 | 0,85–1,12 | 6 (K025 K027 K032 K043 K047 K048; K027 viết lại 2 lần) | 17.843 |
| 2026-10-16 | 001_king-tiger | tieng_indonesia | 51/51 | 0,86–1,10 | 4 (K025 K035 K047 K051) | 16.701 |
| 2026-10-16 | 001_king-tiger | tieng_viet | 51/51 | 0,68–1,05 | 1 (K028) | 14.754 |

## Sổ tốc độ đọc theo ngôn ngữ
Skill `long-tieng` TỰ GHI sau lần đọc đầu của mỗi ngôn ngữ, mỗi tập một dòng; `lt_02` lấy trung vị ký tự/giây để dự báo độ dài từng khối trước khi đọc.

| Ngày | Tập | Ngôn ngữ | Ký tự/giây lời | Lời/khung lần đầu (trung vị) | Số khối đo | Ghi chú |
|---|---|---|---|---|---|---|
| 2026-10-16 | 001_king-tiger | tieng_tay_ban_nha | 15,27 | 1,00 | 51 |  |
| 2026-10-16 | 001_king-tiger | tieng_indonesia | 15,76 | 0,96 | 51 |  |
| 2026-10-16 | 001_king-tiger | tieng_viet | 17,59 | 0,80 | 51 |  |

## Ghi chú vận hành
Giới hạn đồng thời của ai33, lỗi gặp khi chạy, v.v.
- 2026-10-16: ai33 giới hạn 10 task trong hàng đợi cho cả tài khoản (HTTP 429 queue_limit_exceeded). Chạy 3 ngôn ngữ song song bị lỗi → phải chạy lt_03 lần lượt từng ngôn ngữ. Máy chỉ có `python3`.
