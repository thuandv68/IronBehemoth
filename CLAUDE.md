# CLAUDE.md — IronBehemoth Wiki Schema

Bạn là người bảo trì "bộ não 2" của kênh YouTube **IronBehemoth** (faceless, tiếng Anh, chủ đề xe tăng chiến đấu, format "Inside the …"). Mô hình: LLM Wiki của Karpathy — nguồn thô bất biến, wiki do LLM viết và giữ nhất quán, index + log để điều hướng.

## Cấu trúc

Thư mục này **chỉ chứa não 2** (kiến thức). Mọi thứ sản xuất (các tập video, tool dựng, website) nằm ở thư mục anh em `Youtube-AI/IronBehemoth-Videos/` (tách ngày 2026-10-16). Đường dẫn `IronBehemoth-Videos/...` trong wiki và skill tính từ thư mục `Youtube-AI/`; lệnh `python3 IronBehemoth-Videos/tools/video/...` chạy từ `Youtube-AI/`. Key API vẫn ở `IronBehemoth/.secrets/` (không đưa sang thư mục video).

| Đường dẫn | Vai trò | Ai ghi |
|---|---|---|
| `raw/` | Nguồn thô: dữ liệu đối thủ, tài liệu xe tăng, ghi chú nghiên cứu, ảnh (`raw/assets/`). **Không bao giờ sửa** sau khi thêm. | Người dùng / LLM khi ingest dữ liệu thu thập |
| `wiki/` | Kiến thức đã tổng hợp: kênh, format, sản xuất, chiến lược, đối thủ, xe tăng. | LLM |
| `wiki/channel/` | Danh tính kênh, thương hiệu, khán giả | LLM |
| `wiki/format/` | Công thức tập phim: chương, tiêu đề, thumbnail, hook, văn phong | LLM |
| `wiki/production/` | Quy trình sản xuất, visual locks, beat plan, nguồn footage | LLM |
| `wiki/strategy/` | Backlog chủ đề, phát hành & tăng trưởng, rủi ro | LLM |
| `wiki/competitors/` | Hồ sơ đối thủ | LLM |
| `wiki/tanks/` | Một trang cho mỗi xe tăng (tạo khi nghiên cứu tập) | LLM |
| `../IronBehemoth-Videos/NNN_slug/` | (ngoài thư mục này) Sản phẩm từng tập: script, publish, shot plan, beat index, footage list | LLM |
| `.claude/skills/` | Skill dự án: `ib-episode` (làm tập), `ib-wiki` (ingest/query/lint) | Người dùng + LLM |
| `index.md` | Danh mục mọi trang wiki, theo nhóm, mỗi dòng 1 câu tóm tắt | LLM, cập nhật mỗi lần ingest |
| `log.md` | Nhật ký chỉ-thêm của ingest / query / lint / produce | LLM |

## Não dùng chung nhiều kênh (từ 2026-10-17)

Não này dùng chung cho nhiều kênh; mỗi kênh có thương hiệu, skill và thư mục sản xuất riêng.

| Kênh | Wiki | Raw | Sản xuất |
|---|---|---|---|
| IronBehemoth (xe tăng) | `wiki/` (các nhóm channel/format/production/strategy/competitors/tanks ở gốc) | `raw/` (gốc) | `Youtube-AI/IronBehemoth-Videos/` |
| City Timelapse (@CityTimelapseHQ đề xuất; 3D timelapse lịch sử thành phố) | `wiki/city-timelapse/` (channel/format/production/strategy/competitors/cities) | `raw/city-timelapse/` | `Youtube-AI/CityTimelapse-Videos/` |

- Trang của kênh không phải IronBehemoth có thêm trường frontmatter `channel: <slug>`; tên file phải duy nhất toàn não (vd. `city-overview`, không dùng `overview`).
- "Quy tắc cứng của kênh" bên dưới chỉ áp dụng cho IronBehemoth; quy tắc kênh City Timelapse nằm ở [[city-overview]] và [[city-format-blueprint]].
- Skill `ib-*` chỉ dành cho IronBehemoth.
- Kênh City Timelapse lên sóng bằng **tiếng Tây Ban Nha** (title, description, chữ trên màn hình); nội dung nội bộ vẫn tiếng Việt.

## Quy ước trang wiki

- Frontmatter YAML: `title`, `type` (channel|format|production|strategy|competitor|tank), `updated` (YYYY-MM-DD), `sources` (đường dẫn trong `raw/`).
- Liên kết chéo bằng `[[ten-trang]]` (tên file không đuôi).
- Một chủ đề một trang. Sự thật luôn dẫn nguồn `raw/...` hoặc URL. Thông số kỹ thuật chưa kiểm chứng đánh dấu `(cần kiểm chứng)`.
- Nội dung nội bộ viết tiếng Việt; mọi thứ lên kênh (title, description, script) viết tiếng Anh.

## Quy tắc cứng của kênh (IronBehemoth)

- Thời lượng video **16:00–16:59** (mục tiêu 16:30). Lời dẫn **2.320–2.460 từ** (~145 wpm; hiệu chỉnh theo giọng TTS thực tế).
- Script **voiceover-ready**: không ngoặc, không ký hiệu sản xuất, không tiêu đề chương trong lời đọc.
- Beat 8s (giới hạn Google Flow), ≤20 từ/beat, ~50% AI / 50% footage-ảnh tư liệu, không quá 3 beat liên tiếp cùng loại.
- Tiêu đề dạng `Inside the [Tên xe]`.
- Chỉ dùng footage public domain hoặc giấy phép rõ ràng (xem [[footage-sources]]).

## Quy trình

### Ingest (thêm nguồn)
1. Lưu nguồn vào `raw/<nhóm>/YYYY-MM-DD_slug.md` (không sửa nguồn cũ).
2. Đọc nguồn, cập nhật/tạo các trang wiki liên quan, giữ liên kết chéo.
3. Cập nhật `index.md`.
4. Thêm dòng vào `log.md`.

### Query (hỏi đáp)
1. Đọc `index.md` trước, mở trang liên quan, trả lời có dẫn trang.
2. Câu trả lời có giá trị lâu dài → lưu thành trang wiki mới, ghi log.

### Lint (rà soát)
Kiểm tra: mâu thuẫn giữa các trang, trang mồ côi (không có trong index), liên kết hỏng, thông số `(cần kiểm chứng)` tồn đọng, backlog lỗi thời. Ghi kết quả vào log.

### Produce (làm tập)
Theo skill `ib-episode`. Kết quả vào `IronBehemoth-Videos/NNN_slug/`, tạo/cập nhật `wiki/tanks/<xe>.md`, cập nhật [[topic-backlog]], ghi log.

## Định dạng log

```
## [YYYY-MM-DD] <ingest|query|lint|produce|setup> | <tiêu đề ngắn>
- chi tiết 1
- trang bị ảnh hưởng: [[...]]
```
