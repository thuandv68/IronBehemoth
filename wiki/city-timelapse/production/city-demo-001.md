---
title: Demo 001 Ciudad de México (~58s) — cách làm và bài học
type: production
channel: city-timelapse
updated: 2026-10-17
sources: [raw/city-timelapse/competitors/2026-10-17_cornerstone-timelapse.md]
---

# Demo 001 — Ciudad de México (1325 → hoy), 58 giây

Sản phẩm: `Youtube-AI/CityTimelapse-Videos/001_ciudad-de-mexico/demo/CT001_CDMX_demo_1080p.mp4` (1920×1080 30fps, −14,6 LUFS, TP −1,8 dBTP). Phân tích mẫu + shot plan cùng thư mục.

## Cấu trúc học từ video mẫu (Cornerstone, Las Vegas)
Hook hôm nay (đêm) 4s → tua ngược cực nhanh, bộ đếm năm lùi → title card trên cảnh trống → các chương: năm lớn giữa-trên + tên chương + caption đáy → kết hôm nay về đêm → (mẫu không có endcard). Camera bay liên tục, không cắt cứng, không lời dẫn, nhạc nền liên tục (~−21,7 LUFS).

## Pipeline demo
- 5 clip Veo 3.1 Lite (Flow, 8s, x1, 720p): C1 CDMX 2026 đêm · C2 Tenochtitlan mọc trên hồ · C3 Nueva España · C4 1900–1956 · C5 megalópolis. Khóa phong cách: "miniature architectural 3D model, clean clay-like buildings… high oblique aerial ~400 m, slow drift, buildings rise out of the ground (timelapse)".
- Tool: `CityTimelapse-Videos/tools/ct_build_demo.py` (hình) + `ct_mix_demo.py` (âm). Cache segment (CACHE=1), mỗi lần chạy < 170s.
- Xoá chữ "Veo" của Flow: `delogo=x=1234:y=686:w=40:h=26` trên khung 1280×720.
- Dải tối mờ mép trên (top_grad.png) + viền chữ để năm/chương đọc được trên nền sáng.
- Nhạc: YouTube Audio Library "Ancient Civilisations" (Alex Jones / Xander Jones), vào từ giây 9 của bài để đoạn bùng lên trùng title card. SFX Mixkit 9 file (credits trong audio/sfx/CREDITS.md).
- Loudnorm 2-pass −14 LUFS + alimiter 0,72 → TP −1,8.

## Endcard (kiểu IB, cập nhật 17/10 tối)
- Không dùng banner. Nền kem sạch + logo xoay vào + "CITY TIMELAPSE" quét ra + gạch chân đất nung + tagline hiện từng chữ + câu "¿Qué ciudad reconstruimos después?".
- Thanh kênh ở đáy: logo + City Timelapse + Me gusta (bấm → ngón cái xanh) + Suscribirse đỏ (bấm → Suscrito) + chuông (bấm → vàng, rung, sóng); con trỏ bấm lần lượt. SFX click ×3 + chuông (lấy từ IronBehemoth-Videos/tools/video/common/sfx).
- Tool: `CityTimelapse-Videos/tools/ct_endcard.py <out_dir> [dur]` (mốc local: like 2,3s · sub 3,05s · bell 3,8s).

## Bài học / lưu ý
- Tải file từ Chrome: thư mục tải mặc định là `IronBehemoth/outputs/_flow`; Flow tải mỗi clip thành 1 zip "tải xuống.zip"; Chrome chặn tải tự động nhiều file — gộp thành 1 tar và bấm 1 lần.
- Veo Lite 720p → upscale 1080p hơi mềm. Clip "thuộc địa" gần như đứng yên; clip megalópolis ra thung lũng như sa mạc (không đúng CDMX) — cần prompt kỹ hơn (lòng hồ khô, cây xanh, núi lửa Popocatépetl/Iztaccíhuatl xa).
- Bộ đếm năm đang chạy tuyến tính, không gắn với năm xây thật như mẫu (mẫu dựng từ dữ liệu). Chưa có bộ đếm dân số.
- Hết tín dụng Flow sau 5 clip (17/10/2026).
