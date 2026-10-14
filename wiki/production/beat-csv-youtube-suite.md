---
title: Chia beat cho youtube-suite
type: production
updated: 2026-10-11
sources: [youtube-suite/ARCHITECTURE.md, youtube-suite/features/footage/docs/ARCHITECTURE.md, youtube-suite/features/generation/README.md, youtube-suite/examples/csv_input_simple.csv]
---

# Chia beat và CSV cho youtube-suite

youtube-suite đọc **một CSV project** làm hợp đồng chung giữa các tính năng. Video AI ghi vào `<thư mục CSV>/footage/<asset_id>.mp4`. Mỗi asset làm xong được ghi ngược `provider` và `path` vào đúng dòng.

## Cột CSV

| Cột | Bắt buộc | Ai đọc | Ghi chú |
|---|---|---|---|
| `asset_id` | ✔ | tất cả | Mã duy nhất, dạng `B001_A01` (beat + số asset). Dùng làm tên file. |
| `item_type` | ✔ | tất cả | `footage` = video stock, `image` = ảnh stock, `veo3` = video AI (Google Flow Veo 3.1 Lite hoặc Muse). |
| `visual_query` | ✔ | tất cả | footage/image: **từ khóa tìm kiếm ngắn tiếng Anh**. veo3: **prompt video đầy đủ tiếng Anh**. |
| `min_media_length`, `max_media_length` | tùy | footage | Giây, ví dụ 5 và 30. |
| `avoid` | ✔ (cột) | footage/image | Thứ AI chấm điểm phải tránh khi chọn card. |
| `provider`, `path` | để trống | app tự ghi | Xóa `path` thì dòng đó được làm lại. |
| `main_idea` | tùy | lưu kèm | Ý chính của đoạn. |
| `beat_id`, `script` | tùy | app bỏ qua | Giữ để đối chiếu lời đọc. |
| `est_seconds`, `image_prompt` | thêm | app bỏ qua | Thời lượng ước tính; prompt ảnh khởi đầu (start frame) cho dòng veo3. |

- Tìm footage bỏ qua dòng `veo3`. Tạo video (VEO3 hoặc Muse) chỉ chạy dòng `veo3`, dòng nào đã có file thì bỏ qua.
- Muse tự thêm tiền tố "Tạo video 16:9" và gửi theo lô 3–5 prompt, mỗi prompt kèm mã `[asset_id]`.
- **Tạo ảnh AI chưa có trong tool.** Prompt ảnh đặt ở cột `image_prompt` để dùng tay (Flow, Imagen…) hoặc dùng khi tool có tính năng này.

## Quy tắc chia beat (Iron Behemoth)

1. Mỗi beat chứa **tối đa ~20 từ**, đọc ở ~145 từ/phút là khoảng 8 giây, khớp giới hạn clip Veo/Flow.
2. Gộp câu dưới 6 từ vào beat kề bên. Câu dài trên 22 từ thì tách ở dấu phẩy.
3. Mỗi beat **1 asset** (`_A01`). Beat dài hơn 8 giây hoặc cần cắt nhanh thì thêm `_A02`.
4. Chọn `item_type`:
   - **veo3**: cảnh riêng của xe (King Tiger, kíp lái, bên trong khoang, chiến trường 1944). Kho stock không có những cảnh này.
   - **footage**: cảnh chung, stock dễ có: tuyết, rừng, lửa, đồng hồ nhiên liệu, xe hơi, máy bay, cây cầu, nhà máy.
   - **image**: ảnh bảo tàng, ảnh tư liệu, bản vẽ kỹ thuật. Ảnh xe thật cụ thể (King Tiger 213…) nên lấy tay từ Wikimedia và ghi nguồn.
   - Không để quá 3 beat liên tiếp cùng loại nếu có thể.
5. Prompt veo3 gồm: **cảnh cụ thể** + khóa XE (King Tiger…) khi có xe + khóa KÍP LÁI khi có người + khóa STYLE (phim tài liệu WWII, mùa đông 1944, hạt phim, máy quay chậm, 8 giây, không chữ, không chữ vạn, không nhìn thẳng máy quay).
6. Từ khóa footage ngắn (3–6 từ), tiếng Anh, tả cái nhìn thấy được. Không đưa tên riêng của xe vào từ khóa stock.
7. `avoid` cho cảnh WWII: `modern vehicles, modern military, desert, airsoft, video game, cartoon, text overlay, vertical video, swastika, smiling people`.

## File cho tập 001

- `beats_001_king-tiger.csv`: đủ 173 beat (114 veo3 · 45 footage · 14 image), ước tính 16,8 phút.
- `beats_001_veo3.csv`, `beats_001_footage.csv`, `beats_001_image.csv`: tách sẵn theo loại để chạy từng phần.
