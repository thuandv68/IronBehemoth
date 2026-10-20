# Log

## [2026-10-11] setup | Tạo khung LLM Wiki
- Tạo raw/, wiki/, outputs/, .claude/skills/, CLAUDE.md, index.md, log.md.

## [2026-10-11] ingest | Thông tin nền tảng kênh
- Nguồn: raw/competitors/2026-10-11_blue-paw-print-inside-series.md, raw/references/2026-10-11_llm-wiki-pattern.md, raw/references/2026-10-11_owner-decisions.md.
- Viết schema CLAUDE.md.
- Tạo 18 trang wiki: [[overview]], [[brand]], [[audience]], [[episode-template]], [[title-formula]], [[thumbnail-formula]], [[hook-and-description]], [[script-style]], [[pipeline]], [[visual-locks]], [[beat-plan]], [[footage-sources]], [[topic-backlog]], [[release-and-growth]], [[risks-and-compliance]], [[performance-tracker]], [[blue-paw-print]], [[landscape]].
- Tạo skill dự án ib-episode, ib-wiki.
- Việc mở: kiểm tra 38 video Blue Paw Print trước khi chốt tập 001.

## [2026-10-11] query | Xác nhận handle
- @IronBehemoth, @IronBehemothTV, @IronBehemothHQ, @Iron_Behemoth, @TheIronBehemoth đều 404 → còn trống. Không có kênh trùng tên trong tìm kiếm YouTube.
- Cập nhật [[brand]].

## [2026-10-11] ingest | Keyword vidIQ + hồ sơ thiết lập kênh
- Nguồn: raw/keywords/2026-10-11_vidiq-keyword-research.md (12 seed tra trên vidIQ).
- Tạo [[channel-setup]]: About, 20 channel keywords 5K–50K, logo, banner, watermark, upload defaults, playlist, checklist.

## [2026-10-11] ingest | Thông số giọng đọc
- Đo tốc độ và loudness 2 video Blue Paw Print trong raw/assets/video-doi-thu.
- Tạo [[voice-spec]]. Không clone giọng người dẫn đối thủ.

## [2026-10-11] query | Thử giọng ai33
- Tạo 4 mẫu giọng (Leo, Spartan, Russ, Grant Gravitas) bằng hook Tiger I, cập nhật [[voice-spec]].

## [2026-10-11] setup | Tạo skill kịch bản 16–20 phút
- Tạo `.claude/skills/ib-episode/SKILL.md` theo format "Inside the [Xe]" cho kênh IronBehemoth.
- Skill bao gồm: mô hình 10 phần, quy tắc nhịp kể chuyện, dạng câu mở, mẫu chuyển chương, checklist trước khi dựng, và ví dụ áp dụng cho King Tiger.

## [2026-10-11] ingest | Format kịch bản Ingeniería Monumental
- Nguồn: raw/assets/fm/ (8 script + trailer).
- Tạo [[script-dna-ingenieria-monumental]]; liên kết [[script-style]], [[episode-template]].

## [2026-10-11] produce | 001 Inside the King Tiger — script
- Viết script 2.435 từ theo format Ingeniería Monumental; nguồn dữ kiện: script đối thủ + sách Jentz/Doyle, Schneider.
- Tạo [[king-tiger]]; cập nhật [[topic-backlog]].

## [2026-10-11] produce | 001 demo video 3:42
- Voice ai33 (Russ, speed 0.85, atempo 0.93), nhạc YT Audio Library "Kayak" (The Grey Room / Density & Time), SFX YT Audio Library + ai33 sound-effect, ảnh Wikimedia (xem demo/shotlist.md), footage Pexels 10161606/15041333/15341182, 4 clip AI Muse.
- Dựng ffmpeg (demo/tools/build.py), -14.7 LUFS, TP -1.1 dBFS. File: outputs/001_king-tiger/demo/IB001_demo_1080p.mp4

## [2026-10-11] produce | 001 demo v2
- Đoạn thông tin kênh dùng banner assets/branding, grade sáng hơn, thêm thanh Subscribe/Like động (logo + nút + con trỏ + tiếng click) theo phong cách Ingeniería Monumental.
- File: outputs/001_king-tiger/demo/IB001_demo_v2_1080p.mp4

## [2026-10-11] produce | 001 demo bản tiếng Việt
- Dịch 33 câu (demo/script_vi.txt), giọng vbee Anh Khôi nâng cao (ai33), canh thời gian theo word timestamps, đồ họa + thanh Đăng ký/Thích tiếng Việt (Oswald/Roboto).
- File: outputs/001_king-tiger/demo/IB001_demo_vi_1080p.mp4 (2:54)

## [2026-10-11] ingest | Mở rộng mô tả kênh khỏi ngách xe tăng
- About viết lại: câu đầu là thương hiệu mẹ "inside the machines that shape warfare", xe tăng là series khởi đầu, nêu hướng tên lửa/pháo/máy bay/tàu chiến; ~880 ký tự. Đồng bộ [[brand]] và [[channel-setup]].
- Upload defaults: lời kêu gọi subscribe đổi sang "Iron Behemoth documentary"; thêm ghi chú mở rộng keyword và playlist series mới.
- trang bị ảnh hưởng: [[brand]], [[channel-setup]]

## [2026-10-11] ingest | youtube-suite + beat CSV 001
- Đọc youtube-suite (ARCHITECTURE, footage/generation docs, examples). Tạo [[beat-csv-youtube-suite]].
- Xuất outputs/001_king-tiger/beats/beats_001_*.csv (173 beat: 114 veo3, 45 footage, 14 image).

## [2026-10-11] ingest | Rút gọn About, thêm disclaimer
- About ~970 ký tự (≤ 1.000), gộp câu visuals/specifications vào disclaimer "⚠️ Disclaimer: …"; giữ nguyên keyword SEO.
- trang bị ảnh hưởng: [[brand]], [[channel-setup]]

## [2026-10-11] produce | 001 King Tiger, full 1080p
- Built from beats/beats_001_king-tiger.csv (173 beats → 169 shots; B018–B020, B104–B105 and B166–B167 merged), with timing from the Russ voice word timestamps (atempo 0.93).
- Output: outputs/001_king-tiger/full/IB001_King_Tiger_1080p.mp4, 16:41, −15 LUFS, true peak −1.3 dBFS.
- Visuals: 28 Wikimedia images, 18 Pexels clips, 4 Muse clips, 8 chapter cards and 15 stat overlays, plus the reticle, fuel-consumption chart, FUEL card, next-episode card, and banner with subscribe bar ×2. Credits are in full/credits.md.
- Re-rendering: when youtube-suite fills the CSV `path` column, build_full.py uses that file for the beat. The beat-to-visual map is in full/tools/shotmap.txt.
- Open items: veo3 beats still use stand-in images; the music is a single track ("Kayak") looped with crossfades; full/parts/ can be deleted.

## [2026-10-12] produce | 001 King Tiger, v2 with AI footage
- Added 80 of the 107 AI clips from beats/footage (youtube-suite, veo3 beats) to the video, with a separate, brighter colour grade for them.
- QC rejected 18 AI clips: swastika markings, Soviet stars, or off-topic (Shermans). The list is in full/credits.md; those beats keep their old images or footage.
- The 7 veo3 beats that had no clip were filled with Pexels footage: B050 field fire, B061 shooting range, B076 cartridges, B089 man by a fire in the snow, B103 vehicle in mud, B108 forest smoke, B114 hot metal. B123 keeps the Tiger II wheel photo.
- Music: "Kayak" and "Rapid Unscheduled Disassembly" (The Grey Room / Density & Time), crossfaded.
- Output: full/IB001_King_Tiger_1080p_v2.mp4, 16:41, −15 LUFS, true peak −1.3 dBFS.

## [2026-10-12] review + produce | 001 King Tiger v3
- Script went through the review board, YouTube policy audit and fact-check (review_001.md). 5 sentences fixed: date 23–24/12, penetration ≈185 mm at 500 m, 80–86 shells, steering wheel, gearbox. script.md is now the final version.
- New voice: ai33 Russ, 921 s; beats re-aligned (0 mismatched beats). Overlays fixed: ≈185 MM, 80–86 SHELLS.
- Output: full/IB001_King_Tiger_1080p_v3.mp4, 16:33, −14.9 LUFS, true peak −1.4 dBFS.
- QC of the 3D crew clips: _A02 all rejected (live-action people, off-topic). _A03 has the right x-ray style but the tank shape is not a King Tiger (resembles an IS-2/ISU), B026 has a Soviet star, B023 shows 6 crew, B028 has the loader standing outside the tank. The 2D diagram stays.

