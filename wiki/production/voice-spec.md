---
title: Thông số giọng đọc
type: production
updated: 2026-10-19
sources: [raw/assets/video-doi-thu/]
---

# Thông số giọng đọc IronBehemoth

Giọng kênh là giọng riêng (thư viện TTS có giấy phép thương mại, hoặc giọng tự thu/giọng thuê có đồng ý clone). **Không clone giọng người dẫn của đối thủ.**

## Giọng kênh hiện tại (từ 2026-10-19)
- **IB-Clone `clone_2700943`** — giọng anh Aron (chủ kênh) tự thu, clone trên ai33 (MiniMax speech-02-hd). Mẫu: `IronBehemoth-Videos/_voice_clone/thuandv_clone_29s.wav` (29 s, sạch, mono).
- Lý do đổi: khán giả tập 002 chê giọng Russ "robotic"; Russ phải hạ speed 0.85 + atempo nên nghe phẳng.
- Đo trên tập 004: 155 wpm ở speed 1.0, khớp chữ 99,1%. Quy trình đọc theo chương + thẻ `<break>`: xem skill ib-build bước 2.

## Số đo tham chiếu (Blue Paw Print, đo 2026-10-11)
| Video | Thời lượng | Số từ | Tốc độ | Loudness (file mix) | LRA |
|---|---|---|---|---|---|
| Inside the King Tiger | 30:43 | 4.355 | 141.8 wpm | -11.4 LUFS | 5.3 LU |
| Inside the Sturmtiger | 25:04 | 3.710 | 148.0 wpm | -14.0 LUFS | 3.8 LU |

File voice.mp3 có lẫn nhạc/SFX (gần như không có khoảng lặng < -35 dB), nên loudness là của bản mix.

## Mục tiêu cho kênh
- Tốc độ 142–148 wpm (khớp khung 2.320–2.460 từ / 16:30).
- Giọng nam trầm, điềm tĩnh, kể chuyện tài liệu; tiếng Anh Mỹ hoặc Anh.
- Ngắt câu: xuống dòng mỗi câu trong script để TTS nghỉ tự nhiên ~0.3–0.5s.
- Hậu kỳ voice: high-pass 80 Hz, de-ess nhẹ, compressor 3:1, EQ ấm (+2 dB quanh 150–200 Hz), reverb phòng rất nhẹ.
- Mix cuối: -14 LUFS integrated, true peak ≤ -1 dBTP, nhạc nền thấp hơn giọng 15–20 dB, ducking khi có lời.
- Lệnh chuẩn hóa: `ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=6 out.wav`

## Ứng viên giọng ai33 (ElevenLabs, thử 2026-10-11)
Đoạn thử: hook Tiger I, 111 từ, speed=1. Tốc độ đọc liền (chưa tính nghỉ giữa đoạn) cao hơn trung bình cả video nên speed đề xuất là mức khởi đầu, đo lại trên script đầy đủ.

| Mã | voice_id | Mô tả | Thời lượng | wpm @1.0 | speed đề xuất (~145 wpm) |
|---|---|---|---|---|---|
| Leo | elevenlabs_cOHUo8FosWk7BqQhx8nk | Mỹ, trung niên, documentary/broadcast | 36.9s | 181 | 0.85 + nghỉ 0.4s giữa đoạn |
| Spartan | elevenlabs_S75jVZ0i3J6Xa5BbK8CE | Mỹ, baritone, historical narration | 34.9s | 191 | 0.80 + nghỉ 0.4s |
| Russ | elevenlabs_t0eCaS57KWbQQc1wRkah | Mỹ, baritone trầm, nhịp chắc | 34.1s | 196 | 0.80 + nghỉ 0.4s |
| Grant Gravitas | elevenlabs_VC6vCXhVaI8BZefRtXZV | Anh, lớn tuổi, kiểu BBC | 43.5s | 153 | 1.0 |

Model ai33 dùng: eleven_multilingual_v2. Chi phí ~667 credit / 111 từ.
