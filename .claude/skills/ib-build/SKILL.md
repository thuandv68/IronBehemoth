---
name: ib-build
description: Dựng video tập IronBehemoth từ CSV tài nguyên đã đủ: kiểm tra thiếu (thiếu thì dừng và báo), voice ai33, căn beat, đồ họa, shotmap, SFX, nhạc, render ffmpeg, QC, giao 1080p.
---

# ib-build — Dựng video (bước 3/3)

Đầu vào: `IronBehemoth-Videos/NNN_slug/` có `script.md`, `notes.md`, `beats/beats.tsv`, `beats/beats_NNN_slug.csv` (anh Aron đã điền tài nguyên). Tool trong `IronBehemoth-Videos/tools/video/` (đọc docstring đầu mỗi file + `BROWSER_SNIPPETS.md`). Báo tiến độ từng bước bằng tiếng Việt, ngắn gọn, để anh tự theo dõi.

## 0. Kiểm tra tài nguyên — THIẾU LÀ DỪNG
```
cd $HOME/mnt/IronBehemoth
python3 IronBehemoth-Videos/tools/video/ib_build.py IronBehemoth-Videos/NNN_slug check
```
- Tool tìm file theo cột `path` (đường dẫn tuyệt đối, tương đối, hoặc chỉ tên file Windows `D:\...\B001_A001.mp4` → tìm tên đó trong `beats/footage/`, `footage/`, `assets/`) hoặc theo tên bắt đầu bằng `asset_id`.
- Còn thiếu bất kỳ beat nào → **không dựng**: gửi anh danh sách `Bxxx(itemType)` + lời đọc + visual_query của từng beat thiếu, rồi dừng. `render` cũng tự từ chối (exit 2) khi thiếu tài nguyên, đồ họa, voice hoặc nhạc.

## 1. QC clip AI (trước khi làm voice)
Contact sheet mỗi clip (ffmpeg `fps=1/2,scale=320:-1,tile=4x1`, xem bằng Read). Loại: chữ vạn, sao Liên Xô sai phe, sai hình xe, người nhìn thẳng camera, chữ/logo, lạc đề. Clip hỏng → báo anh làm lại (vẫn tính là thiếu, không dựng). Ghi chú clip tối/lỗi đầu-cuối để đặt `off=`/`speed=` trong shotmap.

## 2. Voice ai33 — giọng clone của kênh (từ 19/10/2026)
- Giọng kênh: **IB-Clone `clone_2700943`** (giọng anh Aron, clone trên ai33 từ `IronBehemoth-Videos/_voice_clone/thuandv_clone_29s.wav`; nhà cung cấp MiniMax speech-02-hd). Giọng Russ cũ chỉ dùng khi anh yêu cầu.
- Mục tiêu: khán giả không thấy "máy móc / giọng AI". Quy tắc bắt buộc:
  - **Speed 1.0, không kéo tempo** (`tempo` trong ib.json = 1.0). Kéo chậm speed 0.85 + atempo là nguyên nhân giọng Russ bị chê robot.
  - **Chia theo chương**: mỗi chương (mốc chapters trong notes.md) đọc thành 1 đoạn riêng (~100–350 từ) → `audio/clone/chunk_NN.txt`. Không đọc cả bài một lần.
  - **Ngắt nghỉ có chủ đích** bằng thẻ `<break time="0.3s"/>` sau câu ngắn ≤ 6 từ / câu "đinh", sau câu hỏi; `0.6s` giữa đoạn văn và trước "Question one/two/three". Không thêm quá dày (giọng tự nghỉ ~0.6 s cuối câu).
  - Bật **"Xuất kèm phụ đề"** để có transcript từng từ (`json_url` = cùng tên file mp3 đổi `.mp3`→`.json`).