## 2026-10-13 — 001 King Tiger v4
- Subscribe at 01:53: background is now footage (B018 kt_lg24, B019/B020 AI clips) instead of the banner; channel bar centered at the bottom; Like button removed; one mouse click on Subscribe, then the bell pops in and rings (sfx_bell.mp3).
- Output: outputs/001_king-tiger/full/IB001_King_Tiger_1080p_v4.mp4 (16:33, 1080p, −14.9 LUFS, peak −1.2 dBFS).
- tools/video/make_subscribe.py, build_full.py and common/sfx/sfx_bell.mp3 updated.
- Ending subscribe (B166–B167, ~15:4x) still uses the banner background with the new bar.

## 2026-10-13 — 001 King Tiger v5
- Ending subscribe now matches 01:53: B166 kt_lg05 still, B167 AI clip (camera into the turret hatch) with the centered channel bar, one click + bell. Banner background removed.
- Output: outputs/001_king-tiger/full/IB001_King_Tiger_1080p_v5.mp4 (16:33, 1080p, −14.9 LUFS, peak −1.2 dBFS). Rule for future episodes: subscribe CTAs always sit over footage, never over the banner.

## 2026-10-13 — 001 King Tiger v6
- Subscribe SFX: replaced the multi-click mouse sound with one synthesized click (common/sfx/sfx_click_single.mp3); removed the pop sounds; bell kept. Output IB001_King_Tiger_1080p_v6.mp4 (−14.9 LUFS, peak −1.3 dBFS).
- FINAL: IB001_King_Tiger_FINAL_1080p.mp4 = v6 (approved 2026-10-13). ib-episode skill updated with review/audit/fact-check and Phase 7–8 build rules.

## 2026-10-13 — 001 King Tiger v7 (FINAL)
- Removed the next-video teaser (B168–B173, Abrams) since episode 002 is not made yet; voice now ends on "…what really kept these machines alive." script.md trimmed (old version: script_v2_with_teaser.md); chapter "Next: Inside the M1A2 Abrams" removed from keywords_001.md.
- New 12 s animated end card (tools/video/make_endcard.py, background common/endcard_bg.png = banner with logo/text removed): logo spin-in + ring pulse, wordmark wipe, orange underline draw, tagline type-in, logo shine, subscribe bar with one click + bell at +4 s, fade to black. build_full.py: --end-at <beat> cuts the voice, END shot = seqv:endcard.
- Output IB001_King_Tiger_1080p_v7.mp4 = IB001_King_Tiger_FINAL_1080p.mp4 (16:04, −14.9 LUFS, peak −1.3 dBFS).

## 2026-10-13 — 001 King Tiger v8 (FINAL)
- End card merged with the final CTA: from "And subscribe…" (B167) the animated end card runs under the voice with one subscribe bar (click + bell), then holds 10 s after the voice. Logo/name and subscribe appear only once at the end. Output IB001_King_Tiger_1080p_v8.mp4 = FINAL (16:01).
- Cleanup: deleted versions v1–v8 and parts* folders in outputs/001_king-tiger/full (~10 GB). Kept FINAL, credits.md, pexels_extra/, tools/ and beats/footage/.

## [2026-10-14] setup | Đóng gói 3 skill sản xuất chính thức
- ib-script (viết kịch bản từ tiêu đề + kịch bản mẫu), ib-assets (chia beat + CSV theo raw/assets/mau_beat.csv), ib-build (dựng từ CSV, thiếu tài nguyên thì dừng).
- Tool dùng chung mới trong tools/video/, chạy thử trên dữ liệu 002 (27 beat, 99,4% khớp voice, −15,9 LUFS). Tool cũ của 001 → tools/video/legacy_001/.
- Key ai33 lưu cục bộ .secrets/ai33.env (gitignore).
- trang bị ảnh hưởng: [[pipeline]]

## [2026-10-14] produce | 002 Sturmtiger: viết lại theo tiêu đề "One Shot, One Building, Ten Minutes to Reload"
- ib-script: analysis_002.md (phân tích đối thủ), script.md 2.449 từ (~16:33), review_002.md (board, chính sách, fact-check, QC), notes.md.
- Xương sống mới: đồng hồ 10 phút nạp đạn; nguồn mới: US Ordnance Technical Intelligence Report 192.
- Bản cũ 2026-10-13 lưu ở outputs/002_sturmtiger/_v1_2026-10-13/.

## [2026-10-14] assets | 002 Sturmtiger CSV (Muse 10s)
- ib-assets: 180 beat, 116 veo3 / 30 footage / 34 image, ~16:24. File: outputs/002_sturmtiger/beats/beats_002_sturmtiger.csv
- 2026-10-14: sửa khóa TANK (bỏ chữ Tiger, tả hình hộp không tháp pháo, nhét câu phủ định vào prompt) sau khi clip Muse B008 ra xe Tiger có tháp pháo; thêm "no emblems/labels" sau khi B009 có chữ vạn trên bình cứu hỏa
- 2026-10-14: rà "đúng xe" toàn bộ 180 beat, đổi 13 beat (footage xe chung → ảnh Sturmtiger thật; footage tên lửa hiện đại → ảnh đạn 38 cm), avoid riêng cho beat xe khác; thêm mục 3b vào skill ib-assets
- 2026-10-14: Muse vẫn vẽ sai xe (B005 ra pháo chống tăng nòng dài, B012 ra Elefant). Viết lại khóa TANK chỉ bằng câu khẳng định, bỏ chữ turret/barrel/gun trong prompt xe; lấy 4 ảnh tham chiếu đúng xe từ demo Flow vào ref/
- 2026-10-14: thêm cột ref_image vào CSV 002 (50 beat có xe), 4 ảnh ref trong outputs/002_sturmtiger/ref/
- 2026-10-14: theo yêu cầu, xóa 9 clip Muse cũ trong outputs/002_sturmtiger/footage (tạo bằng prompt cũ, sai xe)
- 2026-10-14: duyệt tài nguyên 002: loại 50 (7 Muse, 35 ảnh, 8 stock), thiếu B015; file loại chuyển vào footage/_reject, xóa path trong CSV. Biên bản: review_assets_002.md
- 2026-10-14: theo yêu cầu, xóa 50 file bị loại (+ảnh thu nhỏ); viết lại 51 beat (50 veo3 Muse, 1 stock) → beats_002_sturmtiger_redo.csv
- 2026-10-14: lấp 10 beat thiếu bằng tài nguyên của kênh (demo Flow 002, clip King Tiger 001, cắt đôi clip Muse B033/B043/B169, thẻ đồ họa B166). Không dùng hình video đối thủ (3D của họ, rủi ro bản quyền)
- 2026-10-14: duyệt lần 2 tài nguyên 002: đủ 180/180, cắt B024/B109/B069, thay tạm B038 bằng B037; sẵn sàng ib-build
- 2026-10-15: thay 12 beat có chữ vạn/sai xe (5 clip Flow mới đã xóa watermark Veo, 7 beat dùng đoạn sạch của clip khác); check 180/180; tạo 29 đồ họa (build/gfx.txt), build/ib.json. Dừng ở bước voice: hệ thống chặn dùng API key ai33 từ trình duyệt/máy chủ, chờ anh quyết
- 2026-10-15: voice ai33 xong (15:30, khớp 98%); 7 clip Flow Pro (có ảnh tham chiếu) thay B042/B043/B095/B102/B103/B151/B154/B162, sạch
- 2026-10-15: ib-build xong 002: full/IB002_Sturmtiger_1080p.mp4 (16:09, 1080p, -15.9 LUFS, peak -2.6 dBFS, không khung đen). Nhạc "Sagas" (YouTube Audio Library). Chapters cập nhật trong notes.md, credits.md

