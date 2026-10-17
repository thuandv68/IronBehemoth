"""Bước 4 — trộn giọng đã khớp với nhạc + SFX của bản gốc, xuất file upload và phụ đề.

Dùng:  python lt_04_tron.py "<thư mục tập>" --ngon-ngu tieng_anh
       python lt_04_tron.py "<thư mục tập>" --tat-ca          # mọi ngôn ngữ đã qua bước 3
Nền:   <V>/_tmp_skill/: <tên V>_nhac.flac + _sfx.flac → nếu thiếu: <tên V>_nen.* (nền trộn sẵn) → không có thì dừng.
Ra:    voice/long_tieng/<tên V>_<ngôn ngữ>.mp3 (giọng + nhạc + SFX) · .srt
       --chi-srt: chỉ làm lại .srt (cắt theo nghĩa, mốc bám khoảng lặng thật của giọng), không trộn lại mp3.
Trộn bằng đúng loc_tron_am() của tron_am.py — y hệt bản gốc.
"""
import argparse, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

import numpy as np

import lt_lib as T

CAU = re.compile(r"(?<=[.?!…。！？؟])\s*")
DAU_NGAT = re.compile(r"[,;:—–、，；：،؛]")      # cắt NGAY SAU các dấu này
TU_TOI_THIEU = 16                               # vế cắt ra ngắn hơn (độ rộng) thì không nhận — tránh mẩu cụt
# Từ không được đứng CUỐI cue / cuối dòng: mạo từ, giới từ, liên từ, loại từ… (gộp mọi ngôn ngữ, chữ thường).
# Đứng cuối là treo một cụm chưa trọn: "một con / tàu", "nếu / dựng đứng lên", "the / ship".
TU_NOI = set("""
một những các của và là nếu khi mà để với cho trong từ đến rằng thì nhưng hay hoặc vì bởi con cái chiếc
đã sẽ đang được bị không rất này nên còn cũng như theo về tới ở trên dưới sau trước
a an the of to in on at for with and or but if that which who whom whose from by as its their his her our
this these those is are was were will would can could has have had not into than when while because so
el la los las un una unos unas de del y o u que en con por para si al su sus lo se e ni sin sobre como
os as um uma uns umas da do das dos em no na nos nas com ao à às pelo pela seu sua mais
le les une des du et ou qui au aux pour avec dans par sur ce cette ces son sa ses leur d' l' qu'
der die das den dem des ein eine einen einem einer und oder dass wenn mit von zu im auf für aus bei nach
ist sind war wird nicht wie als
yang dan di ke dari untuk dengan sebuah seorang jika karena bahwa atau pada oleh akan adalah
في من على إلى أن إذا التي الذي و أو عن مع
""".split())
# Liên từ mở vế mới: cắt NGAY TRƯỚC chúng là chỗ ngắt tự nhiên.
TU_MO = set("và nhưng nếu khi mà rằng vì để and but if when that which because while que pero si cuando porque "
            "mas quando et mais quand und aber wenn weil dass dan tetapi jika ketika karena bahwa".split())
TRO_TU_JA = set("はがをにでとへもや")
TRAN_KHONG_DAU = 130                            # câu không có dấu để cắt: tới mức này vẫn để nguyên một cue
CAT_KHOANG_TRANG = []                           # câu buộc phải cắt ở khoảng trắng — báo cho chủ kênh xem
LANG_TOI_THIEU = 0.12                          # khoảng lặng trong giọng đủ dài để coi là chỗ ngắt (giây)


