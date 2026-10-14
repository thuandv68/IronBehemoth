# Quy trình: từ phân tích video mẫu đến hai skill dựng video

Phiên làm việc ngày 2026-10-10, kênh `kenh-demo`, tập thử 1010 ("Inside the King Tiger").
Mỗi bước gồm: prompt đã dùng (nguyên văn), việc Claude làm, kết quả, và bài học. Cuối mỗi bước có một
**prompt gợi ý dùng lại** đã gọn hơn cho lần sau.

API key ai33 đã được lược khỏi tài liệu này; key nằm ở `D:\YOUTUBE AI\KENH DEMO\_chung\ai33_key.txt`.

## Tổng quan

| # | Bước | Kết quả |
|---|---|---|
| 1 | Tạo vỏ não 2 | Cây thư mục `NAO YOUTUBE` theo mô hình LLM Wiki |
| 2 | Phân tích video mẫu và dựng demo | `1010_demo.mp4` (1 phút 27 giây) |
| 3 | Chọn công cụ tạo video AI | Muse bị chặn → Google Flow, Veo 3.1 Lite |
| 4 | Xử lý hết tín dụng | Đổi tài khoản Flow, tạo đủ 10 clip |
| 5 | Viết hai skill | `viet-prompt`, `dung-video` |
| 6 | Xác định ngách kênh | Giải thích kỹ thuật quân sự bằng 3D |

---

## Bước 1 — Tạo vỏ não 2

**Prompt đã dùng**

> Bạn hãy tạo vỏ thư mục não 2 theo cấu trúc của github này, lưu vào thư mục giúp tôi. Chỉ tạo vỏ, tôi sẽ nhét nội dung vào sau. Não này tôi sử dụng để xây dựng kênh youtube, sau này sẽ có các skill cho các kênh
> https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**Claude đã làm**

- Đọc gist (mô hình LLM Wiki của Karpathy: nguồn thô → wiki → schema).
- Tạo `raw/`, `wiki/`, `outputs/`, `.claude/skills/`, cùng `CLAUDE.md`, `index.md`, `log.md`.

**Kết quả**: `D:\YOUTUBE AI\NAO YOUTUBE\`

**Bài học**: gist chỉ mô tả mô hình, không quy định cây thư mục; các thư mục con (`raw/transcripts`, `wiki/channels`…) là Claude chọn cho mục đích YouTube.

**Prompt gợi ý dùng lại**

```
Tạo vỏ thư mục não 2 cho kênh YouTube theo mô hình LLM Wiki ở <link gist>. Chỉ tạo khung
(raw, wiki, outputs, .claude/skills, CLAUDE.md, index.md, log.md), chưa điền nội dung.
```

---

## Bước 2 — Phân tích video mẫu và dựng demo

**Prompt đã dùng**

> Chưa tạo skill gì. Bây giờ tôi cần bạn xem video mẫu và làm 1 video tương tự cho tôi, sử dụng ffmpeg và các thư viện opensource trên github. Nhạc nền lấy trên youtube studio, các sfx bạn tự tìm và download về. Dùng muse (tôi đã mở trên trình duyệt) để tạo video AI nếu cần. Tôi đã mở sẵn extension claude trên chorme để bạn tự remote. Nếu cần footage hoặc hình ảnh bạn tự lấy trên pexels.
> D:\YOUTUBE AI\KENH DEMO (trong này có thư mục video kênh đối thủ để bạn xem làm mẫu)
> Sau khi phân tích bạn dựng 1 video demo cho tập 1010, trong đó đã có sẵn kịch bản
> Sử dụng ai33 để đọc voice, id giọng đọc: clone_2684023
> Bên dưới là thông tin API để gọi ai333, api key: <đã lược>
> Trong quá trình làm còn thiếu gì hoặc cần gì thì bảo tôi.
> (kèm tài liệu API ai33 v3)

Bổ sung giữa chừng:

> Bạn tự làm từ đầu đến cuối, tự test video, rồi tạo video mẫu khoảng 3 phút cho tôi xem

**Claude đã làm**

1. **Phân tích video mẫu**: trích một khung hình mỗi 3 giây của 225 giây đầu, dò điểm cắt cảnh. Nhận ra cấu trúc: mở đầu điện ảnh trong rừng → bung chi tiết → "trường quay" hồ băng với vạch kích thước, nhãn số liệu, cắt lớp nội thất, bộ phận phát sáng cyan.
2. **Giọng đọc**: gọi ai33 từng câu (`POST /v3/text-to-speech`, lấy kết quả ở `GET /v1/task/{id}`), cắt khoảng lặng thừa, ghép kèm khoảng nghỉ.
3. **Nhạc nền**: vào Thư viện âm thanh YouTube Studio, tìm từ khoá "epic", tải 3 bản nhạc phim; chọn "Deified".
4. **SFX**: tab hiệu ứng của YouTube Studio không có tiếng xe tăng → tải 17 hiệu ứng từ Mixkit.
5. **Dựng**: viết script Python gọi ffmpeg — chuẩn hoá clip về 1080p 30fps, làm chậm clip ngắn, chèn chữ, trộn giọng + nhạc (tự hạ khi có lời) + SFX, chuẩn hoá -14 LUFS.
6. **Tự kiểm**: khung đen, đứng hình, độ to, bảng khung hình, nhận dạng lại lời đọc bằng faster-whisper.

**Kết quả**: `D:\YOUTUBE AI\KENH DEMO\1010\1010_demo.mp4`

**Bài học**

- `script_1010.txt` trùng nguyên văn transcript video đối thủ, có cả dòng 9 tự giới thiệu kênh đó → đã bỏ dòng 9 khỏi giọng đọc; cần viết lại kịch bản trước khi đăng.
- Pexels không có cảnh chuyên biệt ("tiger tank" ra con hổ) → chủ đề này phải dùng video AI.
- Bộ lọc thể loại của YouTube Studio khó thao tác tự động; tìm theo từ khoá nhanh hơn.

**Prompt gợi ý dùng lại**

```
Xem video mẫu trong <thư mục đối thủ>, phân tích cấu trúc hình và nhịp dựng, rồi dựng một video
demo ~<N> phút cho tập <số> theo kịch bản có sẵn. Giọng: ai33, voice <id>. Nhạc: thư viện kênh.
SFX: tự tìm trên Mixkit. Video AI: Google Flow, Veo 3.1 Lite, 8 giây, x1, tối đa <N> clip.
Tự làm từ đầu đến cuối, tự kiểm tra file, báo rõ chỗ nào chưa đạt.
```

---

## Bước 3 — Chọn công cụ tạo video AI

**Prompt đã dùng** (lần lượt)

> (trả lời câu hỏi mức dùng AI) Toàn bộ video AI vì tự vẽ mất công lắm. Vì dùng toàn video AI nên bạn có thể tạo video demo ngắn cũng đc. Cho phép tạo 15 video AI

> https://muse.ai/ Link muse đây

> Mở trên chorme ấy, tôi đăng nhập sẵn rồi. Bạn tự mở, tôi mở lại extension để bạn điều khiển rồi đấy

> Tôi đã mở flow bạn tạo video trên đó nhé. Tạo 10 video ai thôi

> Dùng model 3.1 lite, tạo 8s, x1

**Claude đã làm**

- Gửi lô 5 prompt vào Muse theo đúng mẫu lệnh bạn vẫn dùng → Muse trả lỗi `Video generation isn't available in your country or region` (HTTP 403).
- Trong lúc chờ: viết sẵn 15 prompt, viết script dựng và chạy thử bằng clip giữ chỗ.
- Chuyển sang Flow: tạo dự án, chọn Video / 16:9 / Veo 3.1 Lite / x1 (10 tín dụng một clip), gửi từng prompt.
- Rút kế hoạch từ 15 clip xuống 10 clip, demo còn 1 phút 27 giây.