## [2026-10-15] produce | 003 Maus: "Life Inside the Maus: The World's Heaviest Tank Ever Built"
- ib-script: analysis_003.md (đọc phụ đề Blue Paw Print trực tuyến, không tải/không lưu bản chép), script.md 2.448 từ (~16:32), review_003.md (board, chính sách, fact-check, QC), notes.md.
- Xương sống: xe không súng nào bắn thủng, bị chính kíp lái phá; open loop Kubinka ghép 2 xe.
- trang bị ảnh hưởng: [[maus]] · [[topic-backlog]] · index.md

## [2026-10-15] assets | 003 Maus CSV (Muse/Flow 10s)
- ib-assets: 184 beat, 111 veo3 / 35 footage / 38 image, ~16:35. File: outputs/003_maus/beats/beats_003_maus.csv
- Khóa TANK chỉ câu khẳng định, không ghi tên xe trong prompt veo3; 55 beat có xe đều gắn ref_image (ref/maus_front34|side|front|rear34.jpg, chờ anh lấy ảnh Kubinka từ Wikimedia).
- Hook B001–B019 làm dồn dập: pháo sáng chân trời, kíp lái tháo chạy, nổ, tháp văng (gắn DRAMATIZATION khi dựng).
- 2026-10-15: duyệt 4 clip thử (B001/B002/B005/B006, tạo không có ảnh ref): B001 đạt; B002, B005 ra xe lai King Tiger/E-100 (tháp góc cạnh đặt giữa, tấm hông rời, lộ bánh, 2 nòng dài); B006 kíp lái mặc áo bông kiểu Liên Xô, xe không phải Maus. Viết lại khóa TANK (tháp tròn như bát úp đặt nửa sau, hông là một tấm phẳng liền, nòng phụ ngắn bằng 1/3) và CREW (áo panzer đen, mũ lưỡi trai đen), xuất lại CSV.
- 2026-10-15: tải 4 ảnh ref Kubinka (Wikimedia, CC0/PD) vào outputs/003_maus/ref/, ghi nguồn ở ref/CREDITS.md
- 2026-10-15: viết lại khóa TANK theo ảnh ref Kubinka (thân như viên gạch, tháp hình nêm mũi tròn ở nửa sau, nòng dài không phanh đầu nòng + nòng ngắn), thêm câu 'identical to the attached reference photo'
- 2026-10-15: khóa xe theo từng ảnh ref (TANK_BY_REF), khóa bộ phận (PARTS: deck/turret/hull_dummy/twin) cho 11 beat, cột image_prompt cho 55 beat có xe (bước ảnh tĩnh Muse); bỏ ghi chú overlay ở B014/B052. Tool ib_beats.py hỗ trợ TANK_BY_REF/PARTS/STILL (bản cũ .bak_003); ghi vào skill ib-assets
- 2026-10-15: CSV về đúng 10 cột mẫu (bỏ ref_image/image_prompt); ảnh ref + prompt ảnh tĩnh chuyển sang beats/refs_003_maus.md; sửa tool + skill
- 2026-10-15: theo yêu cầu, chỉ bổ sung vào prompt: bỏ file phụ refs_003_maus.md và phần STILL; CSV đúng 10 cột mẫu
- 2026-10-15: xóa 3 clip thử sai (B002/B005/B006), thư mục _check, _to_delete và tool backup; giữ B001
- 2026-10-16: 12 beat veo3 Muse không tạo được (B012 B017 B018 B096 B103 B109 B113 B152 B166 B174 B176 B180) → viết lại nhẹ hơn (bỏ nổ/lửa/va chạm, chỉ còn khói và cảnh sau) + khóa xe gọn, file beats/beats_003_maus_redo.csv
- 2026-10-16: Muse từ chối cảnh xe bị phá hủy/khói → B012, B180 chuyển sang ảnh tư liệu xác V2 1945; B018, B152, B176 viết lại thành xe còn nguyên, bỏ khói
- 2026-10-16: QC Envato 003: ~30/38 ảnh sai xe; tạo beats/beats_003_maus_veo3_thaythe.csv (33 beat veo3 8s thay ảnh sai, khóa xe chi tiết theo góc ref; xe khác có khóa riêng T-34/T-34-85/Tiger I/Panther/IS-7/Sturmtiger)
- 2026-10-16: đổi file thay thế thành prompt ẢNH (32 beat image, bỏ chuyển động camera) → beats/beats_003_maus_image_thaythe.csv
- 2026-10-16: QC 8 ảnh Flow (ở 002_sturmtiger/_flow_new và _flow): đạt B038, museum Maus, IS-7, B007; sửa B032 (bản vẽ chưa phải Maus), B100 (không phải V12 ngược), B077 (đồng phục/bố cục), result_TEST_01 ra Panzer II (B183 Sturmtiger) → beats/beats_003_maus_image_fix.csv
- 2026-10-16: theo nhận xét Claude Chrome (14/32 ảnh bị bộ lọc chặn): viết lại 32 prompt ảnh, bỏ German/Wehrmacht/Soviet/soldier/officer/quân phục/WWII/swastika, người → thợ máy/kỹ sư đồ bảo hộ hoặc áo dân sự, mô tả Maus đủ bằng chữ (ref chỉ là tùy chọn); gộp 4 bản sửa B032/B077/B100/B183, bỏ file image_fix
- 2026-10-16: đổi tên 32 ảnh Flow trong outputs/_flow thành Bxxx_Axxx.jpg; B183 dùng thumbnail tập 002 (inside-the-sturmtiger.jpg)
- 2026-10-16: chuyển 32 ảnh mới vào 003_maus/beats/footage, xóa ảnh Envato sai cùng beat; xóa thư mục _flow trống
- 2026-10-16: xóa ảnh thu nhỏ cũ trong footage/thumbs của các file Envato đã xóa
- 2026-10-16: QC 109 clip Muse: ~42 sai xe (ra Tiger/King Tiger/Panzer IV), 9 cần xem lại, Maus ngoài trời gần như không tạo đúng; 39 clip không phải 16:9
- 2026-10-16: làm lại 42 clip Muse sai xe theo 2 bước: beats_003_maus_redo2_flow_image.csv (ảnh tĩnh Flow) + beats_003_maus_redo2_muse_video.csv (ảnh→video Muse, chỉ tả chuyển động)
- 2026-10-16: test 2 bước (ảnh Flow → Muse) trên B002/B011/B018: cả 3 giữ đúng Maus suốt 10s, 1216x672; B018 camera lia theo người nên xe trôi khỏi khung cuối clip
- 2026-10-16: viết lại 42 prompt Muse cho ổn định: khung CAMERA/FRAMING/TANK/MOTION/LOOK, camera giới hạn (tripod cố định hoặc dịch ≤10%, cấm pan/bám người), xe luôn nằm trọn khung
- 2026-10-16: test lại B018 trên Muse: bản CAMERA/FRAMING vẫn trôi camera; bản 'still-camera shot, khung giữ y như ảnh, chỉ vật nhỏ chuyển động' giữ khung đứng yên, Maus ở nguyên trong khung 10s → viết lại 42 prompt theo kiểu này (34 still, 8 push nhẹ)
- 2026-10-16: tải được video từ Muse qua Chrome (blob → file, lưu vào thư mục tải gần nhất là outputs/_flow); B018 bản still thay vào footage
- 2026-10-16: chạy xong 42 clip Muse (ảnh Flow → video, prompt still-camera); QC 4 khung/clip, cả 42 đúng Maus; đã thay vào 003_maus/beats/footage (xoá clip sai cũ). B113 chạy lại lần 2 (lần 1 xe quay đầu)
- 2026-10-16: lưu ý khi dựng: B014 nòng ra khỏi khung cuối clip (dùng ~6s đầu); B149 xe chạy xa dần; B050/B086/B096/B128/B153/B002 camera đẩy khá mạnh; B143 xe tải lấn che đầu xe; B158 máy quay lia sang cây cầu; B113 bên hông có vệt lưới hơi lạ
- 2026-10-16: footage 003 còn thiếu B012, B180 (ảnh tư liệu xác xe) — chờ anh bổ sung
- 2026-10-16: bổ sung B012 (ảnh IWM 1945: tháp pháo Maus tách khỏi thân trong nhà máy, PD) và B180 (ảnh Maus V2 thử nghiệm 1944, PD) vào footage 003 → đủ 184/184 beat; ghi nguồn vào ref/CREDITS.md

