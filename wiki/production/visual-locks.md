---
title: Visual locks cho prompt AI
type: production
updated: 2026-10-11
sources: []
---

# Visual locks

Mỗi beat AI dán đủ các khối lock để giữ nhất quán giữa ~62 clip. Viết bằng tiếng Anh.

## STYLE (cố định toàn kênh)
```
STYLE: cinematic photoreal military documentary, 35mm film look, shallow depth of field, muted steel and olive palette with warm orange practical light accents, subtle film grain, slow deliberate camera moves, no text, no logos, no watermarks.
```

## CUTAWAY (dùng cho cảnh "nhìn xuyên" nội thất)
```
CUTAWAY: museum-quality cutaway reconstruction, pure black void background, one side of the hull and turret removed to reveal the interior, interior lit by warm orange work lights, camera glides slowly along the cut plane.
```

## TANK (mỗi tập một khối — điền khi làm tập)
```
TANK: [exact name and variant], [hull shape], [turret shape], [gun + muzzle brake], [road wheels / track layout], [paint scheme], [national markings], [distinctive details]. Exact proportions, historically accurate.
```

## CREW (mỗi tập)
```
CREW: [nationality] tank crew, [year], [uniform], [headgear + headset], [age range], grime and sweat, cramped posture.
```

## AUDIO
```
AUDIO: diegetic engine rumble and metallic clanks only, no music, no dialogue.
```

## NEG
```
NEG: no swastikas, no modern vehicles in historical scenes, no extra gun barrels, no warped tracks, no floating parts, no text, no faces looking at camera.
```

## Timeline clip 8s
`0–2s` thiết lập · `2–6s` hành động chính · `6–8s` giữ khung/chuyển tiếp.

## Ảnh khởi đầu (start frame)
Với cảnh cutaway và cảnh xe toàn thân: tạo ảnh tĩnh trước bằng image model với khối TANK, kiểm tra đúng biến thể, rồi image-to-video trên Flow. Lưu ảnh chuẩn vào `raw/assets/<xe>/` để tái dùng.
