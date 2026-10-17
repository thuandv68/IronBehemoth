---
name: ib-script
description: Viết kịch bản tập IronBehemoth "Inside the [Xe]" (16:00–16:59) từ tiêu đề + kịch bản mẫu/folder đối thủ: phân tích mẫu, nghiên cứu, script voiceover-ready, review board, audit chính sách, fact-check, QC, notes.
---

# ib-script — Viết kịch bản (bước 1/3)

Kênh IronBehemoth, thư mục `/Users/thuandoan/Youtube-AI/IronBehemoth` (device shell: `$HOME/mnt/IronBehemoth`). Đọc `CLAUDE.md`, `index.md`, `wiki/format/script-style.md`, `wiki/format/episode-template.md` trước khi viết.
Làm tự động, giữa các phase chỉ báo 1–2 câu bằng tiếng Việt để anh Aron theo dõi. Bước tiếp theo là `ib-assets`.

## Đầu vào (anh Aron cung cấp)
- Tiêu đề tập, ví dụ `Inside the Sturmtiger`.
- Kịch bản mẫu: một file (`script.txt`) hoặc folder đối thủ (script + video + voice). Thiếu một trong hai → hỏi ngay, không đoán.

## Phase 0 — Chuẩn bị
- Số tập NNN = số lớn nhất trong `IronBehemoth-Videos/` + 1; slug = tên xe viết thường, gạch nối (`002_sturmtiger`).
- Tạo `IronBehemoth-Videos/NNN_slug/`, chép mẫu vào `IronBehemoth-Videos/NNN_slug/doi-thu/` (giữ nguyên, không sửa). Lưu bản gốc vào `raw/assets/video-doi-thu/<TenVideo>/` nếu chưa có.

## Phase 1 — Phân tích kịch bản mẫu → `analysis_NNN.md`
- Tổng số từ; nếu có video/voice: thời lượng (ffprobe) và wpm.
- Mở bài: cấu trúc, độ dài (từ + giây), có CTA không, tóm tắt ý chính.
- Thân bài: các chương, độ dài từng chương, kỹ thuật giữ chân (open loop, câu hỏi, con số gây sốc), ý chính.
- Kết bài: cấu trúc, CTA, câu chốt.
- Đánh giá: điểm mạnh, điểm yếu, cần cải tiến; kiểm tra từng con số với nguồn và liệt kê lỗi sai của mẫu.
- Chỉ học cấu trúc và dữ kiện, không dùng câu chữ của đối thủ.

## Phase 2 — Nghiên cứu
- WebSearch các nguồn: Wikipedia, The Tank Museum, NavWeaps, Tank Historia, War Thunder history, sách. Mỗi thông số ghi nguồn.
- Tạo/cập nhật `wiki/tanks/<xe>.md`, lưu ghi chú `raw/tanks/YYYY-MM-DD_<xe>.md`.

## Phase 3 — Dàn ý
- Hook cao trào trong 60 giây đầu: dựng một cảnh cụ thể, đẩy tới khoảnh khắc đỉnh (bắn, nổ, sập), rồi câu twist "But here is the strange part" và một câu hỏi lớn.
- 3 câu hỏi xương sống, mỗi phần thân mở bằng "Question one/two/three".
- Mỗi 60–90 giây một "moment" (con số so sánh đời thường, chi tiết người trong xe). Cài 2 open loop sớm và trả lời muộn.
- CTA subscribe lần 1 ngay sau hook (~2:00); kết bằng CTA bình luận + tập đã có của kênh + subscribe. Không giới thiệu tập chưa làm.

## Phase 4 — Viết `script.md`
- 2.320–2.460 từ (148 wpm → 16:00–16:59). Báo số từ và thời lượng ước tính.
- Voiceover-ready: không ngoặc, không marker, không tiêu đề chương trong lời đọc, không chữ số (viết bằng chữ), chỉ đơn vị mét/kg, mỗi câu một dòng, câu dài nhất ≤ 30 từ.
- Dòng đầu `# Inside the <Xe>` (dòng `#` bị bỏ qua khi chia beat).

## Phase 5 — Hội đồng review cấp cao
Đóng vai biên tập viên tài liệu, sử gia quân sự, chuyên gia retention YouTube, đạo diễn voiceover. Chấm hook, cấu trúc, retention, yếu tố con người, độ chính xác, độ sẵn sàng đọc (thang 10). Sửa thẳng vào script, ghi bảng phát hiện → thay đổi vào `review_NNN.md`.

## Phase 6 — Audit chính sách YouTube
Bạo lực/gore, ca ngợi chế độ cực đoan (không nêu tên lãnh đạo Nazi, không chữ vạn), thông tin sai lệch (nói rào khi nguồn không chắc), nhãn nội dung AI (altered/synthetic), ad-friendly. Ghi vào `review_NNN.md`.

## Phase 7 — Fact-check
Bảng claim | kết luận | nguồn cho mọi con số và khẳng định. Không chắc → làm tròn hoặc "around/about/accounts put". Ghi các lỗi đã sửa so với mẫu.

## Phase 8 — QC
Độ dài, voiceover-ready, câu dài, danh sách từ khó đọc cho TTS, tính nhất quán con số, open loop đã trả lời, vị trí CTA, chính sách, fact. Ghi bảng QC vào `review_NNN.md`.

## Phase 9 — `notes.md` và đóng sổ
- `notes.md` theo format `IronBehemoth-Videos/002_sturmtiger/notes.md`: số từ/thời lượng, vị trí subscribe, nghịch lý trung tâm, 3 câu hỏi, open loop, 3 tiêu đề, bảng thông số dùng trong script (giá trị + ghi chú), nguồn, gợi ý description (EN), chapters ước tính.
- Chỉ giữ bản cuối: `script.md`, `analysis_NNN.md`, `review_NNN.md`, `notes.md`, `doi-thu/`.
- Thêm dòng `produce` vào `log.md`, cập nhật `wiki/strategy/topic-backlog.md` và `index.md`.
- Báo: số từ, thời lượng ước tính, 3 tiêu đề; gợi ý chạy `ib-assets`.
