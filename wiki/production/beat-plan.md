---
title: Quy tắc beat plan
type: production
updated: 2026-10-11
sources: [raw/references/2026-10-11_owner-decisions.md]
---

# Beat plan

- 1 beat = 8 giây (giới hạn clip Google Flow) ≈ ≤20 từ lời đọc.
- Gộp đoạn < 6 từ vào beat kề.
- ~124 beat/tập; ~50% AI (`BNNN_A.mp4`), ~50% FOOTAGE (`BNNN_F.mp4`, gồm footage + ảnh tư liệu có Ken Burns).
- Không quá 3 beat liên tiếp cùng loại.
- Clip nối tiếp clip trước ghi `CONTINUES Bxxx` và dùng frame cuối clip trước làm start frame.
- Hook (B001–B005) ưu tiên AI hành động mạnh; chương Into Battle trộn dày footage thật.

## Định dạng `shot-plan.md`
```
## B001 — AI — file: B001_A.mp4
SCRIPT: ...
STYLE/TANK/CREW/AUDIO/NEG: (lock)
0–2s: ...
2–6s: ...
6–8s: ...
START FRAME: ...
```
Header phải khớp regex của AIVideoBuilder: `^## (B\d{3,4}) — (AI|FOOTAGE)\b.*?file:\s*(\S+)`.

## `beat-index.csv`
Cột: `beat,type,file,source,script,video_prompt,start_frame_prompt` — `video_prompt` là cột đẩy vào Flow.
