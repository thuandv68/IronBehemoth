---
title: Quy tắc lồng tiếng
skill: long-tieng
# --- Thông số — script long-tieng/scripts/ đọc đúng các dòng này, giữ dạng "khoá: giá trị" ---
# ngon_ngu: <tên file>=<mã ngôn ngữ>=<tên hiển thị>, ngăn bằng dấu chấm phẩy.
ngon_ngu: tieng_tay_ban_nha=es=Spanish;tieng_bo_dao_nha_br=pt-BR=Portuguese (Brazil);tieng_indonesia=id=Indonesian;tieng_a_rap=ar=Arabic;tieng_nhat=ja=Japanese;tieng_phap=fr=French;tieng_duc=de=German;tieng_viet=vi=Vietnamese
# ngon_ngu_thu: ngôn ngữ chỉ để nghe thử (script nhận, nhưng KHÔNG chạy trong lượt chính), cùng dạng với ngon_ngu.
ngon_ngu_thu:
# --- giọng đọc ai33 (dùng cho mọi ngôn ngữ) ---
tts_provider: ai33
# voice_id: ĐIỀN id giọng của bạn trên ai33 (ví dụ clone_1234567). Để nguyên <...> thì script dừng.
voice_id: elevenlabs_t0eCaS57KWbQQc1wRkah
speed: 1.0
pronunciation_dictionary_id:
# --- tiêu đề + mô tả: số lần cụm từ khoá chính phải lặp trong phần văn mô tả (§7). 0 = không kiểm luật từ khoá.
so_lan_tu_khoa: 0
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
| Tây Ban Nha | `tieng_tay_ban_nha` | `es` |
| Bồ Đào Nha (Brazil) | `tieng_bo_dao_nha_br` | `pt-BR` |
| Indonesia | `tieng_indonesia` | `id` |
| Ả Rập | `tieng_a_rap` | `ar` |
| Nhật | `tieng_nhat` | `ja` |
| Pháp | `tieng_phap` | `fr` |
| Đức | `tieng_duc` | `de` |
| Việt | `tieng_viet` | `vi` |

Thêm / bớt ngôn ngữ: sửa khoá `ngon_ngu` ở frontmatter (giữ dạng `tên_file=mã=tên hiển thị`, tên file viết
`tieng_<...>`). Ngôn ngữ trùng với ngôn ngữ gốc của video thì bỏ ra. Các kênh của Aron đọc gốc tiếng Anh nên bộ này bỏ tiếng Anh, thêm tiếng Tây Ban Nha (2026-10-16).

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
