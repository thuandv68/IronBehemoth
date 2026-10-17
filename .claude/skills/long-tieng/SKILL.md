---
name: long-tieng
description: Lồng tiếng một tập video sang nhiều ngôn ngữ để upload làm track âm thanh đa ngôn ngữ trên YouTube (không dùng auto-dub). Mặc định 8 ngôn ngữ (Tây Ban Nha, Bồ Đào Nha BR, Indonesia, Ả Rập, Nhật, Pháp, Đức, Việt). Chia kịch bản thành khối nghĩa 15–25 giây theo SRT gốc, mỗi ngôn ngữ một agent dịch song song, đọc ai33 bằng giọng của kênh, khớp từng khối về đúng khung giờ gốc bằng atempo với một tốc độ chung cho cả chương, lệch ≤ 5% giữ giọng thô (khối vượt ngưỡng thì agent tự viết lại và đọc lại riêng khối đó), rồi trộn với nhạc + SFX gốc, ra mp3 320 kbps dài bằng video, kèm phụ đề SRT, tiêu đề và mô tả đã dịch. Dùng khi user nói "lồng tiếng", "dub", "làm bản lồng tiếng", "làm track âm thanh đa ngôn ngữ", hoặc gửi thư mục tập kèm ý muốn lồng tiếng.
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
4. Key ai33 của Aron nằm ở `<thư mục IronBehemoth>/.secrets/ai33.env` (dòng `AI33_API_KEY=...`). Khi chạy `lt_03` đặt
   `TTS_SECRETS="<thư mục IronBehemoth>/.secrets/ai33.env"` trước lệnh. ⛔ Không chép key sang chỗ khác, không in key.

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