## [2026-10-16] reorganize | Tách não 2 và sản xuất
- Chuyển outputs/001_king-tiger, 002_sturmtiger, 003_maus, _flow, tools/, sites/ sang Youtube-AI/IronBehemoth-Videos/. IronBehemoth/ chỉ còn CLAUDE.md, index.md, log.md, wiki/, raw/, assets/, .claude/skills/, .secrets/.
- Sửa đường dẫn: CSV beats (đường dẫn tuyệt đối), ib_tts.py (key đọc từ IronBehemoth/.secrets), BROWSER_SNIPPETS.md, CLAUDE.md, index.md, wiki/production/pipeline.md, wiki/tanks/, skill ib-assets, ib-build, ib-script. Các dòng log cũ giữ nguyên đường dẫn lịch sử outputs/.
- 2026-10-16: ib-build 003 Maus: voice ai33 (Russ, speed 0.85, tạo trên web ai33) 15:23, căn beat 96,1%, tempo 0.95 → bản dựng IronBehemoth-Videos/003_maus/full/IB003_Maus_1080p.mp4 (16:21, −16 LUFS, peak −2,4 dBFS); 6 bài nhạc YouTube Audio Library theo chương + 14 SFX Mixkit mới; SRT khớp video full/IB003_Maus_EN.srt; ib_build.py thêm delogo_size (xoá ngôi sao Flow trên ảnh/clip Muse), ghi shot an toàn (.part) và --budget

## [2026-10-17] setup | Thêm kênh riêng City Timelapse vào não chung
- Kênh mới tách riêng khỏi IronBehemoth, chỉ dùng chung não. Namespace: wiki/city-timelapse/, raw/city-timelapse/; sản xuất dự kiến Youtube-AI/CityTimelapse-Videos/.
- Ingest dữ liệu kênh Cornerstone Timelapse (4 video, số liệu 17/10) → raw/city-timelapse/competitors/2026-10-17_cornerstone-timelapse.md
- Tạo trang: [[city-overview]], [[city-format-blueprint]], [[city-pipeline]], [[cornerstone-timelapse]]; cập nhật CLAUDE.md (bảng não nhiều kênh), index.md
- 2026-10-17: tạo thư mục sản xuất Youtube-AI/CityTimelapse-Videos/ (README, _templates/description.md, _templates/publish-checklist.md, data/, tools/, assets/{branding,landmarks,music}); cập nhật CLAUDE.md, [[city-pipeline]]

## [2026-10-17] setup | Chốt tên kênh Skyline Rewind (@SkylineRewind)
- "City Timelapse" đã bị dùng nhiều (@CityTimelapse có chủ) → chốt Skyline Rewind, handle @SkylineRewind còn trống lúc kiểm tra.
- Đổi namespace: wiki/city-timelapse → wiki/skyline-rewind, raw/city-timelapse → raw/skyline-rewind, Youtube-AI/CityTimelapse-Videos → Youtube-AI/SkylineRewind-Videos; frontmatter channel: skyline-rewind. Các dòng log cũ giữ đường dẫn lịch sử.
- trang bị ảnh hưởng: [[city-overview]], [[city-format-blueprint]], [[city-pipeline]], [[cornerstone-timelapse]], CLAUDE.md, index.md

## [2026-10-17] ingest | Từ khóa kênh Skyline Rewind
- Lấy tag 33 video lớn trong ngách (YouTube) + đo vidIQ 3 seed → raw/skyline-rewind/keywords/2026-10-17_big-videos-and-vidiq.md
- Chốt 10 từ khóa kênh 5K–50K đúng tuyến, xếp volume giảm dần → [[skyline-channel-setup]]; cập nhật index.md

## [2026-10-17] setup | Đổi tên kênh thành City Timelapse
- Chủ kênh chốt tên hiển thị "City Timelapse" (thay Skyline Rewind); handle cập nhật sau.
- Đổi namespace về wiki/city-timelapse, raw/city-timelapse, Youtube-AI/CityTimelapse-Videos; trang skyline-channel-setup → [[city-channel-setup]]; frontmatter channel: city-timelapse.
- trang bị ảnh hưởng: [[city-overview]], [[city-channel-setup]], [[city-format-blueprint]], [[city-pipeline]], [[cornerstone-timelapse]], CLAUDE.md, index.md

## [2026-10-17] ingest | City Timelapse chuyển sang thị trường tiếng Tây Ban Nha
- Chủ kênh chốt kênh tiếng Tây Ban Nha. Thu video lớn TBN + vidIQ 15 seed TBN → raw/city-timelapse/keywords/2026-10-17_es-big-videos-and-vidiq.md
- Từ khóa đúng ngách TBN đều < 5K → 10 từ khóa kênh nới ra 3 trụ documental historia + animación 3D + ciudades; từ đúng ngách để tag video.
- trang bị ảnh hưởng: [[city-channel-setup]], [[city-overview]], CLAUDE.md, index.md

## [2026-10-17] setup | City Timelapse: logo, banner, mô tả kênh, disclaimer
- Logo + banner tạo bằng ChatGPT (Chrome); logo cắt nền ngoài vòng tròn trong suốt (800, 1254, watermark 150); banner 2560×1440 dịch xuống 100 px cho vùng an toàn → Youtube-AI/CityTimelapse-Videos/assets/branding/
- Mô tả kênh TBN (992 ký tự) + EN + mẫu disclaimer video → CityTimelapse-Videos/_templates/channel-about.md
- trang bị ảnh hưởng: [[city-channel-setup]]
- 2026-10-17: thêm tên kênh City Timelapse + handle đề xuất @CityTimelapseHQ (dự phòng @TheCityTimelapse, @CityTimelapseTV; cả 3 còn trống lúc kiểm tra) vào channel-about.md, [[city-overview]], [[city-channel-setup]], CLAUDE.md, index.md
- 2026-10-17: thêm bộ hashtag TBN/EN (3 cố định + chủ đề + thành phố, ≤10/video) vào channel-about.md và [[city-channel-setup]]

## [2026-10-17] produce | City Timelapse demo 001 Ciudad de México (58s)
- Phân tích video mẫu Las Vegas (Cornerstone) → cấu trúc hook/tua ngược/title/chương/kết đêm.
- 5 clip Veo 3.1 Lite (Flow) + nhạc YouTube Audio Library + 9 SFX Mixkit → CityTimelapse-Videos/001_ciudad-de-mexico/demo/CT001_CDMX_demo_1080p.mp4
- Tool mới: CityTimelapse-Videos/tools/ct_build_demo.py, ct_mix_demo.py
- trang bị ảnh hưởng: [[city-demo-001]]
- 2026-10-17: demo 001 đổi endcard sang kiểu IB (Me gusta / Suscribirse→Suscrito / chuông + con trỏ + SFX click/bell), bỏ banner; tool ct_endcard.py; [[city-demo-001]]
- 2026-10-17: query nhu cầu tìm kiếm theo thành phố (vidIQ ES/EN) → raw/city-timelapse/keywords/2026-10-17_city-demand-vidiq.md; cập nhật [[city-overview]]
- 2026-10-17: thêm pipeline tập đầy đủ City Timelapse (không lời dẫn, 8:00–8:58, Muse 10s): tool ct_build.py, ct_csv.py; 3 skill ct-viet-kich-ban, ct-viet-prompt, ct-dung-video; [[city-pipeline]]

## [2026-10-18] produce | Kịch bản 001 Roma
- 50 beat (≈8:31), 10 chương, 37 caption ES; research.md có nguồn từng mốc; Publish ES (tiêu đề + A/B, thumbnail, description + chapters, tags); 3 bước kiểm tra (review board, policy, fact-check).
- Sửa ct_build.py: năm a. C.; ghi chú Muse không watermark.
- trang bị ảnh hưởng: [[roma]], [[city-pipeline]], index.md

## [2026-10-18] produce | Prompt CSV 001 Roma
- ct-viet-prompt: 50 prompt Muse 10s → `CityTimelapse-Videos/001_roma/prompts.json` + `001_beats.csv` (header khớp mau_beat, 81–110 từ, camera xoay vòng 6 kiểu, B016 viết thành "xây lại khu phố trống", không từ bị chặn). Bước tiếp: anh tạo clip Muse → footage/Bxxx_Axxx.mp4 → ct-dung-video.

