# Gói skill `long-tieng` — lồng tiếng video YouTube đa ngôn ngữ (Claude Code)

> **Gửi Claude đang đọc file này:** người dùng muốn bạn dựng lại **nguyên vẹn** một skill Claude Code tên
> `long-tieng` từ file này. Hãy làm đúng mục **A. Cách dựng skill** ngay bên dưới. Mọi file cần tạo nằm ở mục
> **C**, mỗi file nằm trong một khối code có ghi đường dẫn ngay phía trên. **Chép nguyên văn từng byte** — không
> sửa, không rút gọn, không "cải tiến" code. Các con số, ngưỡng và luật đều đã được chủ skill gốc nghe thử và chốt
> qua nhiều tập thật; đổi một chỗ là skill chạy khác bản gốc.

---

## A. Cách dựng skill — việc của Claude

1. Hỏi người dùng **thư mục dự án** sẽ chứa skill (thư mục họ mở Claude Code). Skill nằm ở
   `<dự án>/.claude/skills/long-tieng/`. Claude Code chỉ nạp skill ở đúng cấp này — không lồng thêm thư mục.
2. Tạo **đúng 10 file** ở mục C, đường dẫn tương đối tính từ `<dự án>/.claude/skills/long-tieng/`:

   ```
   .claude/skills/long-tieng/
   ├── SKILL.md            quy trình (Claude đọc khi user gọi skill)
   ├── quy-tac.md          thông số + luật dịch/co giãn (frontmatter là cấu hình mà script đọc)
   ├── so-do.md            sổ tốc độ đọc theo ngôn ngữ + số đo theo tập (script tự ghi)
   └── scripts/
       ├── ai33.py         client API TTS ai33
       ├── tron_am.py      công thức trộn giọng + nhạc + SFX
       ├── lt_lib.py       thư viện chung
       ├── lt_01_chia_khoi.py
       ├── lt_02_kiem_dich.py
       ├── lt_03_doc_khop.py
       └── lt_04_tron.py
   ```

   Ghi file bằng UTF-8, xuống dòng LF. `quy-tac.md` phải bắt đầu đúng bằng dòng `---` (không BOM, không dòng
   trống phía trên) vì script đọc frontmatter của nó.
3. Kiểm môi trường (mục B) và báo người dùng thiếu gì.
4. Hỏi người dùng **`voice_id`** giọng của họ trên ai33 rồi điền vào frontmatter `quy-tac.md` (khoá `voice_id`).
   Đây là **chỗ duy nhất bắt buộc phải điền**. Các khoá khác chỉ đổi khi người dùng yêu cầu.
5. Chạy thử biên dịch: `python -m py_compile scripts/*.py` trong thư mục skill → phải im lặng.
6. Báo người dùng: skill đã sẵn sàng, gọi bằng `/long-tieng <thư mục tập>` hoặc nói "lồng tiếng tập này".

---

## B. Môi trường cần có — người dùng chuẩn bị

| Thứ | Yêu cầu | Kiểm bằng |
|---|---|---|
| Python | 3.10 trở lên, cài `numpy` và `requests` | `python -c "import numpy, requests"` |
| ffmpeg | bản có `libmp3lame`, `loudnorm`, `sidechaincompress`, `ebur128`, `atempo` (bản full build thông thường đều có). Nằm trong PATH, hoặc đặt biến môi trường `FFMPEG` trỏ tới `ffmpeg.exe` | `ffmpeg -hide_banner -filters \| findstr sidechaincompress` |
| Tài khoản ai33 | có credit, có một giọng (clone hoặc thư viện) dùng làm giọng kênh. Ước tính ~30.000 credit mỗi ngôn ngữ cho một video 20 phút | — |
| API key ai33 | **không bao giờ để trong thư mục dự án.** Đặt biến môi trường `AI33_API_KEY`, hoặc tạo file `~/.secrets/tts.env` (đổi chỗ bằng biến `TTS_SECRETS`) chứa một dòng `AI33_API_KEY=...` | — |
| YouTube | kênh có quyền Advanced features (mới upload được track âm thanh đa ngôn ngữ) | Studio |

### Thư mục một tập video — đầu vào skill

Mỗi tập là một thư mục, tên thư mục chính là "tên tập" (ví dụ `0928_ing`). Skill cần:

```
<thư mục tập>/
├── script_<tên tập>.txt      kịch bản gốc — đúng MỘT file script_*.txt
├── voice/
│   ├── <tên tập>.mp3         voice gốc (ngôn ngữ gốc của video)
│   └── <tên tập>.srt         SRT của voice gốc, mốc thời gian theo từng câu/cụm (ai33 xuất kèm khi bật with_transcript)
└── _tmp_skill/               (giai đoạn B) nền âm — xem quy-tac.md §3
    ├── <tên tập>_nhac.flac + <tên tập>_sfx.flac     cách 1: nhạc chưa duck + SFX, dài đúng bằng video
    └── <tên tập>_nen.flac                           cách 2: nền đã trộn sẵn (không có giọng), dài đúng bằng video
```

File kịch bản có ba khối, mỗi khối mở bằng nhãn ở đầu dòng:

```
TITLE: <tiêu đề video>
DESCRIPTION:
<đoạn mô tả 1>

<đoạn mô tả 2>

00:00 <nhãn chương 1>
03:12 <nhãn chương 2>
...
SCRIPT:
<lời đọc chương 1>
<#1#>
<lời đọc chương 2>
<#1#>
...
```

- Trong khối `SCRIPT:` **chỉ** dùng marker `<#1#>` (nghỉ 1 giây của ai33) để ngăn **chương**. Số marker phải bằng
  số khoảng nghỉ ≥ 0,8 s trong SRT, nếu không bước 1 dừng. Các chỗ nghỉ khác trong voice phải ngắn hơn 0,8 s.
- Số trong lời đọc viết bằng chữ (TTS đọc chữ).
- `voice/<tên tập>.srt` phải sinh từ đúng chữ trong khối `SCRIPT:` hiện tại (bước 1 dừng nếu khớp chữ < 90 %).

---

## C. Nội dung 10 file

