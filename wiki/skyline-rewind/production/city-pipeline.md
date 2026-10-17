---
title: Quy trình dựng Skyline Rewind (giả thuyết)
type: production
channel: skyline-rewind
updated: 2026-10-17
sources: [raw/skyline-rewind/competitors/2026-10-17_cornerstone-timelapse.md]
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
- `Youtube-AI/SkylineRewind-Videos/` (tạo 2026-10-17): mỗi tập `NNN_slug/`, mẫu description + checklist publish ở `_templates/`, landmark + `CREDITS.md` ở `assets/landmarks/`.

Liên quan: [[city-overview]] · [[city-format-blueprint]]