**Bài học**

- Claude chỉ thấy tab nằm trong nhóm tab của Claude trên Chrome; muốn dùng trang nào thì đưa link.
- Lỗi chặn khu vực là giới hạn của dịch vụ, Claude không vượt qua; cần đổi công cụ.
- Khuôn prompt cho ra kết quả ổn: `<máy quay>, single continuous take, no cuts. <khối mô tả chủ thể lặp nguyên văn>, <hành động>, <bối cảnh>. <đuôi phong cách>, no on-screen text.`

---

## Bước 4 — Xử lý hết tín dụng Flow

**Prompt đã dùng**

> Flow của tôi vẫn còn nhiều tín dụng mà, bạn thử lại đi

> Tôi đăng nhập flow bằng tài khoản khác rồi, bạn thử lại đi

**Claude đã làm**

- Kiểm tra bảng tài khoản: tài khoản đang đăng nhập có 0 tín dụng (làm mới hằng ngày 17:44) → báo lại, không tự đổi tài khoản.
- Sau khi bạn chuyển sang tài khoản PRO: tạo dự án mới, gửi 5 clip còn lại, tải cả 10 clip về.
- Dựng bản 10 clip: thêm vạch chiều dài, chiều cao, nhãn chiều rộng và trọng lượng; thêm nền mờ sau chữ.

**Kết quả**: `1010_demo.mp4` bản 1 phút 27 giây, 1080p, -14.3 LUFS.

**Bài học**

- Veo 3.1 Lite vẽ xe tăng chỉ giống đại khái, không giữ y nguyên giữa các clip.
- Ghi "no markings" vẫn ra chữ thập; không ghi rõ mũ thì lính trong xe đội mũ sắt bộ binh.
- Mỗi clip 8 giây, câu dài hơn thì clip bị làm chậm (65–75% ở hai cảnh kíp lái).
- Tải clip từ Flow: lấy đường dẫn video ngay trong trang rồi lưu về, nhanh hơn bấm từng nút tải.

---

## Bước 5 — Viết hai skill

**Prompt đã dùng**