Mỗi file: dòng `### FILE: <đường dẫn>` rồi một khối code. Chép phần **bên trong** khối code (không chép dòng
rào ``` ở đầu và cuối).

### FILE: `SKILL.md`

`````markdown
---
name: long-tieng
description: Lồng tiếng một tập video sang nhiều ngôn ngữ để upload làm track âm thanh đa ngôn ngữ trên YouTube (không dùng auto-dub). Mặc định 8 ngôn ngữ (Anh, Bồ Đào Nha BR, Indonesia, Ả Rập, Nhật, Pháp, Đức, Việt). Chia kịch bản thành khối nghĩa 15–25 giây theo SRT gốc, mỗi ngôn ngữ một agent dịch song song, đọc ai33 bằng giọng của kênh, khớp từng khối về đúng khung giờ gốc bằng atempo với một tốc độ chung cho cả chương, lệch ≤ 5% giữ giọng thô (khối vượt ngưỡng thì agent tự viết lại và đọc lại riêng khối đó), rồi trộn với nhạc + SFX gốc, ra mp3 320 kbps dài bằng video, kèm phụ đề SRT, tiêu đề và mô tả đã dịch. Dùng khi user nói "lồng tiếng", "dub", "làm bản lồng tiếng", "làm track âm thanh đa ngôn ngữ", hoặc gửi thư mục tập kèm ý muốn lồng tiếng.
---

# Skill: lồng tiếng

**Vai trò:** bạn là chuyên gia bản địa hoá video tài liệu trên mười năm kinh nghiệm — dịch cho tai nghe, không cho
mắt đọc, và biết một bản lồng tiếng tệ làm hỏng cả video tốt.

`<SK>` dưới đây = thư mục chứa file này (`.claude/skills/long-tieng`), dùng **đường dẫn tuyệt đối**.
Script nằm ở `<SK>/scripts/`, chạy **từ chính thư mục đó**, đặt `PYTHONIOENCODING=utf-8`.

## 0. Ba bước mở đầu — làm trước mọi thứ

1. Xác định **thư mục tập** `<V>`: user gửi đường dẫn. Không có → hỏi user, không đoán.
2. **Đọc trọn `<SK>/quy-tac.md`.** Ngôn ngữ, ngưỡng co giãn, tên file, luật dịch nằm ở đó, không nằm ở đây.
3. Kiểm `voice_id` trong frontmatter `quy-tac.md` đã điền chưa. Chưa → dừng, hỏi user.

### Vì sao làm như thế này (để không "tối ưu" sai)

- **Track tự upload thay TOÀN BỘ âm thanh** khi người xem chọn ngôn ngữ đó. YouTube không tự trộn nền gốc vào. Vì
  vậy file upload phải là **bản trộn hoàn chỉnh**: giọng mới + nhạc + SFX gốc. Upload chỉ giọng thì người xem
  không nghe nhạc.
- **Khớp theo khối nghĩa, không theo câu, không theo cả bài:** hình, overlay chữ và SFX bám mốc của bản gốc. Mỗi
  khối giữ đúng khung giờ gốc nên lời mới vẫn rơi đúng hình, mà trong khối thì người dịch được tự do sắp câu.
- **Không cần hiệu chuẩn giọng trước:** đọc xong mới đo rồi co giãn; khối lệch quá xa thì viết lại chữ, không
  kéo giọng méo.

## 1. Hai giai đoạn

| Giai đoạn | Bước | Cần | Chạy được khi |
|---|---|---|---|
| **A** — dịch, đọc, khớp | 1 → 3 | `script_*.txt` (gồm khối `TITLE:` + `DESCRIPTION:`) · `voice/<tên V>.srt` | ngay sau khi có voice gốc |
| **B** — trộn, xuất | 4 | nền âm: `_nhac.flac` + `_sfx.flac` → hoặc `_nen.*` (quy tắc §3) | khi đã có file nền |

User gọi skill khi chưa có nền âm → chạy A, báo user B đang chờ nền âm. Gọi lại sau → bước 3 thấy mọi khối đã khớp
thì không đọc lại, đi thẳng bước 4.

## 1b. ⭐ Báo tiến độ cho user — mỗi ~2 phút

Lượt lồng tiếng chạy lâu (dịch, đọc ai33, khớp, trộn). User phải luôn biết agent nào đang làm gì, tới đâu, và máy
**không bị treo**:

- **Mỗi ~2 phút một dòng ngắn** trong chat: bước nào · agent / ngôn ngữ nào · làm tới đâu (khối, task, %) · việc kế tiếp.
- **Bước máy chạy nền** (`lt_03` chờ ai33, `lt_04` trộn): chạy bằng `run_in_background`, rồi đọc file output đều đặn
  (`lt_03` in dòng `[m:ss] … task xong · đang chờ: c2 45%, …` mỗi 60 s) và báo lại con số đó. Không im lặng chờ
  thông báo xong.
- **Agent con theo ngôn ngữ:** khi gửi, ghi rõ danh sách agent đang chạy; mỗi lần một agent báo xong hoặc lỗi thì báo
  ngay; giữa chừng báo theo output nền của các lệnh `lt_03` mà agent đó chạy.
- Dòng báo phải có số thật đọc từ output, không ước đoán.

## 2. Bước 1 — Chia khối *(agent chính, một lần cho mọi ngôn ngữ)*

```bash
cd "<SK>/scripts" && PYTHONIOENCODING=utf-8 python lt_01_chia_khoi.py "<V>"
```

- Ra `<V>/_tmp_skill/long-tieng/khoi.json` + `khoi_goc.txt` (bản ngôn ngữ gốc theo khối) +
  `nguon_tieu_de_mo_ta.txt`.
- Script tự dừng khi số chương trong SRT khác số marker, hoặc khớp chữ SRT ↔ kịch bản dưới 90 %.
- Kịch bản chưa có khối `DESCRIPTION:` → script cảnh báo. Hỏi user có muốn thêm mô tả gốc trước không. Không có mô
  tả thì bản dịch chỉ có tiêu đề.
- ⛔ `khoi.json` đã có thì script dừng: các bản dịch đang bám theo nó. Chỉ `--ghi-de` khi làm lại từ đầu.

Mốc tham chiếu (bản gốc, tập 20 phút): 89 khối nhỏ → gộp còn ~69 khối, 8 chương, khớp chữ 99,7 %, trung vị ~17 s.

## 3. Bước 2–3 — Mỗi ngôn ngữ một agent, chạy song song

Agent chính gửi **một lời gọi `Agent` cho mỗi ngôn ngữ (hiện 8), trong cùng một tin nhắn** (chạy nền), mỗi lời gọi
một ngôn ngữ trong khoá `ngon_ngu` của `quy-tac.md`. Prompt cho từng agent (thay `<…>`):

```
Bạn dịch và lồng tiếng tập <tên V> sang <tên hiển thị> (<mã>), tên file `<ngôn ngữ>`.
Thư mục tập: <V>. Thư mục skill: <SK>.

1. Đọc trọn <SK>/quy-tac.md (§5 luật dịch, §6 co giãn, §7 tiêu đề + mô tả).
2. Đọc <V>/_tmp_skill/long-tieng/khoi_goc.txt và nguon_tieu_de_mo_ta.txt.
3. Viết <V>/_tmp_skill/long-tieng/<ngôn ngữ>/<tên V>_<ngôn ngữ>.txt: giữ NGUYÊN mọi dòng `### Kxxx | …`, thay đoạn
   ngôn ngữ gốc dưới mỗi dòng bằng bản dịch. Số viết bằng chữ.
4. Viết <V>/voice/long_tieng/<tên V>_<ngôn ngữ>_tieu_de_mo_ta.txt theo bố cục §7.
5. Chạy `python lt_02_kiem_dich.py "<V>" --ngon-ngu <ngôn ngữ>` (trong <SK>/scripts/, PYTHONIOENCODING=utf-8) tới
   khi 0 vi phạm. Có dòng CANH BAO "dự báo … viết DÀI thêm / NGẮN lại khoảng N ký tự" (chấm đúng luật khớp của
   lt_03, từ sổ tốc độ đọc): viết lại khối đó cho gần N ký tự, giữ nghĩa, rồi chạy lại tới khi hết CANH BAO — sửa
   chữ lúc này không tốn credit, đọc lại sau mới tốn.
6. Chạy `python lt_03_doc_khop.py "<V>" --ngon-ngu <ngôn ngữ>` CHẠY NỀN, chờ thông báo xong. Có dòng VUOT: viết lại
   đúng các khối đó theo hướng script gợi ý (dài thêm / ngắn lại), giữ nghĩa, chạy lại lt_02 rồi lt_03 — script chỉ
   đọc lại khối đã sửa. Lặp tới khi thoát 0. Dòng LOI (task ai33 lỗi, không tách được khối): dừng, báo nguyên văn.
7. Không sửa file nào khác. Không đọc file của ngôn ngữ khác.
Báo cáo: số khối · tỉ lệ lời/khung thấp nhất–cao nhất · số khối đã viết lại (liệt kê) · credit = số "cộng dồn" ở
dòng `CREDIT:` cuối cùng lt_03 in ra. ⛔ Không tính credit bằng hiệu số dư tài khoản: các agent khác dùng chung tài
khoản ai33 cùng lúc.
```

Luật cho agent chính khi điều phối:

- **Đồng thời ai33:** bản gốc đã chạy 7 agent cùng lúc (~56 task) không lỗi. Nếu có agent báo task lỗi kiểu quá tải
  hoặc giới hạn tốc độ, chạy lại ngôn ngữ đó sau khi các agent khác xong, rồi ghi con số giới hạn vào `so-do.md`.
- Credit ước tính khoảng 30.000 mỗi ngôn ngữ cho tập 20 phút, cộng một ít cho các khối đọc lại. Kiểm credit trước
  khi gửi các agent: không đủ cho tất cả → báo user, không chạy nửa chừng.
- Agent nào FAIL → các agent khác vẫn chạy tiếp. Báo user ngôn ngữ nào lỗi, không tự chạy lại quá một lần.

Mốc tham chiếu (bản gốc, thử 4 khối mở bài tiếng Anh): lần đầu 3/4 khối đạt, một khối đọc ngắn 17 % → viết dài
thêm → đọc lại riêng khối đó 204 credit → 4/4 đạt, tỉ lệ 0,88–0,96.

## 4. Bước 4 — Trộn và xuất *(agent chính)*

```bash
cd "<SK>/scripts" && PYTHONIOENCODING=utf-8 python lt_04_tron.py "<V>" --tat-ca
```

- Script dừng nếu ngôn ngữ nào còn khối chưa đạt. Nền âm chọn theo thứ tự ở quy tắc §3, dòng đầu output ghi đang
  dùng nền nào. Không có nền → script dừng: báo user đặt file nền vào `<V>/_tmp_skill/`.
- Trộn bằng `loc_tron_am()` trong `tron_am.py` — đúng công thức trộn của bản gốc. In thời lượng so với video và
  LUFS. Lệch video quá 0,1 s → cảnh báo, không giao file đó.
- Phụ đề: mỗi câu một cue. Câu > 84 ký tự cắt **theo nghĩa** ở dấu `, ; :` muộn nhất còn vừa cue (vế chêm khép
  trọn); không có dấu thì để nguyên tới 130 ký tự; quá nữa mới cắt ở khoảng trắng — ưu tiên trước liên từ, không
  treo từ nối cuối cue — và script in danh sách `⚠️ … phải cắt ở khoảng trắng` để **báo user** xem lại. Xuống dòng
  trong cue chỉ ở dấu câu, còn lại để YouTube tự xuống dòng. Mốc mỗi cue hút về khoảng lặng thật trong giọng đã
  khớp. Chỉ làm lại phụ đề (không trộn lại, không tốn credit): `lt_04_tron.py "<V>" --ngon-ngu <nn> --chi-srt`.

## 5. Dọn và bàn giao

⛔ **Ghi số đo (cuối mục này) TRƯỚC khi dọn:** credit mỗi ngôn ngữ nằm ở
`<V>/_tmp_skill/long-tieng/<ngôn ngữ>/credit.json` (khoá `tong`, `lt_03` cộng dồn mọi lượt đọc, kể cả lượt của phiên
bị ngắt) — dọn rồi là mất.

Bước 4 xong cho **mọi** ngôn ngữ → xoá `<V>/_tmp_skill/long-tieng/` (không hỏi). Mọi thứ cần giữ đã nằm ở
`<V>/voice/long_tieng/` (mp3, srt, tiêu đề + mô tả; bản dịch theo khối là file tạm, xoá theo). `_tmp_skill/` rỗng
sau đó thì xoá luôn — nhưng **không xoá file nền âm** của user. Giai đoạn B còn chờ → **giữ nguyên** thư mục tạm:
giọng đã khớp trong đó tốn credit mới có.

**Sổ tốc độ đọc — script tự ghi:** lần đọc đầu (≥ 50% số khối) của mỗi ngôn ngữ trong mỗi tập, `lt_03` tự thêm một
dòng vào mục "Sổ tốc độ đọc theo ngôn ngữ" của `<SK>/so-do.md` (ký tự/giây lời, lời/khung trung vị). Lần sau `lt_02`
lấy trung vị các dòng đó để dự báo từng khối trước khi đọc. ⛔ Không sửa tay số trong sổ.

**Ghi số đo — tự ghi, không hỏi:** thêm một dòng vào bảng "Số đo theo tập" của `<SK>/so-do.md` cho mỗi ngôn ngữ —
số khối, tỉ lệ thấp nhất–cao nhất, số khối viết lại, credit (`credit.json` → `tong`).

**Báo cáo cuối:**

```
Tap <tên V> · <số khối> khoi · <số chương> chuong
Ngon ngu        Khoi dat   Ti le       Viet lai   Credit    File
tieng_anh       69/69      0.86–1.10   3          31.204    <tên V>_tieng_anh.mp3 (20:38, -14.0 LUFS)
…
Cho giai doan B: <danh sách> (thiếu nền âm)   ·   Loi: <danh sách hoặc "không">
Upload: quy-tac.md §8
```
`````

### FILE: `quy-tac.md`

`````markdown
---
title: Quy tắc lồng tiếng
skill: long-tieng
# --- Thông số — script long-tieng/scripts/ đọc đúng các dòng này, giữ dạng "khoá: giá trị" ---
# ngon_ngu: <tên file>=<mã ngôn ngữ>=<tên hiển thị>, ngăn bằng dấu chấm phẩy.
ngon_ngu: tieng_anh=en=Inglés;tieng_bo_dao_nha_br=pt-BR=Portugués (Brasil);tieng_indonesia=id=Indonesio;tieng_a_rap=ar=Árabe;tieng_nhat=ja=Japonés;tieng_phap=fr=Francés;tieng_duc=de=Alemán;tieng_viet=vi=Vietnamita
# ngon_ngu_thu: ngôn ngữ chỉ để nghe thử (script nhận, nhưng KHÔNG chạy trong lượt chính), cùng dạng với ngon_ngu.
ngon_ngu_thu:
# --- giọng đọc ai33 (dùng cho mọi ngôn ngữ) ---
tts_provider: ai33
# voice_id: ĐIỀN id giọng của bạn trên ai33 (ví dụ clone_1234567). Để nguyên <...> thì script dừng.
voice_id: <ĐIỀN_VOICE_ID>
speed: 1.0
pronunciation_dictionary_id:
# --- tiêu đề + mô tả: số lần cụm từ khoá chính phải lặp trong phần văn mô tả (§7). 0 = không kiểm luật từ khoá.
so_lan_tu_khoa: 5
# --- chia khối ---
khoi_toi_da_giay: 20
# gộp khối đọc: gom khối liền nhau trong chương tới ≥ khoi_muc_tieu_giay, không vượt khoi_tran_giay; khối < khoi_toi_thieu_giay gộp nốt
khoi_muc_tieu_giay: 15
khoi_tran_giay: 25
khoi_toi_thieu_giay: 8
nghi_that_giay: 0.2
nguong_khe_marker: 0.8
# --- co giãn ---
nen_toi_da: 0.12
gian_toi_da: 0.30
marker_tach_khoi: <#2#>
bitrate_ra: 320k
# co_gian: bộ lọc ffmpeg kéo giọng về khung, {tl} = tempo. Đổi khoá này → bước 3 tự khớp lại mọi khối, không đọc lại voice.
co_gian: atempo={tl}
# khong_co_gian: lời ngắn hơn khung không quá tỉ lệ này thì giữ giọng thô, chỉ để lặng cuối khối.
khong_co_gian: 0.05
# nghi_cuoi_khoi: giây lặng chừa ở cuối mỗi khối — giọng chỉ khớp vào (khung − nghi_cuoi_khoi), để có nhịp nghỉ giữa hai khối như giọng thật.
nghi_cuoi_khoi: 0.4
# du_lang_toi_da: lặng dư sau lời (đã đọc ở tốc độ chương) quá tỉ lệ này của khung lời → khối phải viết dài thêm.
du_lang_toi_da: 0.15
# bien_du_bao: lt_02 thu hẹp vùng đạt hai đầu đi chừng này khi dự báo, vì tốc độ đọc thật dao động theo khối (tiếng Nhật đọc chậm hơn sổ ~4%).
bien_du_bao: 0.04
---

# Quy tắc lồng tiếng

> **Nguồn sự thật cho skill `long-tieng`.** Script đọc frontmatter phía trên; agent dịch đọc §5–§7. Sửa thông số ở
> đây là đổi cho mọi tập sau.

## 1. Ngôn ngữ — 8 thứ tiếng

| Ngôn ngữ | Tên trong file | Mã |
|---|---|---|
| Anh | `tieng_anh` | `en` |
| Bồ Đào Nha (Brazil) | `tieng_bo_dao_nha_br` | `pt-BR` |
| Indonesia | `tieng_indonesia` | `id` |
| Ả Rập | `tieng_a_rap` | `ar` |
| Nhật | `tieng_nhat` | `ja` |
| Pháp | `tieng_phap` | `fr` |
| Đức | `tieng_duc` | `de` |
| Việt | `tieng_viet` | `vi` |

Thêm / bớt ngôn ngữ: sửa khoá `ngon_ngu` ở frontmatter (giữ dạng `tên_file=mã=tên hiển thị`, tên file viết
`tieng_<...>`). Ngôn ngữ trùng với ngôn ngữ gốc của video thì bỏ ra.

## 2. Giọng và trộn âm — y hệt bản gốc

- **Giọng:** một giọng ai33 cho mọi ngôn ngữ (`voice_id`, `speed` ở frontmatter), tắt xuất SRT khi lồng tiếng. Giọng
  nên là giọng của chính video gốc (clone) để người xem đổi track vẫn nghe cùng một người kể. ⛔ Không đổi giọng
  riêng cho một ngôn ngữ khi chưa hỏi user.
- **Trộn âm:** gọi đúng hàm `loc_tron_am()` trong `scripts/tron_am.py` — nhạc sidechain (duck) theo **giọng mới**
  như bản gốc duck theo giọng gốc, cộng SFX, loudnorm về −14 LUFS. Không chép công thức sang chỗ khác.

## 3. Đầu vào · đầu ra

**Vào** (thư mục tập `<V>`):

| File | Dùng ở giai đoạn |
|---|---|
| `script_<tên V>.txt` | A — nguồn chữ để dịch (khối `SCRIPT:`), tiêu đề (`TITLE:`) và mô tả (`DESCRIPTION:`) |
| `voice/<tên V>.srt` | A — chia khối, khung giờ gốc |
| Nền âm — **một trong hai**, xét theo thứ tự, mọi file nằm **ngoài cùng `<V>/_tmp_skill/`** | B — dài file nền = dài video |
| ① `_tmp_skill/<tên V>_nhac.flac` + `_sfx.flac` | nhạc **chưa duck** + SFX, xuất riêng từ phần mềm dựng → skill duck nhạc theo giọng mới, cộng SFX. **Cách chuẩn** |
| ② `_tmp_skill/<tên V>_nen.<flac/wav/mp3/m4a>` | nền đã trộn sẵn, không có giọng (SFX lẫn nhạc đã duck theo giọng gốc — ví dụ xuất từ phần mềm dựng với track giọng tắt, hoặc tách giọng khỏi video đã dựng). Dùng nguyên làm nền: không duck lại, không ghép thêm nhạc. Nhạc võng theo nhịp giọng gốc — vẫn khớp phần lớn vì các khối cùng mốc |

**Ra** (`<V>/voice/long_tieng/`), mỗi ngôn ngữ:

| File | Là gì |
|---|---|
| `<tên V>_<ngôn ngữ>.mp3` | **file upload**: giọng + nhạc + SFX, mp3 320 kbps, dài đúng bằng video |
| `<tên V>_<ngôn ngữ>.srt` | phụ đề ngôn ngữ đó, cắt theo nghĩa (dấu câu), mốc bám khoảng lặng của giọng |
| `<tên V>_<ngôn ngữ>_tieu_de_mo_ta.txt` | tiêu đề + mô tả đã dịch, mốc chương giữ nguyên |

Ví dụ: `0928_ing_tieng_anh.mp3`.

Bản dịch theo khối (chữ TTS đọc) là file **làm việc** của skill, không giao user: nằm ở
`_tmp_skill/long-tieng/<ngôn ngữ>/<tên V>_<ngôn ngữ>.txt` và bị xoá cùng thư mục tạm khi mọi ngôn ngữ xong bước 4.

## 4. Chia khối

- Đơn vị nhỏ nhất là **câu**: nối cue SRT tới khi gặp `. ? !`. Không bao giờ cắt đôi một câu.
- Cắt ở khoảng nghỉ thật ≥ `nghi_that_giay`. Khoảng nghỉ ≥ `nguong_khe_marker` (marker chương) luôn là ranh giới.
- Khối dài hơn `khoi_toi_da_giay` thì chia đôi ở ranh giới câu gần giữa nhất, lặp lại tới khi vừa.
- **Gộp khối đọc:** mỗi khối là **một lượt đọc rời** của TTS, nhiều khối ngắn → nhiều chỗ ngữ điệu bắt đầu lại →
  nghe rời rạc (bản đầu: 101 khối, 19 khối < 8 s). Gom khối liền nhau **trong cùng chương** tới
  ≥ `khoi_muc_tieu_giay` (15 s), không vượt `khoi_tran_giay` (25 s); khối còn < `khoi_toi_thieu_giay` (8 s) gộp nốt
  vào khối kề. Kết quả: 69 khối, trung vị 17,4 s, ngắn nhất 10,9 s.
- Khung của khối = từ đầu cue đầu tiên tới cuối cue cuối cùng. Bản lồng tiếng của khối phải nằm khít trong khung đó.

## 5. Dịch — luật cho agent dịch

1. **Dịch từ chữ của kịch bản**, không từ chữ SRT (SRT đã bị TTS chuẩn hoá lại).
2. **Mỗi khối dịch liền mạch.** Được sắp lại câu, gộp hay tách câu cho tự nhiên với ngôn ngữ đích. Không được chuyển ý
   sang khối khác: lời và hình chỉ khớp khi ý nằm đúng khối.
3. **Giữ độ dài tương đương bản gốc.** Không thêm ý, không giảng giải. Câu ngắn của bản gốc giữ ngắn.
4. **Số viết bằng chữ** như kịch bản gốc, vì TTS đọc chữ. Cổng chặn mọi chữ số `0-9` và `٠-٩`.
5. **Tên riêng** (tên tàu, tên dự án, địa danh) giữ dạng quen thuộc ở ngôn ngữ đích. Viết tắt đã phiên âm trong bản
   gốc thì phiên âm lại theo cách đọc của ngôn ngữ đích.
6. **Giọng kể phim tài liệu**, ngôi hai thân mật nếu ngôn ngữ đích cho phép. Tiếng Nhật dùng thể lịch sự (です/ます).
   Tiếng Ả Rập dùng tiếng Ả Rập chuẩn (MSA). Tiếng Bồ Đào Nha theo cách nói Brazil.
7. **CTA** (đăng ký, like, comment) dịch theo cách creator bản xứ vẫn nói, không dịch từng chữ.

## 6. Co giãn

Đo lời thật của từng khối rồi giãn hoặc nén bằng bộ lọc ở khoá `co_gian` cho vừa khung. Hiện dùng **`atempo`**. Bản
thử dùng `rubberband` mặc định thì nghe **vang và rè**:
- **Rè:** giọng ai33 có đỉnh 1,19–1,34, file trung gian ghi 16-bit nên bị cắt cụt. Đã sửa: file trung gian ghi float.
- **Vang:** do `rubberband` bản R2 trong ffmpeg (không có engine R3). Nghe so 4 bản: giọng thô chưa co giãn chuẩn
  nhất (chỉ là mốc so, không khớp khung), **`atempo` tạm được → chọn**, `rubberband` mặc định và `rubberband` chỉnh
  cho giọng nói đều **loại**.

**Nhịp nghỉ giữa hai khối:** bản đầu khớp giọng kín tới cuối khung, khối sau vào ngay → nghe vội. Nay mỗi khối
**chừa `nghi_cuoi_khoi` (0,4 s) lặng ở cuối**: "khung" trong bảng dưới là khung khối trừ khoảng này (khối ngắn hơn hai
lần khoảng nghỉ thì chừa 20% khung).

**Một tốc độ cho cả chương:** bản đầu co giãn mỗi khối một tốc độ (giữ nguyên tới chậm 28%) → nghe giật nhịp. Nay
tốc độ chương = trung vị lời/khung-lời các khối trong chương (kẹp trong ngưỡng). Khối ngắn hơn đọc đúng tốc độ chương
rồi để lặng; khối dài hơn nén riêng vừa đủ. Lặng dư sau lời quá `du_lang_toi_da` (15%) khung lời → khối phải viết dài
thêm. Khoảng nghỉ `nghi_cuoi_khoi` **giữ nguyên** — khối vẫn là lượt đọc rời, bỏ nghỉ thì hai lượt dính tù tì.

| Tỷ lệ lời / khung | Xử lý |
|---|---|
| Lời ngắn hơn khung tới `khong_co_gian` (5%) | **giữ giọng thô**, không co giãn, để lặng ở cuối khối (khối 20 s dư tối đa ~1 s) |
| Lời ngắn hơn khung từ 5% tới `gian_toi_da` (30%) | giãn chậm, đạt. Nới từ 15% lên 30%: giọng tiếng Việt đọc nhanh hơn khung gốc ~17% gần như ở mọi khối (trung vị lời/khung 0,82, chỉ 40/101 khối đạt ở ngưỡng 15%) |
| Lời dài hơn khung tới `nen_toi_da` (12%) | nén nhanh, đạt |
| Ngoài hai ngưỡng trên | **agent tự viết lại khối đó** (dài hơn hoặc ngắn hơn) rồi đọc lại riêng khối đó. Không hỏi user |

**Dự báo trước khi đọc:** mỗi ngôn ngữ đọc nhanh chậm khác nhau — tiếng Việt nhanh hơn khung gốc ~17% ở lần đầu. Sau
mỗi lần đọc đầu, `lt_03` tự ghi tốc độ (ký tự/giây lời) vào sổ trong `so-do.md`; `lt_02` dùng trung vị sổ để báo khối
nào sẽ lệch và nên viết bao nhiêu ký tự. Dự báo chấm **đúng luật lúc khớp thật**: tính tốc độ chương từ các khối dự
báo, khối đạt khi lời/khung nằm trong `tốc độ chương × (1 − du_lang_toi_da)` … `1 + nen_toi_da`, thu hẹp mỗi đầu
`bien_du_bao`; số ký tự gợi ý nhắm giữa vùng đó.

Ngưỡng nén chặt hơn ngưỡng giãn, vì giọng nói nhanh lên dễ lộ hơn giọng chậm lại.

## 7. Tiêu đề và mô tả

- **Tiêu đề:** dịch từ dòng `TITLE:` của kịch bản. Giữ khuôn tiêu đề của bản gốc (cấu trúc, cụm từ khoá chính).
- **Mô tả:** dịch từ khối `DESCRIPTION:` của file kịch bản. Thiếu khối → chỉ dịch tiêu đề, báo user. **Mốc
  timestamp giữ nguyên tuyệt đối**, chỉ dịch nhãn. Số đoạn giữ nguyên.
- **Từ khoá** (khi `so_lan_tu_khoa` > 0): cụm từ khoá chính của mô tả gốc (cụm lặp nhiều lần, mở đầu nhãn dòng
  `00:00`) dịch thành **một cụm cố định** của ngôn ngữ đích, ghi ở dòng `TU_KHOA:`. Cụm đó phải xuất hiện **đúng
  `so_lan_tu_khoa` lần** trong phần văn (không tính dòng mốc), và nhãn dòng `00:00` mở đầu bằng cụm đó, như bản gốc.
  Với tiếng Nhật, chuỗi được so trực tiếp, không cần khoảng trắng. Mô tả gốc không theo luật này → đặt
  `so_lan_tu_khoa: 0`.

Bố cục file `_tieu_de_mo_ta.txt`:

```
TITLE: <tiêu đề đã dịch>
TU_KHOA: <cụm từ khoá đã dịch>
DESCRIPTION:
<đoạn 1>

<đoạn 2>

00:00 <cụm từ khoá> …
MM:SS …
```

## 8. Upload lên YouTube Studio

1. Studio → video → **Ngôn ngữ** → thêm ngôn ngữ → **Bản lồng tiếng** → tải `<tên V>_<ngôn ngữ>.mp3`.
   Ngôn ngữ nào đã có bản auto-dub thì **xoá bản auto-dub trước**.
2. Cùng ngôn ngữ đó: thêm **Tiêu đề và mô tả** từ file `_tieu_de_mo_ta.txt`.
3. **Phụ đề:** tải `<tên V>_<ngôn ngữ>.srt`, chọn "Có thời gian".
`````

### FILE: `so-do.md`

`````markdown
# Sổ đo lồng tiếng

> File dữ liệu của skill `long-tieng`. `lt_03` tự ghi mục "Sổ tốc độ đọc"; agent chính ghi mục "Số đo theo tập" sau
> mỗi tập. ⛔ Không sửa tay số đã ghi. Giữ nguyên các tiêu đề `## ` — script tìm theo đúng chữ.

## Số đo theo tập
Agent chính ghi một dòng mỗi ngôn ngữ sau mỗi tập (SKILL.md §5).

| Ngày | Tập | Ngôn ngữ | Khối đạt | Tỉ lệ lời/khung | Viết lại | Credit |
|---|---|---|---|---|---|---|

## Sổ tốc độ đọc theo ngôn ngữ
Skill `long-tieng` TỰ GHI sau lần đọc đầu của mỗi ngôn ngữ, mỗi tập một dòng; `lt_02` lấy trung vị ký tự/giây để dự báo độ dài từng khối trước khi đọc.

| Ngày | Tập | Ngôn ngữ | Ký tự/giây lời | Lời/khung lần đầu (trung vị) | Số khối đo | Ghi chú |
|---|---|---|---|---|---|---|

## Ghi chú vận hành
Giới hạn đồng thời của ai33, lỗi gặp khi chạy, v.v.
`````

### FILE: `scripts/ai33.py`

`````python
"""Client TTS ai33 cho skill long-tieng (tách từ script đọc voice gốc của skill viet-kich-ban).

Thông số giọng lấy từ frontmatter quy-tac.md (tts_provider, voice_id, speed, pronunciation_dictionary_id).
API key lấy từ biến môi trường AI33_API_KEY, không có thì từ file ~/.secrets/tts.env (đổi chỗ bằng biến TTS_SECRETS),
dòng `AI33_API_KEY=...`. ⛔ Không để key trong thư mục dự án.
"""
import os
import re
import sys
import time
from pathlib import Path

import requests

FILE_CAU_HINH = Path(__file__).resolve().parents[1] / "quy-tac.md"
FILE_BI_MAT = Path(os.environ.get("TTS_SECRETS", str(Path.home() / ".secrets" / "tts.env")))


def loi(thong_diep: str) -> None:
    print(f"LOI: {thong_diep}", file=sys.stderr)
    raise SystemExit(2)


# --- cấu hình -------------------------------------------------------------


def doc_cau_hinh() -> dict:
    if not FILE_CAU_HINH.is_file():
        loi(f"khong thay file cau hinh {FILE_CAU_HINH}")
    van_ban = FILE_CAU_HINH.read_text(encoding="utf-8")
    khop = re.match(r"---\n(.*?)\n---", van_ban, re.S)
    if not khop:
        loi(f"{FILE_CAU_HINH.name} khong co frontmatter")
    ch = {}
    for dong in khop.group(1).splitlines():
        m = re.match(r"([a-z_]+):\s*(.*?)\s*$", dong)
        if m:
            ch[m.group(1)] = m.group(2)
    for khoa in ("tts_provider", "voice_id", "speed"):
        if not ch.get(khoa):
            loi(f"{FILE_CAU_HINH.name} thieu khoa `{khoa}`")
    if ch["voice_id"].startswith("<"):
        loi(f"chua dien voice_id trong {FILE_CAU_HINH.name}")
    if ch["tts_provider"] != "ai33":
        loi(f"chua ho tro tts_provider={ch['tts_provider']}")
    ch.setdefault("with_transcript", "false")
    return ch


def lay_key(nha_cung_cap: str) -> str:
    ten = f"{nha_cung_cap.upper()}_API_KEY"
    if os.environ.get(ten):
        return os.environ[ten]
    if FILE_BI_MAT.is_file():
        for dong in FILE_BI_MAT.read_text(encoding="utf-8").splitlines():
            if dong.strip().startswith(f"{ten}="):
                return dong.split("=", 1)[1].strip()
    loi(f"khong thay {ten} (bien moi truong hoac {FILE_BI_MAT})")


# --- nhà cung cấp: ai33 ---------------------------------------------------


class Ai33:
    GOC = "https://api.ai33.pro"

    def __init__(self, key: str):
        self.h = {"xi-api-key": key}

    def _get(self, duong: str) -> dict:
        for lan in range(5):
            try:
                r = requests.get(self.GOC + duong, headers=self.h, timeout=30)
                if r.status_code >= 500:
                    raise requests.RequestException(f"HTTP {r.status_code}")
                r.raise_for_status()
                return r.json()
            except requests.RequestException as e:
                if lan == 4:
                    loi(f"GET {duong}: {e}")
                time.sleep(3 * (lan + 1))

    def credits(self):
        return self._get("/v1/credits").get("credits")

    def health(self) -> dict:
        return self._get("/v1/health-check").get("data", {})

    def gui(self, van_ban: str, ch: dict, ten_file: str) -> str:
        truong = {
            "text": van_ban,
            "voice_id": ch["voice_id"],
            "speed": ch["speed"],
            "with_transcript": ch["with_transcript"],
            "file_name": ten_file,
        }
        if ch.get("pronunciation_dictionary_id"):
            truong["pronunciation_dictionary_id"] = ch["pronunciation_dictionary_id"]
        # files= ép multipart/form-data đúng như API yêu cầu; không tự thử lại để khỏi tạo hai task
        r = requests.post(
            self.GOC + "/v3/text-to-speech",
            headers=self.h,
            files={k: (None, str(v)) for k, v in truong.items()},
            timeout=120,
        )
        try:
            du_lieu = r.json()
        except ValueError:
            loi(f"gui task: HTTP {r.status_code} {r.text[:300]}")
        if not du_lieu.get("success") or not du_lieu.get("task_id"):
            loi(f"gui task that bai: HTTP {r.status_code} {du_lieu}")
        return du_lieu["task_id"]

    def task(self, task_id: str) -> dict:
        return self._get(f"/v1/task/{task_id}")


def tai(url: str, dich: Path) -> None:
    tam = dich.with_suffix(dich.suffix + ".part")
    for lan in range(5):
        try:
            with requests.get(url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(tam, "wb") as f:
                    for khuc in r.iter_content(1 << 16):
                        f.write(khuc)
            tam.replace(dich)
            return
        except requests.RequestException as e:
            if lan == 4:
                loi(f"tai {url}: {e}")
            time.sleep(3 * (lan + 1))
`````

### FILE: `scripts/tron_am.py`

`````python
"""Công thức trộn tiếng của skill long-tieng (chép nguyên từ bước dựng video của bản gốc).

ffmpeg: biến môi trường FFMPEG trỏ tới ffmpeg.exe, không có thì gọi `ffmpeg` trong PATH.
"""
import os

FF = os.environ.get("FFMPEG", "ffmpeg")
LUFS_RA = -14.0


def loc_tron_am(T, sr, vo, nh, sx):
    """Công thức trộn tiếng DUY NHẤT của kênh: giọng + nhạc (sidechain theo giọng) + SFX → [a]. Bản gốc dùng đúng hàm
    này cho cả bước dựng video lẫn skill long-tieng — để bản lồng tiếng luôn trộn y hệt bản gốc. vo/nh/sx = nhãn đầu vào.
    2026-10-08 đã thử bỏ sidechain (nhạc chỉ lên ở nghỉ chương) và thử sidechain chỉ ở mở bài — chủ kênh nghe cả hai
    đều chưa ổn, khôi phục nguyên bản này."""
    return [f"{vo}atrim=0:{T:.3f},asetpts=PTS-STARTPTS,aresample={sr},"
            f"afade=t=out:st={T - 0.5:.3f}:d=0.5,asplit=2[vo][vsc]",
            f"{nh}[vsc]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=350[md]",
            f"{sx}aresample={sr},pan=stereo|c0=c0|c1=c0[sx]",
            f"[vo][md][sx]amix=inputs=3:normalize=0:duration=first,afade=t=out:st={T - 0.6:.3f}:d=0.6,"
            f"loudnorm=I={LUFS_RA}:TP=-1.5:LRA=11,aresample={sr}[a]"]
`````

### FILE: `scripts/lt_lib.py`

`````python
"""Thư viện chung của skill long-tieng.

Thông số ở quy-tac.md (frontmatter, thư mục skill). Hai module đi kèm:
- ai33.py: client ai33 + thông số giọng
- tron_am.py: loc_tron_am() — công thức trộn âm, để bản lồng tiếng trộn y hệt bản gốc
"""
import difflib, hashlib, importlib.util, json, os, re, subprocess, sys, unicodedata
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

GOC_SKILL = Path(__file__).resolve().parents[1]
FILE_CAU_HINH = GOC_SKILL / "quy-tac.md"
MARKER = re.compile(r"<#[\d.]+#>")
HET_CAU = re.compile(r"[.?!…][\"'»”)\]]*$")
SR = 48000

_dv = None
_ing = None


def dung(msg):
    print(f"⛔ {msg}", file=sys.stderr)
    raise SystemExit(2)


def doc_voice():
    """Module ai33.py (client ai33, thông số giọng)."""
    global _dv
    if _dv is None:
        p = Path(__file__).resolve().parent / "ai33.py"
        sp = importlib.util.spec_from_file_location("ai33", p)
        _dv = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(_dv)
    return _dv


def tron_am():
    """Module tron_am.py (FF, LUFS_RA, loc_tron_am)."""
    global _ing
    if _ing is None:
        d = str(Path(__file__).resolve().parent)
        if d not in sys.path:
            sys.path.insert(0, d)
        import tron_am as m
        _ing = m
    return _ing


def frontmatter(p):
    s = Path(p).read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", s, re.S)
    if not m:
        dung(f"{Path(p).name} không có frontmatter")
    ch = {}
    for d in m.group(1).splitlines():
        k = re.match(r"([a-z_]+):\s*(.*?)\s*$", d)
        if k:
            ch[k.group(1)] = k.group(2)
    return ch


def cau_hinh():
    ch = frontmatter(FILE_CAU_HINH)
    for k in ("ngon_ngu", "khoi_toi_da_giay", "nghi_that_giay", "nguong_khe_marker", "nen_toi_da", "gian_toi_da",
              "marker_tach_khoi", "bitrate_ra", "co_gian", "khong_co_gian", "nghi_cuoi_khoi", "khoi_muc_tieu_giay",
              "khoi_tran_giay", "khoi_toi_thieu_giay", "du_lang_toi_da"):
        if not ch.get(k):
            dung(f"{FILE_CAU_HINH.name} thiếu khoá `{k}`")
    ch["ds_ngon_ngu"] = {}
    for khoa, thu in (("ngon_ngu", False), ("ngon_ngu_thu", True)):   # _thu: chỉ nghe thử, ngoài lượt chính
        for muc in filter(None, ch.get(khoa, "").split(";")):
            ten, ma, hien = [x.strip() for x in muc.split("=")]
            ch["ds_ngon_ngu"][ten] = dict(ma=ma, hien=hien, thu=thu)
    return ch


def chu_ky(ch):
    """Dấu của cách khớp: đổi co_gian hoặc khong_co_gian → mọi khối được khớp lại (không đọc lại voice)."""
    return f"{ch['co_gian']}|{ch['khong_co_gian']}|{ch['nghi_cuoi_khoi']}"


def khung_loi(khung, ch):
    """Phần khung dành cho LỜI: trừ khoảng lặng cuối khối (nghi_cuoi_khoi) để có nhịp nghỉ giữa hai khối như giọng
    thật (chủ kênh 2026-10-08). Khối ngắn hơn hai lần khoảng nghỉ thì chừa 20% khung."""
    nghi = float(ch["nghi_cuoi_khoi"])
    return khung - nghi if khung > 2 * nghi else khung * 0.8


def toc_chuong(r, ch):
    """Tốc độ chung của một chương từ các tỉ lệ lời/khung-lời r: trung vị, kẹp trong ngưỡng; gần khớp sẵn → 1 (giọng
    thô). lt_03 dùng để khớp, lt_02 dùng để dự báo — chung một hàm để dự báo chấm đúng luật lúc khớp thật."""
    gian, nen, tho = float(ch["gian_toi_da"]), float(ch["nen_toi_da"]), float(ch["khong_co_gian"])
    t = min(max(float(np.median(r)), 1 - gian), 1 + nen)
    return 1.0 if 1 - tho <= t <= 1 else t


def vung_dat(tc, ch, bien=0.0):
    """(thấp, cao) của tỉ lệ lời/khung-lời để khối ĐẠT trong chương tốc độ tc, theo đúng luật lt_03: dài hơn 1+nen →
    VUOT ngắn lại; đọc ở tốc độ chương còn lặng dư quá du_lang_toi_da → VUOT dài thêm (ngưỡng dưới = tc·(1−du_lang),
    KHÔNG phải 1−gian). bien: thu hẹp hai đầu cho dự báo, vì tốc độ đọc thật dao động theo khối."""
    return tc * (1 - float(ch["du_lang_toi_da"])) + bien, 1 + float(ch["nen_toi_da"]) - bien


# ---------------------------------------------------------------- sổ tốc độ đọc theo ngôn ngữ (so-do.md)
# Mỗi tập, lần đọc ĐẦU của mỗi ngôn ngữ ghi một dòng; lt_02 dùng sổ để dự báo khối nào sẽ lệch khung TRƯỚC khi tốn credit
# (chủ kênh 2026-10-08: tiếng Việt đọc nhanh hơn khung ~17% mà lần đầu không ai biết trước).
FILE_SO = GOC_SKILL / "so-do.md"
DAU_SO = "## Sổ tốc độ đọc theo ngôn ngữ"


def doc_so():
    """[(tập, ngôn ngữ, ký tự/giây lời)] từ bảng sổ trong so-do.md."""
    if not FILE_SO.is_file():
        return []
    s = FILE_SO.read_text(encoding="utf-8")
    if DAU_SO not in s:
        return []
    ra_ = []
    for d in s.split(DAU_SO, 1)[1].split("\n## ", 1)[0].splitlines():
        o = [x.strip() for x in d.strip().strip("|").split("|")]
        if len(o) >= 5 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", o[0]) and o[1] and o[2]:
            try:
                ra_.append((o[1], o[2], float(o[3].replace(",", "."))))
            except ValueError:
                pass
    return ra_


def toc_do(nn):
    """Ký tự/giây lời của ngôn ngữ (trung vị các tập đã đo) hoặc None."""
    x = [c for _, n, c in doc_so() if n == nn]
    return float(np.median(x)) if x else None


def ghi_so(tap, nn, cps, tl_tv, so_khoi, ghi_chu=""):
    """Thêm một dòng sổ — chỉ một dòng cho mỗi (tập, ngôn ngữ): lần đọc đầu mới đại diện cho bản dịch chưa chỉnh."""
    if any(t == tap and n == nn for t, n, _ in doc_so()):
        return False
    import datetime
    vn = lambda x: f"{x:.2f}".replace(".", ",")
    dong = f"| {datetime.date.today().isoformat()} | {tap} | {nn} | {vn(cps)} | {vn(tl_tv)} | {so_khoi} | {ghi_chu} |"
    s = FILE_SO.read_text(encoding="utf-8")
    if DAU_SO not in s:
        s = s.replace("\n## Liên quan", f"\n{DAU_SO}\nSkill `long-tieng` TỰ GHI sau lần đọc đầu của mỗi ngôn ngữ, mỗi tập một dòng; "
                      "`lt_02` lấy trung vị ký tự/giây để dự báo độ dài từng khối trước khi đọc.\n\n"
                      "| Ngày | Tập | Ngôn ngữ | Ký tự/giây lời | Lời/khung lần đầu (trung vị) | Số khối đo | Ghi chú |\n"
                      "|---|---|---|---|---|---|---|\n\n## Liên quan", 1)
    dau = s.index(DAU_SO)
    het = s.find("\n## ", dau + 5)
    khoi_so = s[dau:het].rstrip("\n") + "\n" + dong + "\n"
    FILE_SO.write_text(s[:dau] + khoi_so + s[het:], encoding="utf-8")
    return True


def kiem_kenh(v):
    if not Path(v).is_dir():
        dung(f"không thấy thư mục tập {v}")


def tm(v):
    return Path(v) / "_tmp_skill" / "long-tieng"


def ra(v):
    return Path(v) / "voice" / "long_tieng"


def ten_ra(v, nn, duoi):
    return ra(v) / f"{Path(v).name}_{nn}{duoi}"


def file_dich(v, nn):
    """Bản dịch theo khối — file LÀM VIỆC của skill (chữ TTS đọc), nằm trong thư mục tạm, không giao user (chủ kênh
    2026-10-08). Bị xoá cùng _tmp_skill/long-tieng/ khi mọi ngôn ngữ xong bước 4."""
    return tm(v) / nn / f"{Path(v).name}_{nn}.txt"


def tim_script(v):
    ds = [p for p in Path(v).glob("script_*.txt") if re.fullmatch(r"script_[^.]+\.txt", p.name)
          and not p.stem.endswith(("_beat", "_goc", "_backup", "_upload"))]
    if len(ds) != 1:
        dung(f"cần đúng 1 script_*.txt trong {v}, thấy {[p.name for p in ds]}")
    return ds[0]


def khoi(script, nhan):
    """Nội dung khối `<nhan>:` của file kịch bản (TITLE / DESCRIPTION / SOURCE), tới nhãn khối kế tiếp. Không có → None."""
    # chấp nhận cả "TITLE: <chữ>" trên cùng dòng (0928) lẫn "TITLE:" rồi xuống dòng (0926)
    m = re.search(rf"^{nhan}:[ \t]*", script, re.M)
    if not m:
        return None
    sau = re.search(r"^(TITLE|DESCRIPTION|SOURCE|SCRIPT):", script[m.end():], re.M)
    return script[m.end():m.end() + sau.start() if sau else len(script)].strip()


def doc_srt(p):
    s = Path(p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    moc = r"(\d+):(\d+):(\d+)[,.](\d+)"
    cue = []
    for m in re.finditer(moc + r"\s*-->\s*" + moc + r"\n(.*?)(?=\n\s*\n|\Z)", s, re.S):
        g = [int(x) for x in m.groups()[:8]]
        cue.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                    " ".join(m.group(9).split())))
    return cue


def chuan(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if unicodedata.category(c)[0] in "LN")


def gio(x):
    ms = round(x * 1000)
    return f"{ms // 60000:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}"


def gio_srt(x):
    ms = round(x * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def bam(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------- khối
def chia_khoi(cue, ch):
    """Cue SRT → câu → khối. Trả list khối: dict(c0, c1 chỉ số cue, a, b giây, chuong)."""
    cau, cur = [], None
    for i, (s, e, t) in enumerate(cue):
        cur = [i, i] if cur is None else [cur[0], i]
        if HET_CAU.search(t):
            cau.append(cur)
            cur = None
    if cur:
        cau.append(cur)
    nghi, mk = float(ch["nghi_that_giay"]), float(ch["nguong_khe_marker"])
    doan, chuong, ds_chuong = [[cau[0]]], 0, [0]
    for x, y in zip(cau, cau[1:]):
        khe = cue[y[0]][0] - cue[x[1]][1]
        if khe >= nghi:
            doan.append([])
            if khe >= mk:
                chuong += 1
            ds_chuong.append(chuong)
        doan[-1].append(y)

    tran = float(ch["khoi_toi_da_giay"])

    def chia(d):
        L = cue[d[-1][1]][1] - cue[d[0][0]][0]
        if L <= tran or len(d) == 1:
            return [d]
        giua = cue[d[0][0]][0] + L / 2
        k = min(range(1, len(d)), key=lambda j: abs(cue[d[j][0]][0] - giua))
        return chia(d[:k]) + chia(d[k:])

    nho = []
    for d, c in zip(doan, ds_chuong):
        for k in chia(d):
            nho.append(dict(c0=k[0][0], c1=k[-1][1], a=cue[k[0][0]][0], b=cue[k[-1][1]][1], chuong=c))
    khoi = gop_khoi(nho, ch)
    for j, k in enumerate(khoi, 1):
        k["id"] = f"K{j:03d}"
    return khoi


def gop_khoi(nho, ch):
    """Gộp khối nhỏ liền nhau TRONG CÙNG CHƯƠNG thành khối đọc (chủ kênh 2026-10-08): mỗi khối là một lượt đọc rời của
    TTS, càng nhiều khối càng nhiều chỗ ngữ điệu bắt đầu lại → nghe rời rạc (0926: 101 khối, 19 khối < 8 s). Gom tới khi
    ≥ khoi_muc_tieu_giay mà không vượt khoi_tran_giay; khối còn < khoi_toi_thieu_giay thì gộp nốt vào khối kề trong
    chương. Ranh giới mới luôn là ranh giới cũ — bản dịch theo khối cũ ghép lại được, không phải dịch lại."""
    muc, tran, it = (float(ch["khoi_muc_tieu_giay"]), float(ch["khoi_tran_giay"]), float(ch["khoi_toi_thieu_giay"]))
    dai = lambda g: g[-1]["b"] - g[0]["a"]
    nhom = []
    for k in nho:
        g = nhom[-1] if nhom else None
        if g and g[-1]["chuong"] == k["chuong"] and dai(g) < muc and k["b"] - g[0]["a"] <= tran:
            g.append(k)
        else:
            nhom.append([k])
    i = 0
    while i < len(nhom):                     # khối còn quá ngắn: gộp vào khối kề ngắn hơn trong cùng chương
        g = nhom[i]
        if dai(g) < it:
            ke = [j for j in (i - 1, i + 1) if 0 <= j < len(nhom) and nhom[j][0]["chuong"] == g[0]["chuong"]]
            if ke:
                j = min(ke, key=lambda j: dai(nhom[j]))
                a, b = sorted((i, j))
                nhom[a:b + 1] = [nhom[a] + nhom[b]]
                i = max(a - 1, 0)
                continue
        i += 1
    return [dict(c0=g[0]["c0"], c1=g[-1]["c1"], a=g[0]["a"], b=g[-1]["b"], chuong=g[0]["chuong"]) for g in nhom]


def gan_chu(khoi, cue, than):
    """Gán chữ của KỊCH BẢN (không phải SRT — SRT bị TTS chuẩn hoá) cho từng khối: khớp từ SRT ↔ kịch bản bằng
    difflib, rồi chốt ranh giới ở từ kết thúc câu gần nhất của kịch bản."""
    tk = MARKER.sub(" ", than).split()
    nk = [chuan(w) for w in tk]
    ts, het_khoi = [], []
    for k in khoi:
        for i in range(k["c0"], k["c1"] + 1):
            ts += [chuan(w) for w in cue[i][2].split()]
        het_khoi.append(len(ts) - 1)
    map_ = {}
    for a, b, n in difflib.SequenceMatcher(None, nk, ts, autojunk=False).get_matching_blocks():
        for x in range(n):
            map_[b + x] = a + x
    khop = len(map_) / max(len(ts), 1)
    cat, truoc = [], -1
    for j in het_khoi[:-1]:
        jj = max((x for x in map_ if x <= j), default=None)
        if jj is None:
            dung("không khớp được SRT với kịch bản")
        i = map_[jj] + (j - jj)
        vung = range(max(truoc + 1, i - 8), min(len(tk), i + 9))
        # SRT của ai33 có khi đặt dấu chấm ở chỗ kịch bản là dấu phẩy (0928: "gigante," → "gigante.") — khi không có
        # cuối câu gần đó thì chốt ở dấu phẩy / chấm phẩy / hai chấm gần nhất
        ung = [x for x in vung if HET_CAU.search(tk[x])] or [x for x in vung if re.search(r"[,;:]$", tk[x])]
        if not ung:
            dung(f"không tìm được chỗ ngắt trong kịch bản quanh từ '{tk[min(i, len(tk) - 1)]}' — xem lại SRT/kịch bản")
        i = min(ung, key=lambda x: abs(x - i))
        cat.append(i)
        truoc = i
    dau = 0
    for k, c in zip(khoi, cat + [len(tk) - 1]):
        k["goc"] = " ".join(tk[dau:c + 1])
        dau = c + 1
    return khop


# ---------------------------------------------------------------- file dịch theo khối
RE_DAU = re.compile(r"^### (K\d{3}) \| .*$", re.M)


def dau_khoi(k):
    return f"### {k['id']} | {gio(k['a'])} → {gio(k['b'])} | {k['b'] - k['a']:.2f} s"


def ghi_khoi(p, khoi, truong):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text("\n\n".join(f"{dau_khoi(k)}\n{k[truong]}" for k in khoi) + "\n", encoding="utf-8")


def doc_dich(p):
    """{id: (dòng đầu khối, chữ)} theo thứ tự trong file."""
    s = Path(p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    ms = list(RE_DAU.finditer(s))
    ra_ = {}
    for i, m in enumerate(ms):
        het = ms[i + 1].start() if i + 1 < len(ms) else len(s)
        ra_[m.group(1)] = (m.group(0).strip(), " ".join(s[m.end():het].split()))
    return ra_


def doc_khoi(v):
    p = tm(v) / "khoi.json"
    if not p.is_file():
        dung(f"chưa có {p} — chạy lt_01_chia_khoi.py trước")
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- âm thanh
def doc_am(p, af=None):
    L = tron_am()
    c = [L.FF, "-v", "error", "-i", str(p)] + (["-af", af] if af else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(c, capture_output=True, check=True).stdout, np.float32).copy()


def ghi_am(x, p, extra=()):
    """File .wav trung gian ghi dạng FLOAT: giọng ai33 có đỉnh tới 1,19–1,34 — ghi 16-bit là cắt cụt → tiếng rè
    (chủ kênh nghe ra ở bản thử tiếng Anh 2026-10-08). Mức cuối do loudnorm của bước trộn lo."""
    L = tron_am()
    if str(p).lower().endswith(".wav") and not extra:
        extra = ("-c:a", "pcm_f32le")
    subprocess.run([L.FF, "-v", "error", "-y", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-", *extra, str(p)],
                   input=np.asarray(x, np.float32).tobytes(), check=True)


def co_tieng(x, nguong_db=-40):
    e = np.sqrt(np.convolve(x ** 2, np.ones(480) / 480, "same"))
    return e > 10 ** (nguong_db / 20)


def cat_lang(x):
    t = np.flatnonzero(co_tieng(x))
    return x[t[0]:t[-1] + 1] if len(t) else x[:0]


def tach_doan(x, n):
    """Tách audio n khối (nối bằng marker nghỉ dài) tại n-1 khoảng lặng DÀI NHẤT. Trả list đoạn đã cắt lặng hai đầu."""
    t = co_tieng(x)
    lang, i = [], 0
    while i < len(t):
        if not t[i]:
            j = i
            while j < len(t) and not t[j]:
                j += 1
            if i > 0 and j < len(t):
                lang.append((j - i, i, j))
            i = j
        else:
            i += 1
    if len(lang) < n - 1:
        return None, f"chỉ có {len(lang)} khoảng lặng, cần {n - 1}"
    chon = sorted(sorted(lang, reverse=True)[:n - 1], key=lambda z: z[1])
    ngan = min((z[0] for z in chon), default=SR * 9) / SR
    if n > 1 and ngan < 1.2:
        return None, f"khoảng lặng tách khối ngắn nhất chỉ {ngan:.2f} s (< 1,2 s) — marker không tạo nghỉ đủ dài"
    moc = [0] + [(z[1] + z[2]) // 2 for z in chon] + [len(x)]
    return [cat_lang(x[a:b]) for a, b in zip(moc, moc[1:])], None


def gian(x, dich_giay, loc):
    """Kéo đoạn x về đúng dich_giay bằng bộ lọc `loc` (khoá co_gian ở quy tắc kênh, có chỗ {tl} = tempo)."""
    tl = len(x) / SR / dich_giay
    tmp = Path(os.environ.get("TEMP", ".")) / f"_lt_{os.getpid()}.wav"
    ghi_am(x, tmp)
    y = doc_am(tmp, loc.format(tl=f"{tl:.5f}"))
    tmp.unlink(missing_ok=True)
    n = int(round(dich_giay * SR))
    return np.pad(y, (0, max(0, n - len(y))))[:n]


def thoi_luong(p):
    L = tron_am()
    o = subprocess.run([L.FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True, encoding="utf-8",
                       errors="replace").stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", o)
    if not m:
        dung(f"không đọc được thời lượng {p}")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
`````

### FILE: `scripts/lt_01_chia_khoi.py`

`````python
"""Bước 1 — chia khối nghĩa từ SRT gốc, gán chữ kịch bản cho từng khối. Chạy MỘT lần, dùng chung cho mọi ngôn ngữ.

Dùng:  python lt_01_chia_khoi.py "<thư mục tập>" [--ghi-de]
Sinh:  _tmp_skill/long-tieng/khoi.json · khoi_goc.txt (bản ngôn ngữ gốc cho agent dịch) · nguon_tieu_de_mo_ta.txt
"""
import argparse, json, re, statistics
from pathlib import Path

import lt_lib as T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    ap.add_argument("--ghi-de", action="store_true")
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    d = T.tm(v)
    if (d / "khoi.json").exists() and not a.ghi_de:
        T.dung(f"{d / 'khoi.json'} đã có — các bản dịch đang bám theo nó. Chỉ dùng --ghi-de khi chắc chắn làm lại từ đầu")

    script = T.tim_script(v).read_text(encoding="utf-8")
    if "SCRIPT:" not in script:
        T.dung("kịch bản không có khối SCRIPT:")
    than = script.split("SCRIPT:", 1)[1]
    srt = v / "voice" / f"{v.name}.srt"
    if not srt.is_file():
        T.dung(f"chưa có {srt} — cần voice gốc + SRT trước")
    cue = T.doc_srt(srt)

    khoi = T.chia_khoi(cue, ch)
    so_marker = len(T.MARKER.findall(than))
    if khoi[-1]["chuong"] != so_marker:
        T.dung(f"đếm được {khoi[-1]['chuong']} ranh giới chương trong SRT nhưng kịch bản có {so_marker} marker")
    khop = T.gan_chu(khoi, cue, than)
    if khop < 0.9:
        T.dung(f"chỉ khớp {khop:.1%} từ SRT với kịch bản — kịch bản đã sửa sau khi đọc voice?")

    d.mkdir(parents=True, exist_ok=True)
    (d / "khoi.json").write_text(json.dumps(khoi, ensure_ascii=False, indent=1), encoding="utf-8")
    T.ghi_khoi(d / "khoi_goc.txt", khoi, "goc")
    # tiêu đề + mô tả lấy thẳng từ file kịch bản: khối TITLE: và DESCRIPTION:
    mo_ta = T.khoi(script, "DESCRIPTION")
    nguon = f"TITLE: {T.khoi(script, 'TITLE') or ''}\nDESCRIPTION:\n" + (mo_ta or "(chưa có mô tả gốc)")
    (d / "nguon_tieu_de_mo_ta.txt").write_text(nguon + "\n", encoding="utf-8")

    L = [k["b"] - k["a"] for k in khoi]
    print(f"✓ {len(khoi)} khối · {khoi[-1]['chuong'] + 1} chương · khớp chữ {khop:.1%}")
    print(f"  độ dài khối: trung vị {statistics.median(L):.1f} s · ngắn nhất {min(L):.1f} · dài nhất {max(L):.1f}")
    print(f"  12–20 s: {sum(12 <= x <= 20 for x in L)} · < 8 s: {sum(x < 8 for x in L)} · > 20 s: {sum(x > 20 for x in L)}")
    if not mo_ta:
        print("⚠️  kịch bản chưa có khối DESCRIPTION: — bản dịch chỉ có tiêu đề (thêm khối DESCRIPTION: vào kịch bản rồi chạy lại --ghi-de)")
    print(f"→ {d / 'khoi_goc.txt'}")


if __name__ == "__main__":
    main()
`````

### FILE: `scripts/lt_02_kiem_dich.py`

`````python
"""Bước 2 — CỔNG kiểm bản dịch của một ngôn ngữ, trước khi tốn credit đọc voice.

Dùng:  python lt_02_kiem_dich.py "<thư mục tập>" --ngon-ngu tieng_anh
Kiểm:  _tmp_skill/long-tieng/<ngôn ngữ>/<tên V>_<ngôn ngữ>.txt (bản dịch theo khối)  +  voice/long_tieng/<tên V>_<ngôn ngữ>_tieu_de_mo_ta.txt
Thoát 0 = PASS · 1 = có vi phạm · 2 = lỗi đầu vào.
"""
import argparse, re
from pathlib import Path

import lt_lib as T

SO = re.compile(r"[0-9٠-٩０-９]")
MOC = re.compile(r"^(\d{2}):(\d{2})\s+(\S.*)$")


def tach_mo_ta(s):
    """(tiêu đề, từ khoá, [đoạn văn], [(mốc, nhãn)]) từ file tiêu đề + mô tả."""
    tieu_de = re.search(r"^TITLE:\s*(.*)$", s, re.M)
    tu_khoa = re.search(r"^TU_KHOA:\s*(.*)$", s, re.M)
    than = s.split("DESCRIPTION:", 1)[1] if "DESCRIPTION:" in s else ""
    van, moc = [], []
    for d in than.strip().split("\n"):
        m = MOC.match(d.strip())
        if m:
            moc.append((m.group(1) + ":" + m.group(2), m.group(3)))
        else:
            van.append(d)
    doan = [x for x in re.split(r"\n\s*\n", "\n".join(van).strip()) if x.strip()]
    return (tieu_de.group(1).strip() if tieu_de else "", tu_khoa.group(1).strip() if tu_khoa else "", doan, moc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    ap.add_argument("--ngon-ngu", required=True)
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    nn = a.ngon_ngu
    if nn not in ch["ds_ngon_ngu"]:
        T.dung(f"ngôn ngữ '{nn}' không có trong quy-tac.md: {list(ch['ds_ngon_ngu'])}")
    khoi = T.doc_khoi(v)
    vp = []

    # ---- bản dịch theo khối
    f = T.file_dich(v, nn)
    if not f.is_file():
        T.dung(f"chưa có {f}")
    dich = T.doc_dich(f)
    if [k["id"] for k in khoi] != list(dich):
        thieu = [k["id"] for k in khoi if k["id"] not in dich]
        thua = [x for x in dich if x not in {k["id"] for k in khoi}]
        vp.append(f"danh sách khối lệch khoi.json — thiếu {thieu[:8]} · thừa {thua[:8]} · hoặc sai thứ tự")
    for k in khoi:
        if k["id"] not in dich:
            continue
        dau, chu = dich[k["id"]]
        if dau != T.dau_khoi(k):
            vp.append(f"{k['id']}: dòng đầu khối bị sửa — giữ nguyên `{T.dau_khoi(k)}`")
        if not chu:
            vp.append(f"{k['id']}: rỗng")
        elif chu == k["goc"]:
            vp.append(f"{k['id']}: chưa dịch (trùng nguyên văn bản gốc)")
        if SO.search(chu):
            vp.append(f"{k['id']}: còn chữ số `{SO.search(chu).group(0)}` — viết số bằng chữ")
        if "<#" in chu or "###" in chu:
            vp.append(f"{k['id']}: còn marker hoặc dấu ###")

    # ---- tiêu đề + mô tả
    fm = T.ten_ra(v, nn, "_tieu_de_mo_ta.txt")
    nguon = (T.tm(v) / "nguon_tieu_de_mo_ta.txt").read_text(encoding="utf-8")
    _, _, doan_g, moc_g = tach_mo_ta(nguon)
    if not fm.is_file():
        vp.append(f"chưa có {fm.name}")
    else:
        td, kw, doan, moc = tach_mo_ta(fm.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
        if not td:
            vp.append("tiêu đề: thiếu dòng TITLE:")
        if moc_g:
            so_lan = int(T.frontmatter(T.FILE_CAU_HINH).get("so_lan_tu_khoa") or 0)   # 0 = không kiểm luật từ khoá
            if so_lan and not kw:
                vp.append("mô tả: thiếu dòng TU_KHOA:")
            if len(doan) != len(doan_g):
                vp.append(f"mô tả: {len(doan)} đoạn, bản gốc {len(doan_g)}")
            if [m for m, _ in moc] != [m for m, _ in moc_g]:
                vp.append(f"mô tả: mốc {[m for m, _ in moc]} khác bản gốc {[m for m, _ in moc_g]} — giữ nguyên mốc")
            if so_lan and kw:
                n = " ".join(doan).lower().count(kw.lower())
                if n != so_lan:
                    vp.append(f"mô tả: từ khoá '{kw}' xuất hiện {n} lần trong phần văn, cần {so_lan}")
                if moc and not moc[0][1].lower().startswith(kw.lower()):
                    vp.append(f"mô tả: nhãn dòng 00:00 không mở đầu bằng '{kw}'")

    # ---- dự báo độ dài từ sổ tốc độ đọc (wiki) — chỉ CẢNH BÁO, để agent chỉnh bản dịch TRƯỚC khi tốn credit
    cps = T.toc_do(nn)
    if cps is None:
        print(f"dự báo   : chưa có số đo tốc độ đọc của {nn} trong sổ — lần đọc đầu sẽ tự ghi")
    else:
        # Chấm ĐÚNG luật lt_03 (chủ kênh 2026-10-08, sau 0928): tốc độ chương + lặng dư + ngưỡng nén, qua chung hàm
        # T.toc_chuong / T.vung_dat. Bản cũ chỉ chặn dưới ở 1−gian (0,70) trong khi lt_03 bắt "viết dài thêm" từ
        # ~0,77–0,85 → khối lọt dự báo rồi phải đọc lại. Biên an toàn bien_du_bao: tốc độ đọc thật dao động theo khối.
        bien = float(ch.get("bien_du_bao") or 0.04)
        du = {}                                  # id -> (tỉ lệ dự báo, khung lời)
        for k in khoi:
            if k["id"] in dich:
                kl = T.khung_loi(k["b"] - k["a"], ch)
                du[k["id"]] = (len(dich[k["id"]][1]) / cps / kl, kl)
        lech = []
        for c in sorted({k["chuong"] for k in khoi}):
            ids = [k["id"] for k in khoi if k["chuong"] == c and k["id"] in du]
            if not ids:
                continue
            tc = T.toc_chuong([du[i][0] for i in ids], ch)
            thap, cao = T.vung_dat(tc, ch, bien)
            dich_tl = (thap + cao) / 2                   # nhắm GIỮA vùng đạt, không sát mép
            for i in ids:
                tl, kl = du[i]
                if not thap <= tl <= cao:
                    lech.append((i, tl, c, tc, len(dich[i][1]), round(cps * kl * dich_tl)))
        print(f"dự báo   : {cps:.2f} ký tự/giây lời (sổ) · lời/khung dự báo trung vị "
              f"{float(T.np.median([x[0] for x in du.values()])):.2f} · biên an toàn {bien:.2f} · "
              f"{len(lech)} khối dự báo ngoài vùng đạt")
        for i, tl, c, tc, n, nen_viet in lech:
            huong = "NGẮN lại" if tl > 1 else "DÀI thêm"
            print(f"CANH BAO: {i} dự báo {tl:.2f} (chương {c} tốc độ {tc:.2f}) — hiện {n} ký tự, viết {huong} "
                  f"khoảng {nen_viet} ký tự")

    so_ky_tu = sum(len(dich[k["id"]][1]) for k in khoi if k["id"] in dich)
    print(f"bản dịch : {f.name} · {len(dich)} khối · {so_ky_tu} ký tự (gốc {sum(len(k['goc']) for k in khoi)})")
    for x in vp:
        print(f"VI PHAM: {x}")
    print(f"Cong: {len(vp)} vi pham")
    return 1 if vp else 0


if __name__ == "__main__":
    raise SystemExit(main())
`````

### FILE: `scripts/lt_03_doc_khop.py`

`````python
"""Bước 3 — đọc voice một ngôn ngữ bằng ai33 rồi co giãn từng khối về khung gốc.

Dùng:  python lt_03_doc_khop.py "<thư mục tập>" --ngon-ngu tieng_anh

- Mỗi chương gửi MỘT task ai33, các khối nối bằng marker nghỉ dài (marker_tach_khoi) để tách lại chính xác.
- Chỉ đọc khối CHƯA có hoặc ĐÃ SỬA chữ (so mã băm). Sửa chữ một khối rồi chạy lại lệnh này = chỉ đọc lại khối đó.
- task_id lưu ở _tmp_skill/long-tieng/<ngôn ngữ>/tasks.json: bị ngắt thì chạy lại, polling tiếp, không trừ credit hai lần.
- Co giãn bằng bộ lọc co_gian trong ngưỡng nen_toi_da / gian_toi_da. Khối vượt ngưỡng → in VUOT, thoát 1:
  agent viết lại khối đó rồi chạy lại.
Ra:    _tmp_skill/long-tieng/<ngôn ngữ>/khop/<id>.wav · bao_cao.json
"""
import argparse, json, time
from pathlib import Path

import lt_lib as T

GIAY_CHO = 5
TRAN_CHO = 60 * 60
BAO_MOI = 60          # giây giữa hai dòng báo tiến độ khi chờ ai33


def ghi_json(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=1), encoding="utf-8")


def doc_json(p, mac_dinh):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else mac_dinh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    ap.add_argument("--ngon-ngu", required=True)
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    nn = a.ngon_ngu
    if nn not in ch["ds_ngon_ngu"]:
        T.dung(f"ngôn ngữ '{nn}' không có trong quy tắc kênh")
    khoi = T.doc_khoi(v)
    f = T.file_dich(v, nn)
    if not f.is_file():
        T.dung(f"chưa có {f}")
    dich = T.doc_dich(f)
    if [k["id"] for k in khoi] != list(dich) or any(not dich[k["id"]][1] for k in khoi):
        T.dung("bản dịch lệch khoi.json hoặc có khối rỗng — chạy lt_02_kiem_dich.py tới PASS trước")

    d = T.tm(v) / nn
    (d / "raw").mkdir(parents=True, exist_ok=True)
    (d / "khop").mkdir(exist_ok=True)
    meta = doc_json(d / "meta.json", {})
    tasks = doc_json(d / "tasks.json", {})

    # ---- khối cần đọc: chưa có hoặc chữ đã đổi; gom theo chương
    can = [k for k in khoi if meta.get(k["id"], {}).get("bam") != T.bam(dich[k["id"]][1])]
    nhom = {}
    for k in can:
        nhom.setdefault(k["chuong"], []).append(k["id"])
    sep = f"\n\n{ch['marker_tach_khoi']}\n\n"
    viec = []
    for c, ids in sorted(nhom.items()):
        van = sep.join(dich[i][1] for i in ids)
        viec.append(dict(khoa=T.bam(van), ids=ids, van=van, chuong=c))

    loi = []
    moi = []                     # khối vừa đọc trong lượt này (để ghi sổ tốc độ)
    credit_luot = 0
    if viec:
        dv = T.doc_voice()
        cv = dv.doc_cau_hinh()
        cv["with_transcript"] = "false"
        api = dv.Ai33(dv.lay_key(cv["tts_provider"]))
        print(f"{nn}: đọc {len(can)} khối trong {len(viec)} task · {sum(len(x['van']) for x in viec)} ký tự · "
              f"giọng {cv['voice_id']} speed {cv['speed']} · credit {api.credits()}")
        for x in viec:
            if x["khoa"] in tasks:
                print(f"  chương {x['chuong']}: tiếp tục task {tasks[x['khoa']]['task_id']}")
                continue
            tid = api.gui(x["van"], cv, f"{v.name}_{nn}_c{x['chuong']}")
            tasks[x["khoa"]] = dict(task_id=tid, ids=x["ids"], chuong=x["chuong"],
                                    gui_luc=time.strftime("%Y-%m-%d %H:%M:%S"))
            ghi_json(d / "tasks.json", tasks)
            print(f"  chương {x['chuong']}: gửi task {tid} ({len(x['ids'])} khối)")

        bd = time.time()
        con = {x["khoa"]: x for x in viec}
        bao_luc = time.time()
        while con:
            pct = {}
            for khoa in list(con):
                t = api.task(tasks[khoa]["task_id"])
                st = t.get("status")
                pct[con[khoa]["chuong"] if khoa in con else -1] = t.get("progress")
                if st == "error":
                    loi.append(f"chương {con[khoa]['chuong']}: task {tasks[khoa]['task_id']} lỗi: {t.get('error_message')}")
                    tasks.pop(khoa)
                    con.pop(khoa)
                elif st == "done":
                    x = con.pop(khoa)
                    mp3 = d / f"task_{khoa}.mp3"
                    dv.tai(t["metadata"]["audio_url"], mp3)
                    doan, ly_do = T.tach_doan(T.doc_am(mp3), len(x["ids"]))
                    if doan is None:
                        loi.append(f"chương {x['chuong']}: không tách được {len(x['ids'])} khối — {ly_do}. "
                                   f"Giữ {mp3.name} để xem")
                    else:
                        for i, seg in zip(x["ids"], doan):
                            T.ghi_am(seg, d / "raw" / f"{i}.wav")
                            meta[i] = dict(bam=T.bam(dich[i][1]), giay=round(len(seg) / T.SR, 3))
                            moi.append(i)
                        mp3.unlink()
                    tasks.pop(khoa)
                    ghi_json(d / "meta.json", meta)
                    print(f"  chương {x['chuong']}: xong · credit {t.get('credit_cost')}")
                    credit_luot += int(t.get("credit_cost") or 0)
                ghi_json(d / "tasks.json", tasks)
            if con and time.time() - bao_luc >= BAO_MOI:
                # nhịp báo tiến độ: agent chính đọc dòng này để báo user, chứng minh máy không treo (chủ kênh 2026-10-08)
                da = len(viec) - len(con)
                cho = ", ".join(f"c{c} {p if p is not None else '?'}%" for c, p in sorted(pct.items()) if c >= 0)
                print(f"  [{int(time.time() - bd) // 60}:{int(time.time() - bd) % 60:02d}] {nn}: {da}/{len(viec)} task xong"
                      f" · đang chờ: {cho}", flush=True)
                bao_luc = time.time()
            if con:
                if time.time() - bd > TRAN_CHO:
                    T.dung(f"quá {TRAN_CHO // 60} phút chưa xong — chạy lại lệnh để chờ tiếp")
                time.sleep(GIAY_CHO)
        print(f"  credit còn {api.credits()}")

    # ---- credit: cộng credit_cost của từng task, cộng dồn vào credit.json của ngôn ngữ. ⛔ Không đo bằng hiệu số dư
    # tài khoản: các agent chạy song song cùng một tài khoản ai33 (0928, 2026-10-08: số dư lẫn cả 5 ngôn ngữ).
    so_credit = doc_json(d / "credit.json", dict(tong=0, luot=[]))
    if credit_luot:
        so_credit["tong"] += credit_luot
        so_credit["luot"].append(dict(luc=time.strftime("%Y-%m-%d %H:%M:%S"), credit=credit_luot, khoi=len(moi)))
        ghi_json(d / "credit.json", so_credit)
    print(f"CREDIT: lượt này {credit_luot} · cộng dồn {nn} {so_credit['tong']} ({len(so_credit['luot'])} lượt đọc)")

    # ---- sổ tốc độ đọc: chỉ lần đọc ĐẦU (≥ 50% số khối) của tập + ngôn ngữ — lần đọc lại vài khối không đại diện
    if len(moi) >= len(khoi) / 2:
        kk = {k["id"]: k for k in khoi}
        cps = sum(len(dich[i][1]) for i in moi) / sum(meta[i]["giay"] for i in moi)
        tv = float(T.np.median([meta[i]["giay"] / T.khung_loi(kk[i]["b"] - kk[i]["a"], ch) for i in moi]))
        if T.ghi_so(v.name, nn, cps, tv, len(moi)):
            print(f"  SO TOC DO: ghi {v.name} · {nn} · {cps:.2f} ký tự/giây lời · lời/khung lần đầu {tv:.2f} "
                  f"→ {T.FILE_SO.name}")

    # ---- co giãn — MỘT tốc độ chung cho cả chương (chủ kênh 2026-10-08: tốc độ nhảy từ khối này sang khối kia
    # nghe giật). Tốc độ chương = trung vị lời/khung-lời các khối trong chương. Khối ngắn hơn: đọc đúng tốc độ
    # chương rồi để lặng; khối dài hơn: nén riêng vừa đủ. Khối lệch quá xa → VUOT, agent viết lại.
    gian, nen, tho = float(ch["gian_toi_da"]), float(ch["nen_toi_da"]), float(ch["khong_co_gian"])
    du_lang = float(ch["du_lang_toi_da"])
    ky = T.chu_ky(ch)
    co = {}                              # id -> (khung, khung lời, tỉ lệ)
    for k in khoi:
        m = meta.get(k["id"])
        if m and m.get("bam") == T.bam(dich[k["id"]][1]):
            khung = k["b"] - k["a"]
            kl = T.khung_loi(khung, ch)
            co[k["id"]] = (khung, kl, m["giay"] / kl)
    toc = {}
    for c in sorted({k["chuong"] for k in khoi}):
        r = [co[k["id"]][2] for k in khoi if k["chuong"] == c and k["id"] in co]
        if r:
            toc[c] = T.toc_chuong(r, ch)                  # chương gần khớp sẵn: giữ giọng thô
    bao, vuot = [], []
    for k in khoi:
        if k["id"] not in co:
            vuot.append((k["id"], None, "chưa có voice"))
            continue
        m = meta[k["id"]]
        khung, kl, tl = co[k["id"]]
        tc = toc[k["chuong"]]
        t = max(tc, tl)                                  # ngắn hơn: theo tốc độ chương · dài hơn: nén riêng
        lang = kl - m["giay"] / t                        # lặng dư sau lời (ngoài nghi_cuoi_khoi)
        dong = dict(id=k["id"], khung=round(khung, 3), loi=m["giay"], ti_le=round(tl, 4), toc_chuong=round(tc, 4),
                    toc=round(t, 4))
        if tl > 1 + nen:
            ly = f"lời {m['giay']:.2f}s / khung lời {kl:.2f}s = {tl:.2f} → viết NGẮN lại khoảng {(tl - 1) * 100:.0f}%"
        elif lang > du_lang * kl:
            can = round((1 - du_lang / 2) * kl * tc / m["giay"] * 100 - 100)
            ly = (f"lời {m['giay']:.2f}s ở tốc độ chương {tc:.2f} còn lặng {lang:.1f}s / khung lời {kl:.2f}s "
                  f"→ viết DÀI thêm khoảng {can}%")
        else:
            ly = None
        if ly:
            dong["dat"] = False
            vuot.append((k["id"], tl, ly))
        else:
            out = d / "khop" / f"{k['id']}.wav"
            dau = m["bam"] + ky + f"|{t:.4f}"
            if m.get("khop") != dau or not out.is_file():
                x = T.doc_am(d / "raw" / f"{k['id']}.wav")
                n = int(round(khung * T.SR))
                y = x if t == 1.0 else T.gian(x, m["giay"] / t, ch["co_gian"])
                y = T.np.pad(y, (0, max(0, n - len(y))))[:n]
                T.ghi_am(y, out)
                m["khop"] = dau
            dong["dat"] = True
            dong["giu_tho"] = t == 1.0
        bao.append(dong)
    if toc:
        print(f"{nn}: tốc độ theo chương · " + " · ".join(f"c{c} {t:.2f}" for c, t in sorted(toc.items())))
    ghi_json(d / "meta.json", meta)
    ghi_json(d / "bao_cao.json", bao)

    tl = [b["ti_le"] for b in bao]
    if tl:
        print(f"{nn}: {sum(b['dat'] for b in bao)}/{len(khoi)} khối đạt · tỉ lệ lời/khung {min(tl):.2f}–{max(tl):.2f} "
              f"(ngưỡng {1 - gian:.2f}–{1 + nen:.2f}) · giữ giọng thô {sum(b.get('giu_tho', False) for b in bao)} khối")
    for i, _, ly in vuot:
        print(f"VUOT: {i} · {ly}")
    for x in loi:
        print(f"LOI: {x}")
    return 1 if vuot or loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
`````

### FILE: `scripts/lt_04_tron.py`

`````python
"""Bước 4 — trộn giọng đã khớp với nhạc + SFX của bản gốc, xuất file upload và phụ đề.

Dùng:  python lt_04_tron.py "<thư mục tập>" --ngon-ngu tieng_anh
       python lt_04_tron.py "<thư mục tập>" --tat-ca          # mọi ngôn ngữ đã qua bước 3
Nền:   <V>/_tmp_skill/: <tên V>_nhac.flac + _sfx.flac → nếu thiếu: <tên V>_nen.* (nền trộn sẵn) → không có thì dừng.
Ra:    voice/long_tieng/<tên V>_<ngôn ngữ>.mp3 (giọng + nhạc + SFX) · .srt
       --chi-srt: chỉ làm lại .srt (cắt theo nghĩa, mốc bám khoảng lặng thật của giọng), không trộn lại mp3.
Trộn bằng đúng loc_tron_am() của tron_am.py — y hệt bản gốc.
"""
import argparse, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

import numpy as np

import lt_lib as T

CAU = re.compile(r"(?<=[.?!…。！？؟])\s*")
DAU_NGAT = re.compile(r"[,;:—–、，；：،؛]")      # cắt NGAY SAU các dấu này
TU_TOI_THIEU = 16                               # vế cắt ra ngắn hơn (độ rộng) thì không nhận — tránh mẩu cụt
# Từ không được đứng CUỐI cue / cuối dòng: mạo từ, giới từ, liên từ, loại từ… (gộp mọi ngôn ngữ, chữ thường).
# Đứng cuối là treo một cụm chưa trọn: "một con / tàu", "nếu / dựng đứng lên", "the / ship".
TU_NOI = set("""
một những các của và là nếu khi mà để với cho trong từ đến rằng thì nhưng hay hoặc vì bởi con cái chiếc
đã sẽ đang được bị không rất này nên còn cũng như theo về tới ở trên dưới sau trước
a an the of to in on at for with and or but if that which who whom whose from by as its their his her our
this these those is are was were will would can could has have had not into than when while because so
el la los las un una unos unas de del y o u que en con por para si al su sus lo se e ni sin sobre como
os as um uma uns umas da do das dos em no na nos nas com ao à às pelo pela seu sua mais
le les une des du et ou qui au aux pour avec dans par sur ce cette ces son sa ses leur d' l' qu'
der die das den dem des ein eine einen einem einer und oder dass wenn mit von zu im auf für aus bei nach
ist sind war wird nicht wie als
yang dan di ke dari untuk dengan sebuah seorang jika karena bahwa atau pada oleh akan adalah
في من على إلى أن إذا التي الذي و أو عن مع
""".split())
# Liên từ mở vế mới: cắt NGAY TRƯỚC chúng là chỗ ngắt tự nhiên.
TU_MO = set("và nhưng nếu khi mà rằng vì để and but if when that which because while que pero si cuando porque "
            "mas quando et mais quand und aber wenn weil dass dan tetapi jika ketika karena bahwa".split())
TRO_TU_JA = set("はがをにでとへもや")
TRAN_KHONG_DAU = 130                            # câu không có dấu để cắt: tới mức này vẫn để nguyên một cue
CAT_KHOANG_TRANG = []                           # câu buộc phải cắt ở khoảng trắng — báo cho chủ kênh xem
LANG_TOI_THIEU = 0.12                          # khoảng lặng trong giọng đủ dài để coi là chỗ ngắt (giây)


def rong(s):
    """Độ rộng hiển thị: chữ CJK tính 2."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _tu(s, cuoi=True):
    t = s.split()
    return (t[-1] if cuoi else t[0]).strip("\"'«»“”()[]¿¡").lower() if t else ""


def _diem(s, i, muc):
    """Điểm phạt khi cắt s tại i (nhỏ = tốt): lệch mức cân + treo từ nối; thưởng cắt sau dấu câu / trước liên từ."""
    trai, phai = s[:i].rstrip(), s[i:].lstrip()
    p = 0.5 * abs(rong(trai) - muc)
    if " " in s:
        p += 40 if _tu(trai) in TU_NOI else 0
        p -= 25 if _tu(phai, False) in TU_MO else 0
    else:
        p += 0 if trai[-1:] in TRO_TU_JA else 12
    return p - (12 if DAU_NGAT.search(trai[-1:]) else 0)


def _cho_cat(s):
    return [m.start() for m in re.finditer(" ", s)] if " " in s else list(range(1, len(s)))


def chia_cau(cau, tran):
    """Cắt câu dài thành các cue ≤ tran theo NGHĨA, không theo số chữ (chủ kênh 2026-10-08: "một con / tàu" là gãy).
    1. Có dấu , ; : → cắt ở dấu MUỘN NHẤT mà vế trước còn vừa tran: vế chêm khép trọn trong một cue
       ("dài đến mức, nếu dựng đứng lên, / nó sẽ khiến…" — cắt ở dấu phẩy đầu là treo "đến mức").
    2. Không có dấu phù hợp → cắt ở khoảng trắng gần mức chia đều, phạt nặng khi treo từ nối cuối cue."""
    cau = cau.strip()
    if rong(cau) <= tran:
        return [cau]
    tot = None
    for tr in (tran, TRAN_KHONG_DAU):              # vế trước vừa một cue chuẩn; không được thì nới tới cue dài
        for m in DAU_NGAT.finditer(cau):
            if TU_TOI_THIEU <= rong(cau[:m.end()].strip()) <= tr and rong(cau[m.end():].strip()) >= TU_TOI_THIEU:
                tot = m.end()
        if tot is not None:
            break
    if tot is None and rong(cau) <= TRAN_KHONG_DAU:
        return [cau]                                # hơi dài vẫn hơn cắt giữa cụm từ
    if tot is None:
        n = -(-rong(cau) // tran)
        muc = rong(cau) / n
        ung = [i for i in _cho_cat(cau)
               if TU_TOI_THIEU <= rong(cau[:i]) <= tran and TU_TOI_THIEU <= rong(cau[i:].strip()) <= TRAN_KHONG_DAU * (n - 1)]
        ung = ung or [i for i in _cho_cat(cau) if rong(cau[:i]) <= tran] or [len(cau) // 2]
        tot = min(ung, key=lambda i: _diem(cau, i, muc))
        CAT_KHOANG_TRANG.append(f"{cau[:tot].strip()}  ⟋  {cau[tot:].strip()}")
    return [cau[:tot].strip()] + chia_cau(cau[tot:], tran)


def gap_hai_dong(s, tran=50):
    """Xuống dòng trong cue CHỈ ở dấu câu (, ; :) — hai dòng đều ≤ tran. Không có dấu hợp lệ → để một dòng,
    trình phát YouTube tự xuống dòng theo bề rộng màn hình. Ngắt ở khoảng trắng bằng luật là gãy từ ghép
    ("đánh / chìm", "càng / lớn" — chủ kênh 2026-10-08), máy không phân biệt được nếu không hiểu nghĩa."""
    if rong(s) <= 42:
        return s
    ung = [m.end() for m in DAU_NGAT.finditer(s) if rong(s[:m.end()]) <= tran and rong(s[m.end():].strip()) <= tran]
    if not ung:
        return s
    i = min(ung, key=lambda i: abs(rong(s[:i]) - rong(s) / 2))
    return s[:i].rstrip() + "\n" + s[i:].lstrip()


def _lang(x):
    """Các khoảng lặng bên trong giọng (giây): [(đầu, cuối)]."""
    t, ra, i = T.co_tieng(x), [], 0
    while i < len(t):
        if not t[i]:
            j = i
            while j < len(t) and not t[j]:
                j += 1
            if i > 0 and j < len(t) and (j - i) / T.SR >= LANG_TOI_THIEU:
                ra.append((i / T.SR, j / T.SR))
            i = j
        else:
            i += 1
    return ra


def moc_cue(x, manh):
    """Mốc (giây, tính từ đầu khối) cho từng mảnh phụ đề, bám KHOẢNG LẶNG THẬT trong giọng đã khớp:
    mốc dự kiến theo tỉ lệ chữ → hút về khoảng lặng gần nhất (ưu tiên lặng dài). Không có lặng hợp lệ → giữ mốc tỉ lệ."""
    co = np.flatnonzero(T.co_tieng(x))
    v0, v1 = (co[0] / T.SR, co[-1] / T.SR) if len(co) else (0.0, len(x) / T.SR)
    tong = sum(rong(m) for m in manh) or 1
    lang = [z for z in _lang(x) if v0 < z[0] and z[1] < v1]
    moc, truoc, cd = [v0], v0, 0
    for j, m in enumerate(manh[:-1]):
        cd += rong(m)
        du = v0 + (v1 - v0) * cd / tong
        con = len(manh) - 1 - j                     # số mảnh còn lại sau mốc này
        ung = [z for z in lang if truoc + 0.6 < (z[0] + z[1]) / 2 < v1 - 0.6 * con
               and abs((z[0] + z[1]) / 2 - du) <= max(1.5, 0.3 * (v1 - v0) / len(manh))]
        if ung:
            z = min(ung, key=lambda z: abs((z[0] + z[1]) / 2 - du) - 1.5 * (z[1] - z[0]))
            lang.remove(z)
            du = (z[0] + z[1]) / 2
        moc.append(max(du, truoc + 0.3))
        truoc = moc[-1]
    return moc + [v1 + 0.3]


def lam_srt(khoi, dich, d):
    cue = []
    for k in khoi:
        manh = []
        for c in [x.strip() for x in CAU.split(dich[k["id"]][1]) if x.strip()]:
            manh += chia_cau(c, 84)
        moc = moc_cue(T.doc_am(d / "khop" / f"{k['id']}.wav"), manh)
        cue += [(k["a"] + a, k["a"] + b, gap_hai_dong(m)) for m, a, b in zip(manh, moc, moc[1:])]
    return "\n".join(f"{i}\n{T.gio_srt(a)} --> {T.gio_srt(b)}\n{s}\n" for i, (a, b, s) in enumerate(cue, 1))


def chon_nen(v):
    """Chọn nền âm, theo thứ tự. Mọi file nền nằm NGOÀI CÙNG <V>/_tmp_skill/ — không tìm trong voice/.
    1. _tmp_skill/<V>_nhac.flac (+ _sfx.flac) — nhạc chưa duck → duck theo giọng mới (loc_tron_am).
    2. _tmp_skill/<V>_nen.<flac|wav|mp3|m4a> — nền trộn sẵn (SFX lẫn nhạc ĐÃ duck theo giọng gốc): dùng nguyên làm
       nền, không duck lại, không ghép thêm nhạc (tránh hai lớp nhạc).
    Không có cả hai → dừng.
    Trả dict(kieu, T, nhac, sfx | nen)."""
    goc = v / "_tmp_skill"
    nhac, sfx = goc / f"{v.name}_nhac.flac", goc / f"{v.name}_sfx.flac"
    if nhac.is_file():
        if not sfx.is_file():
            T.dung(f"có {nhac.name} nhưng thiếu {sfx.name} — cách 1 cần cả hai file, xem lại {goc}")
        dai = T.thoi_luong(nhac)
        if abs(T.thoi_luong(sfx) - dai) > 0.1:
            T.dung("nhạc và SFX lệch thời lượng — xuất lại cho bằng nhau (= dài video)")
        print(f"nền âm: {nhac.name} + {sfx.name} (bóp nhạc theo giọng mới)")
        return dict(kieu="nhac", T=dai, nhac=nhac, sfx=sfx)
    nen = [p for p in goc.glob(f"{v.name}_nen.*") if p.suffix.lower() in (".flac", ".wav", ".mp3", ".m4a")]
    if len(nen) > 1:
        T.dung(f"có nhiều file nền {[p.name for p in nen]} — giữ đúng một")
    if nen:
        print(f"nền âm: {nen[0].name} (nền tách sẵn, dùng nguyên — không bóp lại, không ghép thêm nhạc)")
        return dict(kieu="nen", T=T.thoi_luong(nen[0]), nen=nen[0])

    T.dung(f"chưa có nền âm trong {goc}: đặt {v.name}_nhac.flac + {v.name}_sfx.flac, hoặc {v.name}_nen.flac "
           f"(dài đúng bằng video) rồi chạy lại — xem quy-tac.md §3")


def loc_nen_tach(T_, sr, lufs):
    """Giọng mới + nền tách sẵn (nhạc đã bóp theo giọng gốc). Cùng fade + loudnorm với loc_tron_am, bỏ sidechain."""
    return [f"[0:a]atrim=0:{T_:.3f},asetpts=PTS-STARTPTS,aresample={sr},afade=t=out:st={T_ - 0.5:.3f}:d=0.5[vo]",
            f"[1:a]aresample={sr}[nn]",
            f"[vo][nn]amix=inputs=2:normalize=0:duration=first,afade=t=out:st={T_ - 0.6:.3f}:d=0.6,"
            f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample={sr}[a]"]


def kiem_xong(v, nn, ch, khoi):
    d = T.tm(v) / nn
    dich = T.doc_dich(T.file_dich(v, nn))
    bao = json.loads((d / "bao_cao.json").read_text(encoding="utf-8")) if (d / "bao_cao.json").is_file() else []
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").is_file() else {}
    chua = [k["id"] for k in khoi
            if not str(meta.get(k["id"], {}).get("khop", "")).startswith(T.bam(dich[k["id"]][1]) + T.chu_ky(ch) + "|")]
    if len(bao) != len(khoi) or not all(b["dat"] for b in bao) or chua:
        T.dung(f"{nn}: bước 3 chưa đạt hết — khối chưa khớp: {chua[:10]}. Chạy lt_03_doc_khop.py tới khi không còn VUOT")


def tron(v, nn, ch, khoi, nen):
    d = T.tm(v) / nn
    dich = T.doc_dich(T.file_dich(v, nn))

    dai = nen["T"]
    g = np.zeros(int(round(dai * T.SR)), np.float32)
    for k in khoi:
        x = T.doc_am(d / "khop" / f"{k['id']}.wav")
        i = int(round(k["a"] * T.SR))
        g[i:i + len(x)] += x[:max(0, len(g) - i)]
    giong = d / "giong_khop.wav"
    T.ghi_am(g, giong)

    L = T.tron_am()
    out = T.ten_ra(v, nn, ".mp3")
    out.parent.mkdir(parents=True, exist_ok=True)
    if nen["kieu"] == "nhac":
        # sidechain nhạc theo GIỌNG MỚI, đúng như bản gốc sidechain theo giọng gốc
        vao = ["-i", str(nen["nhac"]), "-i", str(nen["sfx"])]
        loc = ";".join(L.loc_tron_am(dai, T.SR, "[0:a]", "[1:a]", "[2:a]"))
    else:
        vao = ["-i", str(nen["nen"])]
        loc = ";".join(loc_nen_tach(dai, T.SR, L.LUFS_RA))
    subprocess.run([L.FF, "-v", "error", "-y", "-i", str(giong), *vao,
                    "-filter_complex", loc, "-map", "[a]", "-t", f"{dai:.3f}", "-c:a", "libmp3lame",
                    "-b:a", ch["bitrate_ra"], str(out)], check=True)
    T.ten_ra(v, nn, ".srt").write_text(lam_srt(khoi, dich, d),encoding="utf-8")

    o = subprocess.run([L.FF, "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    lufs = [l for l in o.splitlines() if l.strip().startswith("I:")]
    dai_ra = T.thoi_luong(out)
    canh = "" if abs(dai_ra - dai) <= 0.1 else f"  ⚠️ lệch video {dai_ra - dai:+.2f} s"
    print(f"✓ {out.name} · {dai_ra:.2f} s (video {dai:.2f} s) · {lufs[-1].split()[1] if lufs else '?'} LUFS{canh}")
    print(f"✓ {T.ten_ra(v, nn, '.srt').name}")
    bao_cat_khoang_trang()
    return not canh


def bao_cat_khoang_trang():
    if CAT_KHOANG_TRANG:
        print(f"⚠️  {len(CAT_KHOANG_TRANG)} câu dài không có dấu phẩy, phụ đề phải cắt ở khoảng trắng — nên xem lại:")
        for c in CAT_KHOANG_TRANG:
            print(f"   · {c}")
    CAT_KHOANG_TRANG.clear()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ngon-ngu")
    g.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--chi-srt", action="store_true", help="chỉ làm lại phụ đề .srt, không trộn lại mp3")
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    khoi = T.doc_khoi(v)
    ds = [nn for nn in ch["ds_ngon_ngu"] if (T.tm(v) / nn / "bao_cao.json").is_file()] if a.tat_ca else [a.ngon_ngu]
    if not ds:
        T.dung("chưa ngôn ngữ nào qua bước 3")
    for nn in ds:            # kiểm đủ mọi ngôn ngữ trước khi tốn công ghép nền
        kiem_xong(v, nn, ch, khoi)
    if a.chi_srt:
        for nn in ds:
            srt = lam_srt(khoi, T.doc_dich(T.file_dich(v, nn)), T.tm(v) / nn)
            T.ten_ra(v, nn, ".srt").write_text(srt, encoding="utf-8")
            print(f"✓ {T.ten_ra(v, nn, '.srt').name}")
            bao_cat_khoang_trang()
        return 0
    nen = chon_nen(v)
    ok = all([tron(v, nn, ch, khoi, nen) for nn in ds])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
`````

---

*Hết gói. Đủ 10 file. Sau khi tạo xong, làm tiếp mục A bước 3–6.*