- Cách chạy (web ai33, tab Chrome; key API bị hệ thống chặn đưa vào JS thì dùng giao diện web): chọn giọng **Giọng nhân bản → IB-Clone**, dán từng chunk, bấm tạo, chờ "Xong"; xong 10 đoạn thì tải 1 bundle `{"files": {"chunk_01.mp3": b64, "chunk_01.json": b64, ...}}` về máy → `ib_unbundle.py <bundle> NNN_slug/audio/clone`.
- QC từng đoạn trước khi ghép: khớp chữ với chunk ≥ 95% (chỉ chấp nhận khác biệt do số/gạch nối/chính tả Anh-Mỹ), không đọc sót/lặp, wpm 145–165, không đoạn lặng > 1,5 s ngoài thẻ break, loudness các đoạn chênh ≤ 3 LU.
- Ghép: `python3 IronBehemoth-Videos/tools/video/ib_voice_join.py IronBehemoth-Videos/NNN_slug IronBehemoth-Videos/NNN_slug/audio/clone 0.7 -15` → `audio/voice.mp3` + `audio/voice.json` (cân độ to từng đoạn, nghỉ 0.7 s giữa chương, đổi số trong transcript thành chữ để căn beat).
- Đo thời lượng: video phải 16:00–16:59 (voice + ~10 giây end card). Thiếu/thừa → chỉnh độ dài thẻ break hoặc kịch bản, **không** chỉnh tempo.
- Đổi giọng giữa chừng: sau ib_align phải dời lại offset SFX (`build/sfx.txt`), `shake` trong ib.json và chạy lại `build/edit_shotmap.py`, `build/make_music.py`.

## 3. Căn beat
`python3 IronBehemoth-Videos/tools/video/ib_align.py IronBehemoth-Videos/NNN_slug` → `build/beat_times.json`. Khớp từ phải ≥ 95%; thấp hơn → voice không khớp script, kiểm tra lại.

## 4. Cấu hình + nhạc
- `build/ib.json` từ `templates/ib.json`: `ep`, `name`, `csv`, `end_at` (beat có câu kêu gọi subscribe cuối), `tempo`, `music_ss`, `skip_ai`, `duck` (hạ nhạc ở khoảnh khắc lặng, ví dụ beat "Fire.").
- Nhạc: YouTube Studio → Thư viện âm thanh (từ khóa epic/dark cinematic/tension), tải bằng Chrome, lưu `audio/music.mp3`, ghi tên bài + tác giả vào `credits.md`. Anh có nhạc riêng thì dùng của anh.

## 5. Đồ họa `build/gfx.txt` → `ib_gfx.py`
Từ `notes.md` (bảng thông số) viết spec (mẫu `templates/gfx.txt`): `title` (INSIDE THE / TÊN XE / dòng phụ), `chapter` cho 3 câu hỏi, `ov` cho 6–12 con số lớn, `lt` (DRAMATIZATION ở cảnh dựng lại đầu video; ảnh tư liệu: tên + năm + nguồn), `card` cho con số chủ đạo (ví dụ 18). Đoạn nêu 3 câu hỏi KHÔNG dùng danh sách `q` góc trái nữa mà dùng thẻ câu hỏi giữa màn hình: `python3 IronBehemoth-Videos/tools/video/ib_qcard.py png IronBehemoth-Videos/NNN_slug/gfx/qcard "01|CÂU 1?" "02|CÂU 2?" "03|CÂU 3?"` → `gfx/qcard/q01–q03.png` + `dim.png` (số cam + vạch + câu hỏi, không có chữ QUESTION). Chữ trên màn hình tiếng Anh, viết hoa. `python3 IronBehemoth-Videos/tools/video/ib_gfx.py IronBehemoth-Videos/NNN_slug`. Thanh subscribe và end card tự tạo khi render.