## [2026-10-18] fix | CSV 001 Roma bị báo không hợp lệ
- Header/BOM/CRLF/10 cột khớp mau_beat; khác biệt duy nhất: visual_query 628–800 ký tự (mẫu ≤506), avoid tới 205 (mẫu ≤67). Viết lại v3 ngắn: visual_query ≤500, avoid ≤100, khóa phong cách sa bàn đất sét. Bài học: prompt Muse trong CSV giữ ≤500 ký tự.

## [2026-10-18] fix | Prompt 001 Roma v4 — kéo về look demo
- Muse ra chi tiết/ảnh thật hơn demo Veo. "tabletop diorama" làm Muse vẽ cả bàn + phòng (B003, B006) → bỏ. Khóa v4 = khóa demo gốc ("miniature architectural 3D model of a city, clean untextured clay-like…") + "simple smooth blocky shapes"; avoid thêm no textures/no fine detail/no table. Ảnh tham chiếu phong cách từ demo: 001_roma/ref/style_ref_*.png.

## [2026-10-18] produce | Kịch bản 001 Ciudad de México (Roma tạm dừng)
- Anh tạm dừng 001 Roma, làm tiếp 001 CDMX. Xem lại demo (Veo, 5 clip) → áp bài học vào kịch bản: sa bàn cố định hồ Texcoco + Chapultepec + Tepeyac + 2 núi lửa; cảnh hiện đại luôn có cây xanh/núi.
- 50 beat (≈8:31), 8 chương, 41 caption ES → `CityTimelapse-Videos/001_ciudad-de-mexico/kich-ban.md`; nguồn từng mốc → `research.md`; Publish ES (tiêu đề + 2 A/B, thumbnail, description + chapters, tags); 3 bước kiểm tra.
- trang bị ảnh hưởng: [[ciudad-de-mexico]], [[roma]], index.md

## [2026-10-18] produce | Prompt CSV 001 Ciudad de México
- So khung hình demo Veo với clip Muse Roma cũ (qc/style_compare.jpg): demo = nhà trắng/kem, nước xanh, núi xanh; Muse Roma lệch sang đất nặn hoặc ảnh thật; demo megalópolis bị sa mạc.
- 50 prompt Muse 10s → `CityTimelapse-Videos/001_ciudad-de-mexico/prompts.json` + `001_beats.csv` (header/BOM/CRLF khớp mau_beat; visual_query 441–498 ký tự, avoid ≤98; 6 kiểu camera, không 3 beat liền cùng kiểu). Tool: `tools/_cdmx_prompts.py`.
- Phát hiện lỗi: avoid riêng từng beat của Roma bị cắt hết vì phần avoid chung dài 98 ký tự.
- trang bị ảnh hưởng: [[ciudad-de-mexico]], [[city-pipeline]]

## [2026-10-18] fix | Prompt 001 CDMX B024 Muse không tạo được
- Muse báo B024 ra thành phố chi tiết như thật, không thấy công trình mọc lên (2 lần). Nguyên nhân: chữ phong cách kiến trúc ("ornate baroque", "palaces of red volcanic stone") kéo về chi tiết thật.
- Viết lại B024: camera cố định, "rises out of the ground block by block", avoid thêm no fine detail. Làm mềm trước B025, B027, B028, B033, B035, B037 (bỏ baroque/ornate/neoclassical/art deco/French-style). Bản cũ: 001_beats_v1.csv, prompts_v1.json.
- Bài học: prompt Muse tả hình khối đơn giản, không dùng tên phong cách kiến trúc.

## [2026-10-18] qc | 001 CDMX footage B001–B032
- Kỹ thuật: 32 clip 1280×720 24fps 10s, không lỗi giải mã. Dò cắt cảnh: B011 (9,92s) và B030 (9,5s, nhảy sang người đi trong bảo tàng) → cắt đuôi + giãn về 10s; bản gốc footage/_orig/.
- Tạo lại: B003 (camera thấp), B008 (thành phố Địa Trung Hải), B012 (nhà thờ mái vòm năm 1519), B016 (lâu đài cổ tích), B019 (công trường hiện đại, cần cẩu, máy xúc), B024 (bãi đỗ ô tô), B031 (lâu đài cổ tích). Prompt mới: qc/tao_lai_B01-32.md; B050 đổi "castle" → "palace" phòng trước.
- B014 diễn biến ngược (đất trống → thành phố có kim tự tháp) → đề xuất dùng bản đảo chiều footage/_alt/B014_A014_reverse.mp4.
- Bài học Muse: "fortress"/"castle" ra lâu đài châu Âu; "foundations" ra công trường hiện đại; mở đầu clip hay có công trình sai thời (mái vòm) rồi mới kéo ra.

## [2026-10-18] qc | 001 CDMX B033–B050 + xóa beat không đạt
- B033–B050: đạt 13; B037 (Manhattan/Capitol 1934), B041 (lộ mép bàn), B045 + B049 (nhà thờ Gothic, kim tự tháp Maya nguyên vẹn), B050 (lâu đài cổ tích) không đạt. B042 báo cắt cảnh nhầm, giữ nguyên.
- Theo yêu cầu: xóa 12 clip không đạt (B003, B008, B012, B016, B019, B024, B031, B037, B041, B045, B049, B050); B014 thay bằng bản phát ngược.
- Prompt mới: `001_beats_tao-lai.csv` (12 dòng) + `qc/tao_lai.md`; CSV đầy đủ cập nhật (bản trước: 001_beats_v3.csv).
- Phân tích nguyên nhân → trang mới [[city-muse-prompt-rules]]; cập nhật [[city-pipeline]], index.md.

## [2026-10-18] qc | 001 CDMX — QC 12 beat tạo lại
- Đạt 10: B003, B008, B012, B016, B024, B031, B037, B041, B045, B050 (B008 thành phố xa hơi kiểu Địa Trung Hải; B024/B045 nhà thờ hơi Romanesque/Gothic — chấp nhận).
- Không đạt 2 (đã xóa): B019 (vẫn Gothic + cần cẩu), B049 (Gothic kiểu Notre-Dame, tàn tích Hy Lạp, lộ phông nền). Nguyên nhân: chữ "cathedral" + "two square bell towers" = Notre-Dame; "no gothic" không đủ. Prompt lượt 2 bỏ chữ cathedral, tả tháp chuông mũ chuông + mái vòm.
- Cập nhật [[city-muse-prompt-rules]].

## [2026-10-18] qc | 001 CDMX — QC lượt 2 (B019, B049)
- B049 đạt: nhà thờ tháp mũ chuông + mái vòm, không Gothic, dinh thự, tàn tích thấp, đêm.
- B019 không đạt: clip là cảnh đêm + tàn tích (nội dung của B049), không phải nhà thờ mọc lên ban ngày — có thể đã dán nhầm prompt B049. Chuyển sang footage/_alt/B049_take2.mp4 (bản dự phòng B049). Bài học: prompt bỏ chữ "cathedral" đã hết Gothic.
- 2026-10-18: file B049 mới thực ra là nội dung B019 (nhà thờ mọc lên ban ngày, đạt) → đổi thành B019, cắt bỏ 1,15s cuối lộ mép sa bàn + giãn về 10s (gốc: footage/_orig/B019_A019_raw.mp4). Bản đêm B049_take2 → B049. Đủ 50/50 beat đạt QC.

## [2026-10-18] produce | Dựng 001 Ciudad de México hoàn chỉnh
- B049: chọn bản prompt mới (quảng trường + cột cờ, nhà thờ tháp mũ chuông); 2 bản kia → footage/_orig/.
- Âm thanh: Ancient Civilisations + The Grey Room + Ancient Civilisations lặp lại (2 bài demo chỉ ~350s < 512s); SFX demo (thiếu tiếng gió/đám đông → beat viento/multitud không có ambience).
- Kết quả: CT001_ciudad-de-mexico_1080p.mp4 — 8:32, 1920×1080 30fps, AAC 256k, −14,1 LUFS, peak −1,6 dBFS, 1,13 GB; QC: qc/final_sheet_10s.jpg, qc/final_frames.jpg.
- Sửa ct_build.py (bản cũ: tools/ct_build_bak_20261018.py); mốc CAPÍTULOS +1s (tua ngược 4s).
- trang bị ảnh hưởng: [[ciudad-de-mexico]], [[city-pipeline]]

