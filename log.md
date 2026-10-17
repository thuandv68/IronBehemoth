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
