---
title: Quy tắc viết prompt Muse cho City Timelapse (rút từ QC 001 CDMX)
type: production
channel: city-timelapse
updated: 2026-10-18
sources: [Youtube-AI/CityTimelapse-Videos/001_ciudad-de-mexico/qc/]
---

# Quy tắc prompt Muse (bắt buộc đọc trước khi viết prompt tập mới)

QC 001 CDMX (2026-10-18): 50 clip → 13 hỏng + 2 lỗi đuôi clip. Nguyên nhân và quy tắc:

## 1. Từ chung chung → Muse lấy mẫu châu Âu/Mỹ
| Từ trong prompt | Muse vẽ ra | Viết thay bằng |
|---|---|---|
| cathedral, huge church, "two square bell towers" | nhà thờ Gothic kiểu Notre-Dame (avoid "no gothic" KHÔNG đủ — lượt 2 vẫn ra Gothic) | KHÔNG dùng chữ "cathedral"; tả "a wide pale church with a flat front, two bell towers with bell-shaped caps and a big dome" + avoid "no gothic, no spires" |
| castle, fortress-like | lâu đài cổ tích có tháp nhọn | "a long low palace" / "two-story flat-roofed stone palace with arcades" + avoid "no castle" |
| foundations, construction | công trường hiện đại, cần cẩu, máy xúc (ảnh thật) | "rises block by block" + avoid "no cranes" |
| ornate, baroque, neoclassical, art deco, French-style | ảnh thật siêu chi tiết, không thấy mọc lên | tả hình khối đơn giản (dome, square towers, arcades, low blocks) |
| stepped pyramid (ở thời hiện đại/khai quật) | kim tự tháp Maya nguyên vẹn khổng lồ | "low ruined stone walls of an old temple" + avoid "no pyramid" |
| skyscraper / mốc thế kỷ XX đầu | Manhattan, Capitol Mỹ | ghi rõ chiều cao "low four-story buildings" + avoid "no skyscrapers" |
| dike, wall across lake | thành phố Địa Trung Hải, cầu pháo đài, thuyền buồm | "low wall of stone and wooden posts" + avoid "no ships" |
| island city at peak (thời tiền thuộc địa) | lẫn nhà thờ mái vòm trắng | avoid "no domes, no churches" cho mọi beat trước năm thuộc địa |
| (không nhắc nước) | Muse tự thêm sông/hồ không có thật | chấp nhận được; nếu cần thì ghi "no river" |

## 1b. Cảnh đêm
- Cảnh đêm sa bàn đôi khi lộ phông vải tối phía sau (B049) và tàn tích "temple ruins" ra đền Hy Lạp–La Mã → viết "a low stone ruin".

## 2. Camera
- "Slow pull-back" dễ lộ mép bàn sa bàn ở cuối (B041) → beat chi tiết nhỏ dùng drift/orbit/lock.
- Clip hay mở bằng cận cảnh khác thời rồi mới kéo ra (B007, B012) → beat đầu chương nên tả rõ khung mở.

## 3. Diễn biến
- Beat "biến mất / bị dỡ bỏ" (B014 năm 1521): Muse luôn vẽ thứ MỌC LÊN → tạo cảnh mọc lên rồi phát ngược (`reverse`), đừng tả "gone/cleared".

## 4. Lỗi đuôi clip (Muse)
- Thỉnh thoảng 1–12 khung cuối nhảy sang cảnh người thật (B011, B030) dù có "no people". QC bắt buộc chạy dò cắt cảnh: `select='gt(scene,0.25)'`. Sửa: cắt đuôi + giãn về 10s (≤5%).
- Dò cắt cảnh báo nhầm khi công trình lớn hiện nhanh (B042) → luôn xem khung hình trước khi sửa.

## 5. Giới hạn ký tự
- visual_query ≤ 500, avoid ≤ 100; phần avoid chung giữ 72 ký tự để còn chỗ cho 2 mục riêng.

## Quy trình QC (mỗi đợt)
1. ffprobe (1280×720, 24fps, 10s) + giải mã không lỗi.
2. Dò cắt cảnh.
3. Contact sheet 3 khung (3%, 50%, 97%) mỗi beat; soi: đúng thời kỳ? đúng phong cách sa bàn? có mọc lên? lộ bàn/người/xe?
Liên quan: [[city-pipeline]] · [[ciudad-de-mexico]]
