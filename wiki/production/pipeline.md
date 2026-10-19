---
title: Quy trình sản xuất
type: production
updated: 2026-10-11
sources: [raw/references/2026-10-11_owner-decisions.md]
---

# Quy trình sản xuất một tập

| Bước | Việc | Đầu ra (`IronBehemoth-Videos/NNN_slug/`) | Công cụ |
|---|---|---|---|
| 1 | Chọn xe từ [[topic-backlog]] | — | — |
| 2 | Nghiên cứu, tạo/cập nhật `wiki/tanks/<xe>.md` (thông số + nguồn + câu chuyện trận đánh + chi tiết đặc biệt) | wiki tank page | Web search, sách |
| 3 | Dàn ý theo [[episode-template]] | `outline.md` | — |
| 4 | Viết script 2.320–2.460 từ theo [[script-style]] | `script.md` | — |
| 5 | Tìm footage/ảnh public domain theo [[footage-sources]] | `footage/footage-list.md` | DVIDS, NARA, archive.org, Wikimedia |
| 6 | Chia beat 8s, gán AI/FOOTAGE, viết prompt theo [[visual-locks]] | `shot-plan.md`, `beat-index.csv` | — |
| 7 | Tạo clip AI | `clips/BNNN_A.mp4` | Google Flow qua AIVideoBuilder |
| 8 | Tải/cắt footage | `clips/BNNN_F.mp4` | — |
| 9 | Voiceover | `audio/voiceover.wav` | TTS |
| 10 | Dựng: ghép theo mã beat, nhạc, SFX, chapter | `render/final.mp4` | CapCut / Premiere / DaVinci |
| 11 | Thumbnail theo [[thumbnail-formula]] (2 phương án) | `thumbnail/` | Image model |
| 12 | Publish pack: tiêu đề, description, chapters, tags, nguồn | `publish.md` | — |
| 13 | Trailer Short 60s | `short/` | — |
| 14 | Ghi log, cập nhật backlog, sau 7 ngày ghi số liệu vào [[performance-tracker]] | — | — |

## Ngân sách thời gian mục tiêu (2 tập/tháng)
- Nghiên cứu + script: 1,5 ngày
- Shot plan + prompt: 0,5 ngày
- Tạo clip AI (~62 clip, tính cả tạo lại): 1–2 ngày chạy hàng đợi
- Dựng + thumbnail + publish: 1,5 ngày

## Quy tắc dựng (cập nhật 2026-10-13, từ tập 001)
- Dựng bằng `IronBehemoth-Videos/tools/video/` (align_beats → make_gfx_full + make_subscribe → shotmap → build_full), master 1080p, −15 ± 1 LUFS, peak ≤ −1 dBFS.
- Chỉ dựng khi đủ clip AI, voiceover + transcript, nhạc và footage.
- QC clip AI trước khi dựng: chữ vạn, sao Liên Xô, sai hình xe, người thật nhìn camera → bỏ (SKIP_AI).
- Kêu gọi subscribe: nền là footage của đoạn đó (không dùng banner), thanh kênh giữa phía dưới (logo, tên, Subscribe → Subscribed, chuông; không Like), âm thanh đúng 1 tiếng click + chuông, đặt vào beat có chữ "subscribe", shot ≥ 5,3 giây.
- End card động bắt đầu ngay ở câu kêu gọi subscribe cuối, chạy dưới lời đọc rồi giữ 10 giây sau đó, chỉ 1 thanh subscribe (logo xoay vào, chữ quét ra, gạch cam, tagline, thanh subscribe + chuông) bằng `IronBehemoth-Videos/tools/video/make_endcard.py`. Chỉ giới thiệu tập sau khi tập đó đã có; nếu chưa có thì kết thúc ở câu kêu gọi subscribe (`build_full.py --end-at <beat>`).

## Quy trình 3 skill (từ 2026-10-14)
| Skill | Đầu vào | Đầu ra |
|---|---|---|
| `ib-script` | Tiêu đề + kịch bản mẫu (file hoặc folder đối thủ) | `analysis_NNN.md`, `script.md`, `review_NNN.md`, `notes.md` |
| `ib-assets` | `script.md` | `beats/beats.tsv`, `beats/beats_NNN_slug.csv` theo mẫu `raw/assets/mau_beat.csv` (anh Aron tự tìm tài nguyên) |
| `ib-build` | CSV đã đủ tài nguyên | `full/IBNNN_<Xe>_1080p.mp4` |

- Độ dài beat theo công cụ video AI: Veo 3 / Flow 8 giây (`--clip 8`, ≤ ~20 từ), Muse 10 giây (`--clip 10`, ≤ ~24 từ).
- Tool dùng chung: `IronBehemoth-Videos/tools/video/` (`ib_beats.py`, `ib_align.py`, `ib_gfx.py`, `ib_build.py`, `ib_unbundle.py`, `make_subscribe.py`, `make_endcard.py`, `templates/`, `BROWSER_SNIPPETS.md`). Tool riêng tập 001 chuyển vào `IronBehemoth-Videos/tools/video/legacy_001/`.
- `ib_build.py render` từ chối dựng khi còn thiếu tài nguyên, đồ họa, voice hoặc nhạc.
- Watermark ngôi sao chỉ có ở clip Flow (`provider=flow`), clip Muse không xử lý.
- Key ai33 nằm ở `.secrets/ai33.env` (đã gitignore), không ghi vào skill hay wiki.

- **End card kiểu chồng lên cảnh cuối (từ 2026-10-18, mặc định):** `ib_build.py` dùng clip của beat kêu gọi cuối (END_AT), quay chậm cho đủ thời lượng, rồi chồng `make_endcard.py --overlay` (logo + IRON BEHEMOTH trắng + tagline trên lớp tối mờ, PNG trong suốt) và thanh Subscribe. Không còn nền banner. Muốn quay lại banner: `"endcard_style": "banner"` trong `build/ib.json`. Bản cũ: `tools/video/*.bak_overlay`.