## [2026-10-18] produce | Endcard mới chồng lên cảnh cuối (City Timelapse + IronBehemoth)
- Chủ kênh không thích endcard nền trắng/kem → endcard thành lớp trong suốt chồng lên beat cuối, có lớp tối mờ cho chữ; nút Like/Subscribe/Subscribed tiếng Anh.
- City Timelapse: ct_endcard.py --overlay, ct_build.py (endcard overlay mặc định, CT_OUT_DIR xuất ra ổ tạm). 001 CDMX dựng lại: CT001_ciudad-de-mexico_1080p.mp4 — 8:24, −14,1 LUFS, peak −1,6 dBFS.
- IronBehemoth: make_endcard.py --overlay, ib_build.py endcard_style='overlay' (mặc định) dùng clip beat END_AT quay chậm; thử trên 003 Maus (B184) đạt. Bản cũ *.bak_overlay.
- trang bị ảnh hưởng: [[pipeline]], [[city-pipeline]], [[ciudad-de-mexico]], skill ib-build
- 2026-10-18: IB thanh kênh thêm nút Like (Like → Subscribe → chuông, con trỏ bấm lần lượt) giống City Timelapse; ib_build.sfx_plan: 3 click (1,30 / 2,05 / 2,80s) + chuông 2,85s; DUR 5,4s. Bản cũ: tools/video/make_subscribe.py.bak_like. Áp dụng cho cả thanh giữa video lẫn end card.
- 2026-10-18: City Timelapse thêm thanh nhắc Like/Subscribe giữa video: front matter `subscribe: B011+2` (ct_build.py + ct_endcard.py --bar, 3 click + chuông). 001 CDMX: thanh ở 1:46 (cảnh Tenochtitlan rực rỡ, beat không caption); video dựng lại 8:24, −14,1 LUFS.

## [2026-10-18] produce | Kịch bản 004 Inside the Scorpion (ib-script)
- Không có mẫu đối thủ riêng → theo anh Aron mượn mẫu 003 (Blue Paw Print Maus) để học cấu trúc: `004_scorpion/doi-thu/README.md`, `analysis_004.md`.
- Nghiên cứu: `raw/tanks/2026-10-18_scorpion.md`, trang mới [[scorpion]]. Lệch nguồn: ngày kỷ lục (26/1 hay 26/3/2002) → chỉ nói năm; xe trúng mìn Tumbledown (Scorpion/Scimitar) → "by most accounts a Scorpion".
- `script.md` 2.453 từ (~16:34), mở/đóng ở cảnh xe trúng mìn dưới Mount William đêm 13/6/1982 (DRAMATIZATION); 3 câu hỏi, 3 open loop; subscribe ~2:13; cầu nối Inside the Maus. `review_004.md` (review, chính sách, fact-check, QC), `notes.md` (tiêu đề, thông số, nguồn, description, chapters). Chưa tra từ khóa vidIQ.
- trang bị ảnh hưởng: [[scorpion]], [[topic-backlog]], index.md

## [2026-10-18] produce | CSV tài nguyên 004 Scorpion (ib-assets)
- Muse 10s (theo anh Aron): 178 beat, 2.453 từ, ~16:34. veo3 93 / footage 42 / image 43, không chuỗi >3 beat cùng loại.
- `beats/locks.json`: khóa xe Scorpion chỉ tả bằng câu khẳng định (thân hộp thấp, 5 bánh lớn, tháp nhỏ đặt sau, nòng ngắn dày, xanh đậm vằn đen), 4 khóa theo ảnh ref (`ref/scorpion_front34|side|rear34|front.jpg`, anh tự đặt ảnh), PARTS interior/engine_deck/tracks; STYLE Cold War 1970s–1982.
- Đầu ra: `IronBehemoth-Videos/004_scorpion/beats/beats_004_scorpion.csv` (10 cột đúng mẫu). Chưa có ảnh ref; mô hình 3D NoAI không được dùng làm ref.
- Lưu ý từ 003: Muse vẽ sai xe ~40%; nếu lặp lại nên làm 2 bước (ảnh tĩnh Flow → Muse animate, camera tĩnh).

## [2026-10-18] qc | 004 Scorpion tài nguyên lượt 1
- 177/178 beat (thiếu B152). Clip AI 93: đạt 89; tạo lại B046, B059 (nòng dài), B074/B085 dùng 5s đầu.
- Ảnh/stock: 25 cần thay (sai xe: B006 B011 B040 B044 B049 B058 B091 B121 B143 B164 B167 B169 B029 B035 B062 B079 B081 B086 B101 B106 B127 B177; lệch nội dung: B037 B133 B159). Báo cáo: IronBehemoth-Videos/004_scorpion/qc/qc_footage_004.md.
- Bài học: kho stock gần như không có Scorpion → beat có tên xe nên lấy Wikimedia/IWM hoặc clip AI có ref.

## [2026-10-18] produce | 004 Scorpion — tạo lại 17 clip trên Muse
- Chuyển 14 beat ảnh sai xe/lệch nội dung sang clip AI (B006 B011 B037 B040 B044 B049 B058 B091 B121 B133 B159 B164 B167 B169) + tạo lại B046, B059, B152 (thiếu). Prompt: beats/beats_004_scorpion_redo.csv; CSV chính cập nhật (bản trước: beats_004_scorpion_v1.csv).
- Muse: đoạn chat phụ "Tạo video xe tăng Anh 1970s", batch 2 prompt/tin. B152 bị từ chối lần 1 (blast/flash), viết nhẹ lại (spray of mud and smoke) thì qua. B164 sơn cát sa mạc.
- Tải: Chrome chặn tải nhiều file từ muse.ai cho tới khi anh Aron cho phép Automatic downloads. File về _flow/ rồi chép vào beats/footage/, bản cũ ở footage/_orig/.
- QC: 17 clip 1280x720 10s. Đạt 15; B059 nòng vẫn dài ở giữa clip; B152 không thấy tia nổ (xe nằm trong hố, lửa xa) — dùng tạm.
- Còn lại cần ảnh thật: B029 B035 B062 B079 B081 B086 B101 B106 B127 B143 B177 (Wikimedia/IWM).

## [2026-10-18] qc | 004 Scorpion — ảnh Envato lượt 2
- Đạt: B079 (tấm nhôm). Không đạt: B035 (BTR-80 bánh lốp), B081 (súng máy cổ), B106 (Challenger 2, không phải King Tiger), B143 (xe bọc thép bánh lốp). Ảnh cũ sai xe còn lại: B029 B062 B086 B101 B127 B177; yếu: B026 (máy bay WWII), B142.
- Đã chuyển hết sang footage/_orig/. Prompt Flow (Veo 8s) cho 12 beat: beats/beats_004_scorpion_flow.csv. Ảnh ref Maus chép sang 004_scorpion/ref/maus_front34.jpg.
- 2026-10-18: B177 (cầu nối tập Maus) dùng lại clip 003_maus B158 (Maus kẹt cạnh cây cầu sập) thay vì tạo mới; bỏ B177 khỏi beats_004_scorpion_flow.csv (còn 11).
- 2026-10-18: B106 (so sánh King Tiger): Flow từ chối prompt xe tăng Đức WWII → dùng lại clip 001_king-tiger B075_A01 (King Tiger bò lên dốc bùn); bỏ B106 khỏi flow CSV (còn 10). Bài học: cảnh xe của tập trước thì lấy lại từ thư mục tập đó.
- 2026-10-18: B106 (so sánh King Tiger): Flow từ chối prompt xe tăng Đức WWII → dùng lại clip 001_king-tiger B075_A01 (King Tiger bò lên dốc bùn), lưu 004_scorpion/footage/B106_A106.mp4; bỏ B106 khỏi flow CSV (còn 10). Bài học: cảnh xe của tập trước thì lấy lại từ thư mục tập đó.
- 2026-10-18: 10 clip Flow (B026 B029 B035 B062 B081 B086 B101 B127 B142 B143) đã nhận, mỗi clip chỉ 4,0s (1280x720). Xoá ngôi sao watermark sẵn bằng delogo x=1130 y=570 w=62 h=62 (bản gốc footage/_orig/flow_raw/). CSV chính: 10 beat → veo3, provider "AI da xoa logo" (không chứa flow/veo/google để ib-build không xoá lần 2).