def rong(s):
    """Độ rộng hiển thị: chữ CJK tính 2."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _tu(s, cuoi=True):
    t = s.split()
    return (t[-1] if cuoi else t[0]).strip("\"'«»“”()[]¿¡").lower() if t else ""


def _diem(s, i, muc):
    """Điểm phạt khi cắt s tại i (nhỏ = tốt): lệch mức cân + treo từ nối; thưởng cắt sau dấu câu / trước liên từ."""
    trai, phai = s[:i].rstrip(), s[i:].lstrip()
    p = 0.5 * abs(rong(trai) - muc)
    if " " in s:
        p += 40 if _tu(trai) in TU_NOI else 0
        p -= 25 if _tu(phai, False) in TU_MO else 0
    else:
        p += 0 if trai[-1:] in TRO_TU_JA else 12
    return p - (12 if DAU_NGAT.search(trai[-1:]) else 0)


def _cho_cat(s):
    return [m.start() for m in re.finditer(" ", s)] if " " in s else list(range(1, len(s)))


def chia_cau(cau, tran):
    """Cắt câu dài thành các cue ≤ tran theo NGHĨA, không theo số chữ (chủ kênh 2026-10-08: "một con / tàu" là gãy).
    1. Có dấu , ; : → cắt ở dấu MUỘN NHẤT mà vế trước còn vừa tran: vế chêm khép trọn trong một cue
       ("dài đến mức, nếu dựng đứng lên, / nó sẽ khiến…" — cắt ở dấu phẩy đầu là treo "đến mức").
    2. Không có dấu phù hợp → cắt ở khoảng trắng gần mức chia đều, phạt nặng khi treo từ nối cuối cue."""
    cau = cau.strip()
    if rong(cau) <= tran:
        return [cau]
    tot = None
    for tr in (tran, TRAN_KHONG_DAU):              # vế trước vừa một cue chuẩn; không được thì nới tới cue dài
        for m in DAU_NGAT.finditer(cau):
            if TU_TOI_THIEU <= rong(cau[:m.end()].strip()) <= tr and rong(cau[m.end():].strip()) >= TU_TOI_THIEU:
                tot = m.end()
        if tot is not None:
            break
    if tot is None and rong(cau) <= TRAN_KHONG_DAU:
        return [cau]                                # hơi dài vẫn hơn cắt giữa cụm từ
    if tot is None:
        n = -(-rong(cau) // tran)
        muc = rong(cau) / n
        ung = [i for i in _cho_cat(cau)
               if TU_TOI_THIEU <= rong(cau[:i]) <= tran and TU_TOI_THIEU <= rong(cau[i:].strip()) <= TRAN_KHONG_DAU * (n - 1)]
        ung = ung or [i for i in _cho_cat(cau) if rong(cau[:i]) <= tran] or [len(cau) // 2]
        tot = min(ung, key=lambda i: _diem(cau, i, muc))
        CAT_KHOANG_TRANG.append(f"{cau[:tot].strip()}  ⟋  {cau[tot:].strip()}")
    return [cau[:tot].strip()] + chia_cau(cau[tot:], tran)


def gap_hai_dong(s, tran=50):
    """Xuống dòng trong cue CHỈ ở dấu câu (, ; :) — hai dòng đều ≤ tran. Không có dấu hợp lệ → để một dòng,
    trình phát YouTube tự xuống dòng theo bề rộng màn hình. Ngắt ở khoảng trắng bằng luật là gãy từ ghép
    ("đánh / chìm", "càng / lớn" — chủ kênh 2026-10-08), máy không phân biệt được nếu không hiểu nghĩa."""
    if rong(s) <= 42:
        return s
    ung = [m.end() for m in DAU_NGAT.finditer(s) if rong(s[:m.end()]) <= tran and rong(s[m.end():].strip()) <= tran]
    if not ung:
        return s
    i = min(ung, key=lambda i: abs(rong(s[:i]) - rong(s) / 2))
    return s[:i].rstrip() + "\n" + s[i:].lstrip()


def _lang(x):
    """Các khoảng lặng bên trong giọng (giây): [(đầu, cuối)]."""
    t, ra, i = T.co_tieng(x), [], 0
    while i < len(t):
        if not t[i]:
            j = i
            while j < len(t) and not t[j]:
                j += 1
            if i > 0 and j < len(t) and (j - i) / T.SR >= LANG_TOI_THIEU:
                ra.append((i / T.SR, j / T.SR))
            i = j
        else:
            i += 1
    return ra


def moc_cue(x, manh):
    """Mốc (giây, tính từ đầu khối) cho từng mảnh phụ đề, bám KHOẢNG LẶNG THẬT trong giọng đã khớp:
    mốc dự kiến theo tỉ lệ chữ → hút về khoảng lặng gần nhất (ưu tiên lặng dài). Không có lặng hợp lệ → giữ mốc tỉ lệ."""
    co = np.flatnonzero(T.co_tieng(x))
    v0, v1 = (co[0] / T.SR, co[-1] / T.SR) if len(co) else (0.0, len(x) / T.SR)
    tong = sum(rong(m) for m in manh) or 1
    lang = [z for z in _lang(x) if v0 < z[0] and z[1] < v1]
    moc, truoc, cd = [v0], v0, 0
    for j, m in enumerate(manh[:-1]):
        cd += rong(m)
        du = v0 + (v1 - v0) * cd / tong
        con = len(manh) - 1 - j                     # số mảnh còn lại sau mốc này
        ung = [z for z in lang if truoc + 0.6 < (z[0] + z[1]) / 2 < v1 - 0.6 * con
               and abs((z[0] + z[1]) / 2 - du) <= max(1.5, 0.3 * (v1 - v0) / len(manh))]
        if ung:
            z = min(ung, key=lambda z: abs((z[0] + z[1]) / 2 - du) - 1.5 * (z[1] - z[0]))
            lang.remove(z)
            du = (z[0] + z[1]) / 2
        moc.append(max(du, truoc + 0.3))
        truoc = moc[-1]
    return moc + [v1 + 0.3]


def lam_srt(khoi, dich, d):
    cue = []
    for k in khoi:
        manh = []
        for c in [x.strip() for x in CAU.split(dich[k["id"]][1]) if x.strip()]:
            manh += chia_cau(c, 84)
        moc = moc_cue(T.doc_am(d / "khop" / f"{k['id']}.wav"), manh)
        cue += [(k["a"] + a, k["a"] + b, gap_hai_dong(m)) for m, a, b in zip(manh, moc, moc[1:])]
    return "\n".join(f"{i}\n{T.gio_srt(a)} --> {T.gio_srt(b)}\n{s}\n" for i, (a, b, s) in enumerate(cue, 1))


def chon_nen(v):
    """Chọn nền âm, theo thứ tự. Mọi file nền nằm NGOÀI CÙNG <V>/_tmp_skill/ — không tìm trong voice/.
    1. _tmp_skill/<V>_nhac.flac (+ _sfx.flac) — nhạc chưa duck → duck theo giọng mới (loc_tron_am).
    2. _tmp_skill/<V>_nen.<flac|wav|mp3|m4a> — nền trộn sẵn (SFX lẫn nhạc ĐÃ duck theo giọng gốc): dùng nguyên làm
       nền, không duck lại, không ghép thêm nhạc (tránh hai lớp nhạc).
    Không có cả hai → dừng.
    Trả dict(kieu, T, nhac, sfx | nen)."""
    goc = v / "_tmp_skill"
    nhac, sfx = goc / f"{v.name}_nhac.flac", goc / f"{v.name}_sfx.flac"
    if nhac.is_file():
        if not sfx.is_file():
            T.dung(f"có {nhac.name} nhưng thiếu {sfx.name} — cách 1 cần cả hai file, xem lại {goc}")
        dai = T.thoi_luong(nhac)
        if abs(T.thoi_luong(sfx) - dai) > 0.1:
            T.dung("nhạc và SFX lệch thời lượng — xuất lại cho bằng nhau (= dài video)")
        print(f"nền âm: {nhac.name} + {sfx.name} (bóp nhạc theo giọng mới)")
        return dict(kieu="nhac", T=dai, nhac=nhac, sfx=sfx)
    nen = [p for p in goc.glob(f"{v.name}_nen.*") if p.suffix.lower() in (".flac", ".wav", ".mp3", ".m4a")]
    if len(nen) > 1:
        T.dung(f"có nhiều file nền {[p.name for p in nen]} — giữ đúng một")
    if nen:
        print(f"nền âm: {nen[0].name} (nền tách sẵn, dùng nguyên — không bóp lại, không ghép thêm nhạc)")
        return dict(kieu="nen", T=T.thoi_luong(nen[0]), nen=nen[0])

    T.dung(f"chưa có nền âm trong {goc}: đặt {v.name}_nhac.flac + {v.name}_sfx.flac, hoặc {v.name}_nen.flac "
           f"(dài đúng bằng video) rồi chạy lại — xem quy-tac.md §3")


def loc_nen_tach(T_, sr, lufs):
    """Giọng mới + nền tách sẵn (nhạc đã bóp theo giọng gốc). Cùng fade + loudnorm với loc_tron_am, bỏ sidechain."""
    return [f"[0:a]atrim=0:{T_:.3f},asetpts=PTS-STARTPTS,aresample={sr},afade=t=out:st={T_ - 0.5:.3f}:d=0.5[vo]",
            f"[1:a]aresample={sr}[nn]",
            f"[vo][nn]amix=inputs=2:normalize=0:duration=first,afade=t=out:st={T_ - 0.6:.3f}:d=0.6,"
            f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample={sr}[a]"]


def kiem_xong(v, nn, ch, khoi):
    d = T.tm(v) / nn
    dich = T.doc_dich(T.file_dich(v, nn))
    bao = json.loads((d / "bao_cao.json").read_text(encoding="utf-8")) if (d / "bao_cao.json").is_file() else []
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").is_file() else {}
    chua = [k["id"] for k in khoi
            if not str(meta.get(k["id"], {}).get("khop", "")).startswith(T.bam(dich[k["id"]][1]) + T.chu_ky(ch) + "|")]
    if len(bao) != len(khoi) or not all(b["dat"] for b in bao) or chua:
        T.dung(f"{nn}: bước 3 chưa đạt hết — khối chưa khớp: {chua[:10]}. Chạy lt_03_doc_khop.py tới khi không còn VUOT")


def tron(v, nn, ch, khoi, nen):
    d = T.tm(v) / nn
    dich = T.doc_dich(T.file_dich(v, nn))

    dai = nen["T"]
    g = np.zeros(int(round(dai * T.SR)), np.float32)
    for k in khoi:
        x = T.doc_am(d / "khop" / f"{k['id']}.wav")
        i = int(round(k["a"] * T.SR))
        g[i:i + len(x)] += x[:max(0, len(g) - i)]
    giong = d / "giong_khop.wav"
    T.ghi_am(g, giong)

    L = T.tron_am()
    out = T.ten_ra(v, nn, ".mp3")
    out.parent.mkdir(parents=True, exist_ok=True)
    if nen["kieu"] == "nhac":
        # sidechain nhạc theo GIỌNG MỚI, đúng như bản gốc sidechain theo giọng gốc
        vao = ["-i", str(nen["nhac"]), "-i", str(nen["sfx"])]
        loc = ";".join(L.loc_tron_am(dai, T.SR, "[0:a]", "[1:a]", "[2:a]"))
    else:
        vao = ["-i", str(nen["nen"])]
        loc = ";".join(loc_nen_tach(dai, T.SR, L.LUFS_RA))
    subprocess.run([L.FF, "-v", "error", "-y", "-i", str(giong), *vao,
                    "-filter_complex", loc, "-map", "[a]", "-t", f"{dai:.3f}", "-c:a", "libmp3lame",
                    "-b:a", ch["bitrate_ra"], str(out)], check=True)
    T.ten_ra(v, nn, ".srt").write_text(lam_srt(khoi, dich, d),encoding="utf-8")

    o = subprocess.run([L.FF, "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    lufs = [l for l in o.splitlines() if l.strip().startswith("I:")]
    dai_ra = T.thoi_luong(out)
    canh = "" if abs(dai_ra - dai) <= 0.1 else f"  ⚠️ lệch video {dai_ra - dai:+.2f} s"
    print(f"✓ {out.name} · {dai_ra:.2f} s (video {dai:.2f} s) · {lufs[-1].split()[1] if lufs else '?'} LUFS{canh}")
    print(f"✓ {T.ten_ra(v, nn, '.srt').name}")
    bao_cat_khoang_trang()
    return not canh


def bao_cat_khoang_trang():
    if CAT_KHOANG_TRANG:
        print(f"⚠️  {len(CAT_KHOANG_TRANG)} câu dài không có dấu phẩy, phụ đề phải cắt ở khoảng trắng — nên xem lại:")
        for c in CAT_KHOANG_TRANG:
            print(f"   · {c}")
    CAT_KHOANG_TRANG.clear()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ngon-ngu")
    g.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--chi-srt", action="store_true", help="chỉ làm lại phụ đề .srt, không trộn lại mp3")
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    khoi = T.doc_khoi(v)
    ds = [nn for nn in ch["ds_ngon_ngu"] if (T.tm(v) / nn / "bao_cao.json").is_file()] if a.tat_ca else [a.ngon_ngu]
    if not ds:
        T.dung("chưa ngôn ngữ nào qua bước 3")
    for nn in ds:            # kiểm đủ mọi ngôn ngữ trước khi tốn công ghép nền
        kiem_xong(v, nn, ch, khoi)
    if a.chi_srt:
        for nn in ds:
            srt = lam_srt(khoi, T.doc_dich(T.file_dich(v, nn)), T.tm(v) / nn)
            T.ten_ra(v, nn, ".srt").write_text(srt, encoding="utf-8")
            print(f"✓ {T.ten_ra(v, nn, '.srt').name}")
            bao_cat_khoang_trang()
        return 0
    nen = chon_nen(v)
    ok = all([tron(v, nn, ch, khoi, nen) for nn in ds])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