## 6. Shotmap
`python3 IronBehemoth-Videos/tools/video/ib_build.py IronBehemoth-Videos/NNN_slug shotmap` → `build/shotmap.txt` (mỗi beat một shot, tự gộp beat < 1,6 giây). Sửa tay:
- Overlay `ten.png@giây@thờilượng`: `lt_drama` ở B001, `title.png@0.25@4.6` ở beat có câu "This is the <Xe>", `chapter_qN` ở beat "Question one/two/three", `ov_*` ở beat nói con số; 3 câu hỏi: `qc:q01.png@0.15@4.2`, `qc:q02.png@0.1@…`, `qc:q03.png@0.1@…` ở đúng beat đọc từng câu (mỗi lần 1 câu giữa màn hình, nền tối + thẻ phóng nhẹ, tool tự thêm whoosh).
- Thẻ toàn màn hình: `Bxxx gfx:card_18.png none`.
- Clip: `off=` bỏ đoạn đầu tối/lỗi, `speed=0.8` kéo dài clip ngắn hơn beat, `zoom=`.
- Subscribe giữa video: thêm `seq:subscribe@0.4` vào beat có chữ "subscribe"; shot đó ≥ 5,3 giây (gộp beat nếu cần). Nền là footage của chính đoạn đó, không banner; thanh giữa phía dưới; đúng 1 tiếng click + chuông (tool tự thêm).
- Dòng cuối `Bxxx_END seqv:endcard none seq:subscribe@1.0` với Bxxx = `end_at`: end card động chạy dưới câu kêu gọi cuối và giữ `endcard_tail` giây. Từ 2026-10-18 end card mặc định chồng lên clip của chính beat đó (quay chậm), không dùng nền banner (`endcard_style: banner` để quay lại kiểu cũ). Không có teaser tập chưa làm.

## 7. SFX `build/sfx.txt`
Mẫu `templates/sfx.txt`: `file  Bxxx[+/-giây]|t=giây  volume  [thời lượng]`. Bộ có sẵn ở `IronBehemoth-Videos/tools/video/common/sfx/` (mk_* Mixkit + sfx_*). Đặt tiếng ở khoảnh khắc hook (đóng nắp, bắn, nổ, sập), không quá dày. Tool tự thêm whoosh/impact cho chapter, click cho ov/lt, click + chuông cho subscribe, whoosh cho end card. Thiếu tiếng → tìm trên Mixkit (BROWSER_SNIPPETS), lưu `audio/sfx/`.

## 8. Render
- Render trong container (nhanh hơn): stage `IronBehemoth-Videos/NNN_slug` (beats/footage, audio, build, gfx, beats csv/tsv; ≤ 50 file mỗi lần stage) và `tools/video` vào container, giữ cấu trúc thư mục.
- Preview: `python3 ib_build.py <EP> render --preview --jobs 4` → `full/IBNNN_<Xe>_720p_preview.mp4`. Gửi anh duyệt (nén ≤ 30 MB nếu cần).
- Sửa: đổi dòng shotmap nào thì chỉ shot đó dựng lại (cache theo nội dung dòng). Sửa ảnh PNG overlay/thẻ mà không đổi dòng → xóa `build/_tmp/Bxxx_*` của shot đó trước khi render lại. `--test i,j` dựng thử vài shot.
- Bản cuối: `render --jobs 4` → `full/IBNNN_<Xe>_1080p.mp4`.

## 9. QC bản dựng
- Contact sheet mỗi 10 giây + xem kỹ hook, 3 chapter, các overlay số, đoạn subscribe, end card. Đoạn 3 câu hỏi phải là thẻ giữa màn hình (`qc:`), không phải danh sách góc trái. Không còn khung "MISSING", không khung đen, không ngôi sao watermark Flow (ghi `provider=flow` để tool tự xóa; clip Muse không cần).
- Loudness `ebur128`: −15 ± 1 LUFS, peak ≤ −1 dBFS. Thời lượng 16:00–16:59.

## 10. Giao file
- 1080p: cắt segment 12 giây, chép sang `IronBehemoth-Videos/NNN_slug/full/parts/` theo lô ≤ 92 MB (SendUserFile → device_commit_files), ghép trên máy trong `$HOME/work` bằng `ffmpeg -f concat -c copy -movflags +faststart` rồi chép vào `full/IBNNN_<Xe>_1080p.mp4`; bản anh duyệt cuối → `IBNNN_<Xe>_FINAL_1080p.mp4`.
- Gửi anh bản nén xem nhanh qua chat.
- `credits.md` (ảnh Wikimedia tác giả + giấy phép, footage, nhạc, "AI reconstructions", "Narration: AI voice (ai33)"); cập nhật chapters thật trong `notes.md` theo `beat_times.json`; ghi `log.md`; nhắc tick "altered or synthetic content" khi đăng.

## An toàn
Không tạo tài khoản, đăng nhập, mua hàng hay đăng ký license thay anh; chấp nhận điều khoản/Envato license cần anh đồng ý trong chat. Chỉ xóa file khi anh yêu cầu.
