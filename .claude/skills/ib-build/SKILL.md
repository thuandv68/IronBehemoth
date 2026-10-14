---
name: ib-build
description: Dựng video tập IronBehemoth từ CSV tài nguyên đã đủ: kiểm tra thiếu (thiếu thì dừng và báo), voice ai33, căn beat, đồ họa, shotmap, SFX, nhạc, render ffmpeg, QC, giao 1080p.
---

# ib-build — Dựng video (bước 3/3)

Đầu vào: `outputs/NNN_slug/` có `script.md`, `notes.md`, `beats/beats.tsv`, `beats/beats_NNN_slug.csv` (anh Aron đã điền tài nguyên). Tool trong `tools/video/` (đọc docstring đầu mỗi file + `BROWSER_SNIPPETS.md`). Báo tiến độ từng bước bằng tiếng Việt, ngắn gọn, để anh tự theo dõi.

## 0. Kiểm tra tài nguyên — THIẾU LÀ DỪNG
```
cd $HOME/mnt/IronBehemoth
python3 tools/video/ib_build.py outputs/NNN_slug check
```
- Tool tìm file theo cột `path` (đường dẫn tuyệt đối, tương đối, hoặc chỉ tên file Windows `D:\...\B001_A001.mp4` → tìm tên đó trong `beats/footage/`, `footage/`, `assets/`) hoặc theo tên bắt đầu bằng `asset_id`.
- Còn thiếu bất kỳ beat nào → **không dựng**: gửi anh danh sách `Bxxx(itemType)` + lời đọc + visual_query của từng beat thiếu, rồi dừng. `render` cũng tự từ chối (exit 2) khi thiếu tài nguyên, đồ họa, voice hoặc nhạc.

## 1. QC clip AI (trước khi làm voice)
Contact sheet mỗi clip (ffmpeg `fps=1/2,scale=320:-1,tile=4x1`, xem bằng Read). Loại: chữ vạn, sao Liên Xô sai phe, sai hình xe, người nhìn thẳng camera, chữ/logo, lạc đề. Clip hỏng → báo anh làm lại (vẫn tính là thiếu, không dựng). Ghi chú clip tối/lỗi đầu-cuối để đặt `off=`/`speed=` trong shotmap.

## 2. Voice ai33
- Key + voice id nằm ở `.secrets/ai33.env` (device shell: `cat $HOME/mnt/IronBehemoth/.secrets/ai33.env`). Chỉ đưa vào biến JS lúc gọi; không in ra chat, không ghi vào file/skill/log. Không có file → hỏi anh.
- Giọng kênh: Russ `elevenlabs_t0eCaS57KWbQQc1wRkah`, `eleven_multilingual_v2`, speed khởi đầu 0.85. Không clone giọng người thật.
- Gọi trong tab Chrome (máy và container không ra mạng) theo `BROWSER_SNIPPETS.md` → bundle JSON về `~/Downloads` → `python3 tools/video/ib_unbundle.py ~/Downloads/<bundle>.json outputs/NNN_slug/audio` → `audio/voice.mp3`, `audio/voice.json`.
- Đo thời lượng: phải ra video 16:00–16:59 (voice + ~10 giây end card). Lệch → chỉnh `tempo` trong `ib.json` (0.92–1.05) hoặc tạo lại với speed khác.

## 3. Căn beat
`python3 tools/video/ib_align.py outputs/NNN_slug` → `build/beat_times.json`. Khớp từ phải ≥ 95%; thấp hơn → voice không khớp script, kiểm tra lại.

## 4. Cấu hình + nhạc
- `build/ib.json` từ `templates/ib.json`: `ep`, `name`, `csv`, `end_at` (beat có câu kêu gọi subscribe cuối), `tempo`, `music_ss`, `skip_ai`, `duck` (hạ nhạc ở khoảnh khắc lặng, ví dụ beat "Fire.").
- Nhạc: YouTube Studio → Thư viện âm thanh (từ khóa epic/dark cinematic/tension), tải bằng Chrome, lưu `audio/music.mp3`, ghi tên bài + tác giả vào `credits.md`. Anh có nhạc riêng thì dùng của anh.

## 5. Đồ họa `build/gfx.txt` → `ib_gfx.py`
Từ `notes.md` (bảng thông số) viết spec (mẫu `templates/gfx.txt`): `title` (INSIDE THE / TÊN XE / dòng phụ), `chapter` cho 3 câu hỏi, `ov` cho 6–12 con số lớn, `lt` (DRAMATIZATION ở cảnh dựng lại đầu video; ảnh tư liệu: tên + năm + nguồn), `card` cho con số chủ đạo (ví dụ 18), `q` cho danh sách 3 câu hỏi. Chữ trên màn hình tiếng Anh, viết hoa. `python3 tools/video/ib_gfx.py outputs/NNN_slug`. Thanh subscribe và end card tự tạo khi render.

