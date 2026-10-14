# LLM Wiki pattern (Karpathy)

Nguồn: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (đọc 2026-10-11)

Tóm tắt:
- Ba lớp: nguồn thô (bất biến, sự thật gốc) → wiki markdown do LLM viết và duy trì → schema (CLAUDE.md/AGENTS.md) quy định cấu trúc, quy ước, quy trình.
- `index.md`: danh mục nội dung theo nhóm, mỗi trang một dòng tóm tắt; LLM đọc trước khi trả lời, cập nhật mỗi lần ingest.
- `log.md`: nhật ký chỉ-thêm (ingest, query, lint) với tiền tố thống nhất để grep.
- Thao tác: ingest, query (câu trả lời tốt lưu lại thành trang), lint (mâu thuẫn, trang mồ côi, khoảng trống).
- Cấu trúc thư mục cụ thể tùy chỉnh theo lĩnh vực.
