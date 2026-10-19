---
title: Quy trình dựng City Timelapse (giả thuyết)
type: production
channel: city-timelapse
updated: 2026-10-17
sources: [raw/city-timelapse/competitors/2026-10-17_cornerstone-timelapse.md]
---

# Quy trình dựng (giả thuyết từ description đối thủ)

## Dữ liệu
- Footprint, chiều cao, năm xây từng tòa nhà: open data của thành phố/quận (NYC open data; LA: LARIAC + Assessor parcels; Las Vegas: Clark County assessor).
- Đường phố, bờ biển, landmark: OpenStreetMap.
- Công trình đã mất: dựng lại từ bản đồ lịch sử + sách sử.
- Năm xây nhà thường không có đủ → ước tính cho animation (đối thủ thừa nhận).
- Landmark chi tiết: mô hình Sketchfab CC-BY 4.0, ghi credit.

## Dựng (cần kiểm chứng)
- Có thể dùng Blender + addon nhập OSM/GIS, cho mỗi tòa nhà "mọc" theo năm xây bằng keyframe theo thuộc tính năm.
- Render 4K, camera bay theo chương.
- Thành phố ngoài Mỹ: kiểm tra từng nơi có dữ liệu năm xây hay không (cần kiểm chứng).

## Thư mục sản xuất
- `Youtube-AI/CityTimelapse-Videos/` (tạo 2026-10-17): mỗi tập `NNN_slug/`, mẫu description + checklist publish ở `_templates/`, landmark + `CREDITS.md` ở `assets/landmarks/`.

Liên quan: [[city-overview]] · [[city-format-blueprint]]

## Pipeline tập đầy đủ (từ 2026-10-17)
- Định dạng: không lời dẫn, chữ tiếng TBN, 8:00–8:58, 100% video AI Muse 10s/beat (~50 beat).
- Skill: `ct-viet-kich-ban` (tên thành phố → kich-ban.md) → `ct-viet-prompt` (→ NNN_beats.csv, 10 cột như _templates/mau_beat.csv) → anh tạo clip Muse vào footage/ → `ct-dung-video` (→ CTNNN_<slug>_1080p.mp4).
- Tool: `CityTimelapse-Videos/tools/ct_build.py` (dựng theo lượt ≤140s, in CONTINUE/DONE, --qc), `ct_csv.py`, `ct_endcard.py`. Test thành công trên `000_test-build` (81s, −14,5 LUFS).
- Clip Muse không có watermark → `delogo:` để trống (chỉ điền khi trộn clip Flow có chữ "Veo").
- ct_build.py hiển thị năm âm thành "N a. C." (kể cả khi chạy qua mốc 0 và trong đoạn tua ngược) — sửa 2026-10-18.
- Bài học 2026-10-18 (CDMX): avoid ≤100 ký tự nhưng phần chung của Roma đã 98 ký tự → avoid riêng từng beat bị bỏ âm thầm (Roma cũng dính). Giữ phần avoid chung ≤72 ký tự. Bỏ "soft natural daylight" ở beat đêm/chạng vạng/hoàng hôn/u ám/bình minh.
- Trước khi viết prompt Muse cho tập mới: đọc [[city-muse-prompt-rules]] (bảng từ cấm/thay thế + quy trình QC).
- Bài học dựng 2026-10-18 (CDMX): lệnh trên máy anh bị ngắt sau ~3 phút, kể cả chạy nền; ghi 1,1 GB vào thư mục kết nối chậm (~20 MB/s). ct_build.py đã sửa: bỏ qua ghép hình/trộn âm nếu đã có, bỏ faststart ở file tạm. Bước cuối nên mux trên ổ tạm của VM ($HOME/ctb) rồi chép về bằng dd theo khúc (skip/seek, nối tiếp được) + cmp. Nhạc phải đủ dài ≥ tổng thời lượng (amix duration=first), không thì video bị cắt cụt.
- Endcard (từ 2026-10-18): mặc định chồng lên beat cuối (`ct_endcard.py --overlay`, ct_build tự làm), nút tiếng Anh Like / Subscribe / Subscribed; câu hỏi + tagline vẫn tiếng TBN. Kiểu nền kem cũ: ghi `endcard: card` trong front matter kich-ban.md. Video không còn 8s endcard riêng → 001 CDMX dài 8:24.
- Thanh nhắc Like/Subscribe giữa video (từ 2026-10-18): 1 lần, ở beat "đỉnh cảm xúc" khoảng 20–25% thời lượng, beat KHÔNG có caption (thanh nằm đáy), tránh 60 giây đầu. Ghi trong front matter kich-ban.md: `subscribe: Bxxx+2`. Lần 2 (tuỳ chọn) ~55–60% ở beat không caption.