## 6. Shotmap
`python3 tools/video/ib_build.py outputs/NNN_slug shotmap` → `build/shotmap.txt` (mỗi beat một shot, tự gộp beat < 1,6 giây). Sửa tay:
- Overlay `ten.png@giây@thờilượng`: `lt_drama` ở B001, `title.png@0.25@4.6` ở beat có câu "This is the <Xe>", `chapter_qN` ở beat "Question one/two/three", `ov_*` ở beat nói con số, `q1/q2/q3` khi nêu 3 câu hỏi.
- Thẻ toàn màn hình: `Bxxx gfx:card_18.png none`.
- Clip: `off=` bỏ đoạn đầu tối/lỗi, `speed=0.8` kéo dài clip ngắn hơn beat, `zoom=`.
- Subscribe giữa video: thêm `seq:subscribe@0.4` vào beat có chữ "subscribe"; shot đó ≥ 5,3 giây (gộp beat nếu cần). Nền là footage của chính đoạn đó, không banner; thanh giữa phía dưới; đúng 1 tiếng click + chuông (tool tự thêm).
- Dòng cuối `Bxxx_END seqv:endcard none seq:subscribe@1.0` với Bxxx = `end_at`: end card động chạy dưới câu kêu gọi cuối và giữ `endcard_tail` giây. Không có teaser tập chưa làm.

## 7. SFX `build/sfx.txt`
Mẫu `templates/sfx.txt`: `file  Bxxx[+/-giây]|t=giây  volume  [thời lượng]`. Bộ có sẵn ở `tools/video/common/sfx/` (mk_* Mixkit + sfx_*). Đặt tiếng ở khoảnh khắc hook (đóng nắp, bắn, nổ, sập), không quá dày. Tool tự thêm whoosh/impact cho chapter, click cho ov/lt, click + chuông cho subscribe, whoosh cho end card. Thiếu tiếng → tìm trên Mixkit (BROWSER_SNIPPETS), lưu `audio/sfx/`.

## 8. Render
- Render trong container (nhanh hơn): stage `outputs/NNN_slug` (beats/footage, audio, build, gfx, beats csv/tsv; ≤ 50 file mỗi lần stage) và `tools/video` vào container, giữ cấu trúc thư mục.
- Preview: `python3 ib_build.py <EP> render --preview --jobs 4` → `full/IBNNN_<Xe>_720p_preview.mp4`. Gửi anh duyệt (nén ≤ 30 MB nếu cần).
- Sửa: đổi dòng shotmap nào thì chỉ shot đó dựng lại (cache theo nội dung dòng). `--test i,j` dựng thử vài shot.
- Bản cuối: `render --jobs 4` → `full/IBNNN_<Xe>_1080p.mp4`.

## 9. QC bản dựng
- Contact sheet mỗi 10 giây + xem kỹ hook, 3 chapter, các overlay số, đoạn subscribe, end card. Không còn khung "MISSING", không khung đen, không ngôi sao watermark Flow (ghi `provider=flow` để tool tự xóa; clip Muse không cần).
- Loudness `ebur128`: −15 ± 1 LUFS, peak ≤ −1 dBFS. Thời lượng 16:00–16:59.

## 10. Giao file
- 1080p: cắt segment 12 giây, chép sang `outputs/NNN_slug/full/parts/` theo lô ≤ 92 MB (SendUserFile → device_commit_files), ghép trên máy trong `$HOME/work` bằng `ffmpeg -f concat -c copy -movflags +faststart` rồi chép vào `full/IBNNN_<Xe>_1080p.mp4`; bản anh duyệt cuối → `IBNNN_<Xe>_FINAL_1080p.mp4`.
- Gửi anh bản nén xem nhanh qua chat.
- `credits.md` (ảnh Wikimedia tác giả + giấy phép, footage, nhạc, "AI reconstructions", "Narration: AI voice (ai33)"); cập nhật chapters thật trong `notes.md` theo `beat_times.json`; ghi `log.md`; nhắc tick "altered or synthetic content" khi đăng.

## An toàn
Không tạo tài khoản, đăng nhập, mua hàng hay đăng ký license thay anh; chấp nhận điều khoản/Envato license cần anh đồng ý trong chat. Chỉ xóa file khi anh yêu cầu.
