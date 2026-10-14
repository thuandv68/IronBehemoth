---
title: Công thức thumbnail
type: format
updated: 2026-10-11
sources: [raw/competitors/2026-10-11_blue-paw-print-inside-series.md]
---

# Công thức thumbnail

## Bố cục
- **Một** chiếc xe, góc 3/4 trước-bên, chiếm 70–80% khung, hơi thấp (camera ngang xích) để xe trông đồ sộ.
- Nền đen tuyền hoặc gradient than → đen.
- **Mặt cắt lai**: một phần thân/tháp pháo bị cắt hoặc trong suốt, lộ ghế kíp lái, đạn, động cơ phát sáng cam.
- Rim light ấm từ sau, key light lạnh phía trước — tách xe khỏi nền.
- **Không chữ**. Không mũi tên, không khung đỏ.

## Khác biệt nhận diện kênh
- Luôn có một điểm sáng cam `#E0662B` (động cơ hoặc đạn) — dấu hiệu thương hiệu.
- Có thể có 1 bóng người kíp lái nhỏ bên trong để gợi "crew story".

## Prompt khung (image model)
```
Studio cutaway render of a [TANK NAME, exact variant], three-quarter front view, low camera angle at track height, the [left side hull and turret] cut away to reveal the interior: crew seats, [main gun breech], stacked [shell type] rounds, glowing orange engine bay at the rear. Pure black background, warm rim light from behind, cool key light from front left, hyper-detailed military museum quality, accurate proportions, historically accurate markings [national cross / star], no text, no logos, 16:9.
```

## Kiểm tra trước khi đăng
- Đúng biến thể xe (số bánh, hình tháp pháo, nòng, phanh đầu nòng).
- Không có chữ vạn hay biểu tượng cấm; xe Đức dùng Balkenkreuz.
- Xem ở kích thước nhỏ (mobile) vẫn nhận ra hình xe.
