# Đoạn JS chạy trong Chrome (Claude in Chrome) cho IronBehemoth

Máy Mac (device shell) và container không ra được mạng ngoài, nên mọi thứ cần mạng (ai33, Pexels, Wikimedia, Mixkit) chạy bằng `fetch` trong tab Chrome, rồi tải về `~/Downloads` thành **một file JSON bundle** và giải bằng `ib_unbundle.py`.

Quy tắc chung
- Chrome chặn tải tự động lần thứ hai trong cùng một tab → mỗi bundle mở một tab mới (ví dụ `https://example.org`) rồi chạy hàm tải.
- Không ghi key ra màn hình, log hay file. Key đọc từ `IronBehemoth/.secrets/ai33.env` (device shell) và chỉ đưa vào biến JS khi chạy.
- Bundle: `{"files": {"tên.ext": "<base64>"}}` → `python3 tools/video/ib_unbundle.py ~/Downloads/<bundle>.json <thư mục đích>`.

## Hàm tải bundle (dán trước các đoạn khác)
```js
window.ibSave = (name, obj) => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(obj)], {type: 'application/json'}));
  a.download = name; document.body.appendChild(a); a.click(); a.remove();
};
window.ibB64 = async (blob) => {
  const buf = new Uint8Array(await blob.arrayBuffer()); let s = '';
  for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
  return btoa(s);
};
```

## ai33 TTS (giọng đọc + transcript có timestamp từng từ)
- Endpoint: `POST https://api.ai33.pro/v3/text-to-speech` (FormData), poll `GET https://api.ai33.pro/v3/task/{task_id}` tới khi `status=done`; kết quả có `metadata.audio_url` và `metadata.json_url` (transcript từng từ).
- Giọng kênh: Russ `elevenlabs_t0eCaS57KWbQQc1wRkah`, model `eleven_multilingual_v2`, speed khởi đầu 0.85 (đo lại wpm, mục tiêu 142–148).
- Nếu API trả lỗi tên trường, đọc nội dung lỗi và sửa tên trường; không đoán lại liên tục quá 2 lần, báo anh Aron.
```js
async function ibTTS(KEY, VOICE, text, speed = 0.85) {
  const fd = new FormData();
  fd.append('voice_id', VOICE); fd.append('text', text); fd.append('model_id', 'eleven_multilingual_v2');
  fd.append('speed', String(speed)); fd.append('with_transcript', 'true');
  const H = {'xi-api-key': KEY};
  const r = await (await fetch('https://api.ai33.pro/v3/text-to-speech', {method: 'POST', headers: H, body: fd})).json();
  const id = r.task_id || r.id || (r.data && r.data.task_id); if (!id) return {error: r};
  for (let i = 0; i < 180; i++) {
    await new Promise(z => setTimeout(z, 5000));
    const t = await (await fetch('https://api.ai33.pro/v3/task/' + id, {headers: H})).json();
    const st = (t.status || (t.data && t.data.status) || '').toLowerCase();
    if (st === 'done' || st === 'completed' || st === 'success') return t;
    if (st === 'failed' || st === 'error') return {error: t};
  }
  return {error: 'timeout', id};
}
// Sau khi có t: tải audio + json rồi đóng gói
async function ibVoiceBundle(t, name) {
  const m = t.metadata || (t.data && t.data.metadata) || t;
  const audio = await (await fetch(m.audio_url)).blob();
  const tr = await (await fetch(m.json_url)).json();
  ibSave(name, {audio_b64: await ibB64(audio), transcript: tr});
}
```
Giải: `ib_unbundle.py ~/Downloads/<name>.json outputs/NNN_slug/audio` → `voice.mp3`, `voice.json`.
Script dài (~2.400 từ) gửi một lần được; nếu bị giới hạn ký tự thì chia 3–4 phần theo chương, ghép mp3 bằng ffmpeg và cộng dồn timestamp.

## Pexels (footage/ảnh, nếu anh nhờ tìm)
- Tìm: mở `https://www.pexels.com/search/videos/<từ khóa>/?orientation=landscape`, đọc id từ link `/video/<slug>-<id>/`.
- Tải: điều hướng tab tới `https://www.pexels.com/download/video/<id>/?h=1080&w=1920` → file về `~/Downloads/<id>-hd_1920_1080_*.mp4`, đổi tên thành `<asset_id>.mp4`.

## Wikimedia Commons (ảnh tư liệu, ảnh tham chiếu xe)
```js
async function ibCommons(files, name) {  // files: ['File:Sturmtiger in Munster.jpg', ...]
  const out = {};
  for (const f of files) {
    const q = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1920&titles=' + encodeURIComponent(f);
    const j = await (await fetch(q)).json(); const p = Object.values(j.query.pages)[0].imageinfo[0];
    out[f.replace(/^File:/, '').replace(/[^\w.-]+/g, '_')] = await ibB64(await (await fetch(p.thumburl || p.url)).blob());
  }
  ibSave(name, {files: out});
}
```
Ghi tác giả + giấy phép (`extmetadata.Artist`, `LicenseShortName`) vào `credits.md`.

## Mixkit SFX
- Preview mp3: `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3` (mở tab `https://assets.mixkit.co/` rồi fetch để tránh CORS).
- Bộ SFX đã có sẵn trong `tools/video/common/sfx/` (mk_*.mp3): hatch_slam, big_impact, metal_explosion, rocket_ignition, rocket_whoosh, explosion_battle, war_field_explosion, debris_explosion, whoosh_deep_impact, terror_sweep, explosion_afar, heartbeat_impact, trailer_riser, war_ambience, metal_hit, gear_lock, mech_move, distant_thunder, bomb_battle, rocket_rumble, heartbeat_mystery.

## YouTube Audio Library (nhạc nền)
Studio → Thư viện âm thanh → tìm từ khóa ("epic", "dark cinematic", "tension") → rê chuột vào dòng → bấm Tải xuống (mở tab mới). Ghi tên bài + tác giả vào `credits.md`. Bài đã dùng: "Density & Time" (Twin Lynches).

## Google Flow (Veo) — tải ảnh tham chiếu lên khi không có quyền upload file
1. Mở bảng thêm thành phần (nút +), chạy:
```js
window._dt = new DataTransfer();
for (const [u, n] of [[URL1, 'tank_ref1.jpg'], [URL2, 'tank_ref2.jpg']]) {
  const b = await (await fetch(u)).blob(); window._dt.items.add(new File([b], n, {type: b.type || 'image/jpeg'}));
}
const orig = HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click = function () {
  if (this.type === 'file') { this.files = window._dt.files; this.dispatchEvent(new Event('input', {bubbles: true})); this.dispatchEvent(new Event('change', {bubbles: true})); return; }
  return orig.call(this);
};
```
2. Bấm "Tải nội dung lên" → ảnh xuất hiện ở "Tệp tải lên" → chọn ảnh → "Thêm vào câu lệnh" → gõ prompt → bấm mũi tên.
(URL ảnh lấy từ `upload.wikimedia.org/.../1280px-...` — fetch được trong trang Flow.)
3. Tải clip: mở clip → biểu tượng tải xuống → 720p. File Flow có ngôi sao watermark góc phải dưới → ghi `provider=flow` trong CSV để `ib_build.py` tự xóa. Clip Muse không cần.
