---
name: ib-assets
description: Chia beat kịch bản IronBehemoth và xuất file CSV tài nguyên theo mẫu raw/assets/mau_beat.csv (veo3/footage/image, prompt, từ khóa, avoid) để anh Aron tự đi tìm/tạo tài nguyên.
---

# ib-assets — CSV tài nguyên (bước 2/3)

Đầu vào: `IronBehemoth-Videos/NNN_slug/script.md` (đã qua `ib-script`). Đầu ra duy nhất: `IronBehemoth-Videos/NNN_slug/beats/beats_NNN_slug.csv`. **Không tự đi tìm/tải tài nguyên** — anh Aron tự tìm và điền `provider`, `path`. Báo tiến độ ngắn bằng tiếng Việt.
Tool: `IronBehemoth-Videos/tools/video/ib_beats.py` (chạy được ngay trên device shell, không cần mạng). Mẫu: `IronBehemoth-Videos/tools/video/templates/locks.json`.

## 1. Chọn công cụ tạo video AI → độ dài beat
- Veo 3 / Google Flow: clip 8 giây → `--clip 8` (tối đa ~19–20 từ/beat).
- Muse: clip 10 giây → `--clip 10` (tối đa ~24 từ/beat).
- Anh chưa nói dùng gì → hỏi một câu; không trả lời thì mặc định 8. Prompt trong CSV tự ghi "single continuous 8-second take" hoặc "10-second".

## 2. Chia beat
```
cd $HOME/mnt/IronBehemoth
python3 IronBehemoth-Videos/tools/video/ib_beats.py split IronBehemoth-Videos/NNN_slug --clip 8
```
→ `beats/beats.tsv` (Bxxx, số từ, lời đọc) + `beats/meta.json`. Câu dưới 6 từ gộp vào beat kề, câu dài tách ở dấu phẩy. Báo số beat, số từ, thời lượng ước tính.

## 3. Khóa hình ảnh `beats/locks.json`
Chép từ `IronBehemoth-Videos/tools/video/templates/locks.json`, sửa cho xe của tập:
- `TANK`: mô tả hình dạng xe thật chi tiết (khung gầm, bánh, tháp pháo hay casemate, nòng, vị trí đặc trưng, màu sơn, chỉ chữ thập Balkenkreuz nhỏ / sao trắng Mỹ…) lấy từ `wiki/tanks/<xe>.md` và ảnh bảo tàng. Veo hay vẽ sai xe: khóa càng cụ thể càng tốt (ghi rõ "NO turret" nếu không có tháp pháo).
- `CREW`: quân phục kíp lái đúng phe, năm; nhìn nghiêng/sau lưng.
- `STYLE`: giữ phong cách kênh (phim tài liệu WWII photoreal, mùa/năm của tập, hạt phim 35mm, không chữ, không logo, không chữ vạn, không nhìn thẳng camera).
- `AVOID_*`: dạng "no …" như mẫu.
- **Bài học tập 002:** Muse bỏ qua cột avoid và vẽ theo tên gọi. Trong prompt veo3 KHÔNG ghi tên xe hay tên khung gầm gốc ("Sturmtiger", "Tiger I chassis" → Muse vẽ ra Tiger có tháp pháo). Tả bằng hình dạng ("turretless siege mortar, boxy casemate, very short fat tube") và đặt câu phủ định ngay trong khóa TANK ("Absolutely no turret, no long barrel"). STYLE luôn có "no emblems, insignia or labels on any equipment" (Muse tự vẽ chữ vạn lên nhãn thiết bị). Luôn đính ảnh tham chiếu xe thật. Không dùng từ phủ định về bộ phận xe trong prompt ("no turret", "no long barrel"): AI tạo video đọc thấy chữ turret/barrel sẽ vẽ ra đúng thứ đó. Chỉ tả hình dạng bằng câu khẳng định. Tập 002: Muse chỉ bằng chữ vẫn vẽ sai Sturmtiger, nên mọi beat có khóa VEHICLE phải tạo từ ảnh (image-to-video) với ảnh tham chiếu trong `IronBehemoth-Videos/NNN_slug/ref/`. Gán ảnh cho từng beat bằng khóa `"ref": "ref/<file>.png"` trong beatmap; CSV giữ đúng 10 cột mẫu, không thêm cột hay file phụ; góc ảnh ref chỉ thể hiện trong prompt (câu "View as in the reference photo…"). Chọn ảnh theo góc máy: cận cảnh/chính diện → ảnh chính diện, tracking ngang → ảnh ngang hông, orbit → ảnh 3/4. Muse (Meta AI): tải ảnh vào ô lệnh rồi dán prompt.

- **Bài học tập 003:** mô tả xe theo đúng góc của ảnh ref. `locks.json` có `TANK_BY_REF` (mỗi ảnh ref một khóa: câu "View as in the reference photo…" + thân/tháp/nòng/sơn/tỉ lệ theo thứ tự cố định), `PARTS` cho cảnh chỉ thấy một phần xe (gán `"part"` trong beatmap: nóc xe, tháp rời, thân không tháp, hai xe giống nhau). Mọi bổ sung chỉ nằm trong nội dung prompt; CSV chỉ được có đúng các cột của `raw/assets/mau_beat.csv`. Không để ghi chú dựng ("overlay", "later") lọt vào `desc` của veo3.