> Tôi cần bạn viết 2 skill để tôi áp dụng cách tạo video này cho các video kênh "kenh-demo" của tôi
>
> 1. Skill viet-prompt đầu vào là file kịch bản, đầu ra là 1 file csv có chứa các prompt để tôi đi tạo video AI. Cấu trúc file csv đầu ra như file mau.csv tôi đang để trong thư mục
> 2. Skill dung-video: đầu vào là file kịch bản => đầu ra là file hoàn chỉnh như bạn đã test ở trên
>
> Chưa rõ chỗ nào thì hỏi tôi trước khi làm nhé

Bốn quyết định bạn đã chọn khi Claude hỏi lại:

| Câu hỏi | Bạn chọn |
|---|---|
| Loại dòng trong CSV | Chỉ `veo3`, `provider = muse` |
| Ai tạo clip AI | Bạn tạo từ CSV, skill chỉ dựng |
| Chữ trên hình | Nhãn số liệu, không phụ đề |
| Nhạc và SFX | Nhạc dùng chung; SFX khác nhau theo video thì phải tuỳ biến từng tập |

**Claude đã làm**

- Đọc `file mau.csv` (209 dòng, 10 cột, mỗi câu kịch bản một beat) để lấy đúng cấu trúc.
- Viết `viet-prompt`: hướng dẫn chia beat và viết prompt + script `ghi_csv.py` kiểm tra rồi mới ghi CSV.
- Viết `dung-video`: 4 script (`b1_giong_doc.py`, `b2_dung.py`, `b3_kiem_tra.py`, `tai_sfx.py`) + hướng dẫn soạn lời đọc, nhãn, SFX.
- Tạo thư mục dùng chung `KENH DEMO\_chung\` (cấu hình, key, nhạc, SFX trung tính).
- Chạy thử trọn dây chuyền trên một tập thử dựng từ 10 clip demo, rồi xoá tập thử.
- Ghi thẻ kênh `wiki/channels/kenh-demo.md`, cập nhật `CLAUDE.md`, `index.md`, `log.md`.

**Kết quả**

```
NAO YOUTUBE\.claude\skills\
  viet-prompt\   SKILL.md, scripts\ghi_csv.py, vi-du\beats_01.json
  dung-video\    SKILL.md, scripts\{chung,b1_giong_doc,b2_dung,b3_kiem_tra,tai_sfx}.py, vi-du\*.json
```

**Bài học**

- Vạch đo bám theo thân xe trong demo là căn tay từng clip, không tự động hoá được cho hơn 200 clip → skill chỉ đặt nhãn ở dưới khung hình.
- Phần viết prompt theo SKILL.md chưa được chạy trên một kịch bản đầy đủ nào; lần chạy đầu nên soát kỹ.
- Một tập 30 phút cần khoảng 250 clip, tức khoảng 2.500 tín dụng Veo 3.1 Lite.

**Prompt gợi ý dùng lại** (đóng gói một quy trình khác thành skill)

```
Viết skill <tên> cho kênh <slug>: đầu vào <…>, đầu ra <…>, theo đúng cách đã làm ở tập <số>.
File mẫu đầu ra: <đường dẫn>. Chưa rõ chỗ nào thì hỏi tôi trước khi viết. Viết xong chạy thử
trên dữ liệu thật và báo phần nào chưa được kiểm.
```

---

## Bước 6 — Xác định ngách kênh

**Prompt đã dùng**

> Kênh này là ngách gì nhỉ

**Trả lời**: giải thích kỹ thuật quân sự bằng hoạt hình 3D — mỗi tập "mổ xẻ" một cỗ máy (kích thước, kíp lái, vũ khí, giáp, động cơ, truyền động, đánh giá thực chiến). Khán giả mê lịch sử quân sự, kỹ thuật, mô hình, game; rất khắt khe về độ chính xác.

**Còn bỏ ngỏ**: kênh đi hướng quân sự thuần hay "cỗ máy khổng lồ" nói chung (file mẫu CSV là tàu ngầm Typhoon, tiếng Tây Ban Nha). Nhận định này mới dựa trên một video mẫu và một kịch bản.

---

## Cách chạy cho tập tiếp theo

1. Tạo `D:\YOUTUBE AI\KENH DEMO\<tên tập>\` và đặt `script_<tên tập>.txt` vào.
2. Mở phiên Claude trong thư mục `NAO YOUTUBE`, gõ:

```
/viet-prompt <tên tập>
```

3. Đem `prompts_<tên tập>.csv` đi tạo clip (Veo 3.1 Lite, 8 giây, 16:9), lưu vào `footage\` với tên `<asset_id>.mp4`.
4. Gõ:

```
/dung-video <tên tập>
```

5. Nghe thử file `<tên tập>_final.mp4`: Claude kiểm được hình, độ to và lời đọc bằng máy, nhưng không nghe được nhạc và SFX có hợp không.

## Việc còn tồn

- Viết lại kịch bản 1010 (đang trùng nguyên văn video đối thủ).
- Chốt định vị ngách rồi ghi vào thẻ kênh.
- Chạy `viet-prompt` lần đầu trên một kịch bản đầy đủ và soát chất lượng prompt.
- `1010\work\prompts_muse.md` vẫn là bản 15 clip viết cho Muse, đã lỗi thời.
- Cân nhắc chuyển API key ai33 sang biến môi trường `AI33_KEY` nếu máy có người khác dùng.