## [2026-10-18] query | Abrams: nguồn hình ảnh + video đối thủ
- Trả lời từ dữ liệu sẵn có: footage DVIDS/Commons PD dồi dào (demo đã có 13 file); đối thủ đã làm nhiều (Jared Owen 64.9M, 19-Kilo 37.7M, Real Engineering 7.6M...), Blue Paw Print chưa làm Abrams.
- trang tham chiếu: [[m1-abrams]] · [[footage-sources]] · [[landscape]] · [[topic-backlog]]

## 2026-10-18 — 004_scorpion /ib-build: preview
- Render chuyển lên container (máy local chậm, tiến trình nền bị kill); footage stage 171 file + tar audio/gfx/build/tools.
- Hiệu ứng mới trong ib_build.py (backup ib_build.py.bak_fx): `lut` (common/luts/IB_Steel.cube, tạo bằng colour-science/colour BSD-3), `grain` (ffmpeg noise), `shake` [[beat, t0, dur, px]] — cấu hình trong build/ib.json.
- Preview 720p 977.9 s; QC: I −16.0 LUFS, peak −1.2 dBFS; 3 chapter overlay, title, card_8, subscribe, endcard OK; dip-to-black 0.15 s mỗi cut là thiết kế.
- B149 (stock sét đêm gần như đen 7 s) → thay bằng B001 (đồi đêm có lửa, callback mở đầu).
- notes.md chapters cập nhật theo beat_times; credits.md mới. Chờ anh duyệt preview rồi render 1080p.
- Sửa theo anh (1:41): đoạn 3 câu hỏi B019–B021 đổi từ danh sách góc trái (q1/q2/q3.png) sang thẻ câu hỏi giữa màn hình, mỗi lần 1 câu (ib_qcard.py: gfx/qcard/q01–q03.png + dim.png). ib_build.py thêm overlay `qc:qNN.png@t@d` (nền tối + thẻ phóng nhẹ + whoosh); backup ib_build.py.bak_qcard (trên container). Preview v2: full/IB004_Scorpion_preview_480p_v2.mp4.
- Theo anh: bỏ chữ QUESTION trên thẻ câu hỏi (ib_qcard.py, mặc định cho mọi tập); tạo lại gfx/qcard, preview v3. Cập nhật skill ib-build: bước 5 tạo thẻ bằng ib_qcard.py, bước 6 dùng `qc:qNN.png@t@d` thay q1/q2/q3, bước 8 ghi chú xóa cache khi đổi PNG, bước 9 QC kiểm thẻ giữa màn hình.

## [2026-10-18] produce | Kịch bản 002 Las Vegas
- Tham khảo video mẫu Cornerstone (OnuZcxjyQzE). 60 beat × 8s (Veo 3) + tua ngược 4s ≈ 8:04 (chủ kênh: khoảng 8 phút), 10 chương 1829→2026, 53 caption tiếng Anh.
- Chủ kênh chốt: tiêu đề tiếng Tây Ban Nha, chữ trên màn hình tiếng Anh (mở rộng ngôn ngữ). Front matter `lang: en` (cần thêm vào ct_build/ct_endcard), `delogo` cho Flow, `subscribe: B013+2`.
- File: CityTimelapse-Videos/002_las-vegas/{kich-ban.md, research.md, _gen_kichban.py}.
- trang bị ảnh hưởng: [[las-vegas]], index.md

## [2026-10-18] produce | Chốt tiêu đề tập Abrams
- Tiêu đề: "Inside the Abrams: The World's Most Powerful Tank" (bỏ hướng "fastest" 17/10). Căn cứ 19FortyFive top 1 năm 2026; A/B dự phòng: Heaviest Tank in the World (Guinness, đang phục vụ).
- trang bị ảnh hưởng: [[m1-abrams]] · IronBehemoth-Videos/005_abrams/outline.md

## [2026-10-18] lint | Kiểm tra nguồn 002 Las Vegas + 001 CDMX
- API Wikipedia (qua Chrome): LV 40/40 link tồn tại; CDMX 2 link sai tên đã sửa (Tlatelolco_(altepetl), es: Gran_Canal_del_Desagüe_(Ciudad_de_México)). Đối chiếu mốc với nội dung bài.
- Sửa LV: tên "Las Vegas" — không có bằng chứng Rivera đặt tên (đến thung lũng 12/1829–1/1830), ghi nhận sớm nhất là Frémont 1844 → sửa caption B003/B004 + description; Stewart 1881 (không 1882); thử hạt nhân 65 dặm tây BẮC; bỏ "world's largest hotel" khỏi caption International 1969.
- CDMX (đã dựng): mọi mốc khớp; ghi chú Tam cường 1428 (thắng chiến tranh) / 1430 (hiệp ước).
- trang bị ảnh hưởng: [[las-vegas]], [[ciudad-de-mexico]]

## [2026-10-18] produce | Abrams thành tập 005
- Đổi thư mục IronBehemoth-Videos/004_abrams → 005_abrams; ảnh IB004_F* → IB005_F* (IB004 thuộc Scorpion); sửa nhãn tập trong dàn ý/footage list.
- trang bị ảnh hưởng: [[m1-abrams]] · [[topic-backlog]] · index.md

## [2026-10-18] produce | Script tập 005 Inside the Abrams
- Script "Inside the Abrams: The World's Most Powerful Tank": 2.442 từ (~16:30), 3 câu hỏi, 3 open loop, subscribe ~2:37; mở/đóng 73 Easting.
- Review board + audit chính sách + fact-check + QC (review_005.md); bỏ 3 câu không nguồn; hook nói "one major defense ranking… number one" thay vì khẳng định "most powerful".
- Dàn ý viết lại theo script; demo 60s giữ ở demo/script.md.
- trang bị ảnh hưởng: [[m1-abrams]] · [[topic-backlog]] · index.md · raw/tanks/2026-10-18_m1-abrams-bo-sung.md
- 3D tháo rời (Blender, mô hình LM3D CC BY 4.0) chèn ở B040 (3:35, "How do you fit three men…"), off=1.5, zoom=1.0; credits.md thêm ghi công.
- Render 1080p trong container (52 phút, 172 shot): 977.9 s (16:18), −16.0 LUFS, peak −2.5 dBFS. Giao qua 83 phần 12 s (full/parts/, part_060 tách a/b vì > 30 MB) → ghép trên máy: full/IB004_Scorpion_1080p.mp4 (875 MB). Chờ anh duyệt để đặt FINAL.

## [2026-10-19] produce | Prompt Veo 3 tập 002 Las Vegas
- Xem video mẫu (data/001/EVOLUTION-OF-LAS-VEGAS1855–2026.mp4, 18 khung): look = render 3D kiểu bản đồ GIS (nhà khối trơn trắng/xám/pastel, sa mạc cát phẳng, đường nhựa xám, nhìn chéo ~800 m, màu nhạt; đêm = nền tối + cửa sổ sáng + viền neon) — khác look đất sét của CDMX. Ảnh tham chiếu: 002_las-vegas/ref/style_ref_day.jpg, style_ref_night.jpg, sample_sheet.jpg.
- 60 prompt Veo 3 (8s) → 002_las-vegas/prompts.json + 002_beats.csv (provider=flow, itemType=veo3; vq 375–477, avoid ≤97; 6 kiểu camera không 3 liền). Tool: tools/_lv_prompts.py. ct_csv.py đọc `provider` từ front matter.
- Áp dụng [[city-muse-prompt-rules]]: không "castle/fort/cathedral/casino", nổ phá = "slowly lowers into pale dust", thử hạt nhân = ánh sáng xa, avoid riêng từng beat.
- 2026-10-19: QC 5 clip Veo thử (002 LV): đổi tên theo nội dung (B005, B033, B058, B059, B060). Đạt B033/B059/B060; không đạt B005 (thị trấn hiện đại + đường nhựa năm 1855 — do khóa phong cách có "gray asphalt roads") và B058 (ra cây đàn thật, nền đồi cát). Sửa: B002–B013 bỏ "gray asphalt roads" + nhà trắng khỏi khóa, avoid "no town, no roads"; B058 tả "glass hotel tower whose outline is shaped like an electric guitar", avoid "no musical instruments". Vị trí "Veo" khớp delogo 1851,1029,60,39. Bài học: tải nhiều clip Flow cùng lúc mất mã beat trong tên → nhận diện bằng hình.
- 2026-10-19: B005 + B058 tạo lại ĐẠT (sa mạc trống + khu nhà đất mọc lên; khách sạn kính hình cây đàn giữa các tháp resort). Clip Flow chỉ 4s → kéo chậm 2× bằng minterpolate (mci) lên 8s, soi khung không thấy lỗi; bản gốc 4s ở footage/_orig/. Lưu ý: kiểm tra Flow để thời lượng 8s.
- 2026-10-19: B005/B058 bản 8s mới (v2) đạt nhưng kém hơn bản 4s kéo chậm (B005 v2: ruộng có sẵn từ đầu, suối thành hẻm vực lớn; B058 v2: tháp đứng giữa đại lộ, có sẵn từ đầu không mọc lên, chói nắng) → giữ bản kéo chậm, v2 ở footage/_alt/.
- 2026-10-19: QC cuối 60 clip 002 LV — kỹ thuật đạt cả 60 (8s, 1280×720, không cắt cảnh, không trùng). Phong cách đồng đều, khớp video mẫu. Cần tạo lại: B002 (nền title có cả thị trấn adobe — phải là thung lũng trống), B014 (cận cảnh đường phố, biển hiệu có chữ, xe hiện đại), B019 (Flamingo 1946 giữa thành phố dày đặc). Prompt mới đã cập nhật vào 002_beats.csv.