- **Từ tập 006 (anh Aron chọn dựng theo kiểu Blue Paw Print):** hook và trận đánh dùng cảnh điện ảnh gây cấn (khói, lửa đầu nòng, đạn nảy khỏi giáp, kíp lái bỏ xe); các beat giải thích kỹ thuật dùng `"style": "3d"` trong beatmap → prompt lấy `STYLE_3D` của locks (mô hình 3D đứng một mình trên sàn xám bóng phản chiếu, nền thị trấn đổ nát mờ, x-ray giáp chuyển cyan trong suốt để lộ kíp lái/đạn/động cơ, exploded view, linh kiện xoay trên nền đen, đường đo kích thước trắng). Chữ/số đo thêm ở bước đồ họa, không để AI vẽ.

## 3b. Nguyên tắc bắt buộc: đúng xe
Lời đọc nói về xe nào thì hình phải là đúng xe đó. Không lấy xe khác "trông giống" để thế chỗ.
- Beat nói về xe của tập: chỉ dùng **image** có tên xe (ảnh thật, bảo tàng, Bundesarchiv), hoặc **veo3** có khóa TANK kèm ảnh tham chiếu. Không dùng **footage** stock, vì kho stock không có xe này.
- **footage** chỉ dùng cho cảnh không có xe (thời tiết, phố đổ nát, đồng hồ, biển, giấy tờ). Cột avoid của footage luôn có "no tanks or military vehicles".
- Beat nói về xe khác (xe gốc, đối thủ, tập trước) thì ghi rõ tên xe đó và đặt `avoid` riêng trong beatmap: "must be a real X, not <xe của tập>".
- Avoid của ảnh xe tập: "must be a real <xe>, not <các xe dễ nhầm>, no scale models, no game renders".
- QC: đọc từng dòng, so sánh xe trong hình với xe trong lời đọc.

## 4. Gán loại + mô tả từng beat `beats/beatmap.json`
`{"B001": {"type": "veo3|footage|image", "desc": "cảnh nhìn thấy được, tiếng Anh", "camera": "Slow push-in at one steady speed"}}`
- Tỉ lệ tham khảo theo `mau_beat.csv`: ~65% veo3, ~20% footage, ~15% image. Không quá 3 beat liên tiếp cùng loại (tool cảnh báo).
- **veo3**: cảnh riêng của xe/kíp lái/chiến trường mà kho stock không có. `desc` = một cảnh cụ thể, một hành động, khớp lời đọc; không tả bạo lực lên người (Flow chặn "shells strike", "machine guns firing" → dùng "a round streaks…", "a blast bursts from the building"). `camera` một chuyển động (push-in, slow orbit, locked-off, low tracking, high drone glide).
- **footage** (Pexels/Envato): từ khóa ngắn 3–8 từ tả cái nhìn thấy, không tên riêng của xe (ví dụ "snowy forest road winter dusk", "blacksmith hot metal sparks").
- **image**: ảnh tư liệu/bảo tàng (Wikimedia, US Army, Bundesarchiv) — được ghi tên xe, nơi, năm ("Sturmtiger at Deutsches Panzermuseum Munster").
- Beat có con số lớn/thông số → ghi chú trong `desc` để dựng đồ họa sau (ví dụ veo3 cận cảnh vật thể + overlay số).

## 5. Xuất CSV
```
python3 IronBehemoth-Videos/tools/video/ib_beats.py csv IronBehemoth-Videos/NNN_slug NNN_slug
```
Cột đúng mẫu `raw/assets/mau_beat.csv`: `beat_id, asset_id (B001_A001), itemType, visual_query, min_media_length, max_media_length, avoid, script, provider, path` (UTF-8 BOM). `provider`, `path` để trống. Footage: min 8 / max 15 giây.

## 6. QC CSV trước khi giao
- Số dòng = số beat; mọi `visual_query` khác rỗng; không có "swastika" ngoài cột avoid; không tên xe trong từ khóa footage; prompt veo3 có khóa TANK khi có xe.
- Đọc lướt 10 prompt veo3 ngẫu nhiên: cảnh khớp lời đọc, không bạo lực lên người, đúng hình xe.
- Gợi ý thêm 2–3 ảnh tham chiếu xe thật (Wikimedia) cho các beat có xe, liệt kê ở cuối tin nhắn: với Flow nên đính ảnh tham chiếu vào phần "Thành phần" để Veo vẽ đúng xe (cách tải ảnh lên: `IronBehemoth-Videos/tools/video/BROWSER_SNIPPETS.md`).

## 7. Giao
- Gửi file CSV (SendUserFile) + đường dẫn trên máy. Báo: số beat, số veo3/footage/image, thời lượng ước tính, công cụ (8s/10s).
- Nhắc quy ước để `ib-build` tự nhận file: đặt tài nguyên vào `IronBehemoth-Videos/NNN_slug/beats/footage/` với tên bắt đầu bằng `asset_id` (`B001_A001.mp4`, `B002_A002-pexels-123.jpeg`) hoặc điền đường dẫn vào cột `path`; `provider` ghi `muse`, `flow`, `pexels`, `envato`, `wikimedia`… (clip `flow` sẽ được xóa ngôi sao watermark, `muse` thì không).
- Ghi một dòng vào `log.md`. Bước tiếp theo: anh tìm đủ tài nguyên rồi chạy `ib-build`.
