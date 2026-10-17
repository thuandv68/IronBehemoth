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