## [2026-10-19] build | CT002 Las Vegas
- B002/B014/B019 tạo lại đạt QC; xóa 002_beats_tao-lai.csv.
- ct_build.py/ct_endcard.py: thêm `lang: en` (REWINDING TIME, "Which city should we rebuild next?", "The history of cities, year by year"); backup *_bak_lang.py.
- Dựng xong CT002_las-vegas_1080p.mp4: 8:03, 1080p, -14.1 LUFS; nhạc tạm dùng lại bộ của 001.

## 2026-10-19 — 004_scorpion: đổi sang giọng clone IB-Clone (clone_2700943)
- Lý do: bình luận khán giả tập 002 chê giọng AI "robotic" (Russ speed 0.85 + atempo). Anh Aron tự thu 3:31 giọng → mẫu 29 s `_voice_clone/thuandv_clone_29s.wav` → clone trên ai33 (MiniMax speech-02-hd).
- Voice tập 4: 10 đoạn theo chương (audio/clone/chunk_NN.txt/.mp3/.json), speed 1.0, thẻ `<break>` 0.3/0.6 s, ghép bằng tools/video/ib_voice_join.py (cân −15 LUFS mỗi đoạn, nghỉ 0.7 s giữa chương, đổi số → chữ trong transcript). 155 wpm, khớp chữ 99,1%. Bản Russ cũ: audio/_russ_old/.
- Căn lại: ib_align (178 beat), dời SFX + shake theo từ, edit_shotmap (chapter card lùi để hiện đủ 3 s; gộp B077+B078; B149→B001; B040 3D off=1.0), make_music.
- ib_build.py: thêm `limit` và `post_gain` trong ib.json (trước đây limiter 0.6 làm bản dựng chỉ −16 LUFS). Tập 4: loudness −14.6, limit 0.85, post_gain 1.4 → −14,7 LUFS, peak −1,3 dBFS.
- Bản cuối: full/IB004_Scorpion_1080p.mp4 (16:04, 868 MB); bản Russ cũ → full/IB004_Scorpion_1080p_russ.mp4. dubprep: voice/004_scorpion.srt (177 câu) + .mp3, script_004_scorpion.txt, _tmp_skill/*_nhac/_sfx.flac cho long-tieng.
- Lưu ý chuyển file: file âm thanh (mp3/flac) qua thư mục outputs bị thay đổi nội dung → gói tar rồi mới chuyển, kiểm md5 trên máy.
- Chapters mới: 0:00 · 2:16 · 3:26 · 5:04 · 6:32 · 8:30 · 10:05 · 10:46 · 12:12 · 14:29 (notes.md, index/public-en.txt).

## [2026-10-19] produce | Thumbnail v2 tập 002 Sturmtiger
- Prompt mới: cắt lớp nền đen, 3 kíp lái nạp đạn 380 mm, ánh cam #E0662B, siết độ nét (không khói/tuyết/nền rối); phương án B quy mô, C chữ "10 MIN" thêm bằng Canva.
- File: IronBehemoth-Videos/002_sturmtiger/thumbnail/prompt_thumbnail_v2.md; tham chiếu [[thumbnail-formula]] · [[blue-paw-print]]
- 2026-10-19: thumbnail tập 4 (thumbnail/): ảnh gốc ChatGPT 1672×941 (full/inside-the-scorpion*.png) → 1280×720: overcast (không chữ), bluesky (không chữ), overcast_82kmh ("82 KM/H" + nhãn cam "WORLD'S FASTEST TANK"). Gợi ý chạy Test & Compare 3 bản.
- 2026-10-19: ib-assets 005_abrams (Muse 10 s): 178 beat, 2.442 từ, ~16:30; 99 veo3 / 57 footage / 22 image → beats/beats_005_abrams.csv. Khóa xe Abrams tả bằng hình dạng (không tên xe trong prompt), 3 ảnh ref PD trong ref/ (front F03, side F01, 3/4 F08), PARTS: interior/roof/door/engine/sight. B177 (Scorpion) nên dùng lại clip tập 004.

## [2026-10-20] build | Tập 005 Abrams — 1080p xong
- Voice IB-Clone qua API (ib_tts_clone.py, 11 chunk theo chương, speed 1.0, break 0.3/0.6 s); chunk 11 bị 429 → làm riêng. Ghép 15:57, khớp chữ 98,7%, 178/178 beat.
- ib_tts_clone.py sửa: gửi từng đoạn một, tự chờ khi 429, lưu task id ngay (_tasks.json); thêm --one.
- QC ảnh: thay ảnh stock sai xe (T-72/T-90 B013·B084·B109, Challenger 2 B031·B163, BMD B134, Panzer B027, xe khác B035) và ảnh người mẫu (B030/B153) bằng ảnh Abrams thật Wikimedia PD; bỏ B151 (lịch DEC 31). Chữ trên màn hình: bỏ "19FORTYFIVE"/"AGT1500" (chữ lẫn số), SEP V3, ≈ 40 MAIN GUN ROUNDS ON BOARD, ≈ 8 SECONDS, NEARLY 70 TONNES; bỏ nhãn GULF WAR/UKRAINE trên ảnh stock.
- Kết quả: full/IB005_Abrams_1080p.mp4 (16:07, −15.0 LUFS, peak −0.9 dBFS), voice/005_abrams.srt + mp3, _tmp_skill nhạc/sfx flac, script_005_abrams.txt, credits.md, chapters trong notes.md.

## [2026-10-20] produce | Tập 006 Tiger I — script
- Nghiên cứu đối thủ (raw/competitors/2026-10-20_top-tank-videos-for-ep6.md): Tiger I nhu cầu cao, Blue Paw Print chưa làm.
- Theo yêu cầu anh Aron: bám đối thủ, học hook "This is the …". Phân tích King Tiger + Sturmtiger của Blue Paw Print → analysis_006.md (mạnh: hook gọi tên + nghịch lý, tour cố định, chuỗi bắn bằng lệnh kíp lái; yếu: thông số khô, không câu chuyện, trích chỉ huy SS, CTA yếu).
- Script 2.451 từ: hook kiểu đối thủ + open loop Tiger 131, bỏ 3 câu hỏi. Kèm review_006.md, notes.md; tạo [[tiger-i]], cập nhật [[topic-backlog]], index.

## [2026-10-20] produce | ib-assets 006_tiger (Muse 10 s)
- 173 beat, 2.458 từ; 139 veo3 (56 beat kiểu 3D Blue Paw Print: sàn bóng, x-ray cyan, exploded view) / 19 image / 15 footage → beats/beats_006_tiger.csv.
- Khóa xe Tiger I tả bằng hình dạng (không tên xe trong prompt), 3 ảnh ref Wikimedia (CC BY/BY-SA) ghi trong ref/CREDITS.md; ib_beats.py thêm "style": "3d" → STYLE_3D.
- Hook gây cấn: xe lao ra khỏi khói, xích nghiền tường, đạn nảy khỏi giáp trước, kíp lái nhảy khỏi xe bỏ chạy.
