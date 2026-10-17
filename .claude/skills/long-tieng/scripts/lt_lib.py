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
