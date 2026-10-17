"""Bước 2 — CỔNG kiểm bản dịch của một ngôn ngữ, trước khi tốn credit đọc voice.

Dùng:  python lt_02_kiem_dich.py "<thư mục tập>" --ngon-ngu tieng_anh
Kiểm:  _tmp_skill/long-tieng/<ngôn ngữ>/<tên V>_<ngôn ngữ>.txt (bản dịch theo khối)  +  voice/long_tieng/<tên V>_<ngôn ngữ>_tieu_de_mo_ta.txt
Thoát 0 = PASS · 1 = có vi phạm · 2 = lỗi đầu vào.
"""
import argparse, re
from pathlib import Path

import lt_lib as T

SO = re.compile(r"[0-9٠-٩０-９]")
MOC = re.compile(r"^(\d{2}):(\d{2})\s+(\S.*)$")


def tach_mo_ta(s):
    """(tiêu đề, từ khoá, [đoạn văn], [(mốc, nhãn)]) từ file tiêu đề + mô tả."""
    tieu_de = re.search(r"^TITLE:\s*(.*)$", s, re.M)
    tu_khoa = re.search(r"^TU_KHOA:\s*(.*)$", s, re.M)
    than = s.split("DESCRIPTION:", 1)[1] if "DESCRIPTION:" in s else ""
    van, moc = [], []
    for d in than.strip().split("\n"):
        m = MOC.match(d.strip())
        if m:
            moc.append((m.group(1) + ":" + m.group(2), m.group(3)))
        else:
            van.append(d)
    doan = [x for x in re.split(r"\n\s*\n", "\n".join(van).strip()) if x.strip()]
    return (tieu_de.group(1).strip() if tieu_de else "", tu_khoa.group(1).strip() if tu_khoa else "", doan, moc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    ap.add_argument("--ngon-ngu", required=True)
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    nn = a.ngon_ngu
    if nn not in ch["ds_ngon_ngu"]:
        T.dung(f"ngôn ngữ '{nn}' không có trong quy-tac.md: {list(ch['ds_ngon_ngu'])}")
    khoi = T.doc_khoi(v)
    vp = []

    # ---- bản dịch theo khối
    f = T.file_dich(v, nn)
    if not f.is_file():
        T.dung(f"chưa có {f}")
    dich = T.doc_dich(f)
    if [k["id"] for k in khoi] != list(dich):
        thieu = [k["id"] for k in khoi if k["id"] not in dich]
        thua = [x for x in dich if x not in {k["id"] for k in khoi}]
        vp.append(f"danh sách khối lệch khoi.json — thiếu {thieu[:8]} · thừa {thua[:8]} · hoặc sai thứ tự")
    for k in khoi:
        if k["id"] not in dich:
            continue
        dau, chu = dich[k["id"]]
        if dau != T.dau_khoi(k):
            vp.append(f"{k['id']}: dòng đầu khối bị sửa — giữ nguyên `{T.dau_khoi(k)}`")
        if not chu:
            vp.append(f"{k['id']}: rỗng")
        elif chu == k["goc"]:
            vp.append(f"{k['id']}: chưa dịch (trùng nguyên văn bản gốc)")
        if SO.search(chu):
            vp.append(f"{k['id']}: còn chữ số `{SO.search(chu).group(0)}` — viết số bằng chữ")
        if "<#" in chu or "###" in chu:
            vp.append(f"{k['id']}: còn marker hoặc dấu ###")

    # ---- tiêu đề + mô tả
    fm = T.ten_ra(v, nn, "_tieu_de_mo_ta.txt")
    nguon = (T.tm(v) / "nguon_tieu_de_mo_ta.txt").read_text(encoding="utf-8")
    _, _, doan_g, moc_g = tach_mo_ta(nguon)
    if not fm.is_file():
        vp.append(f"chưa có {fm.name}")
    else:
        td, kw, doan, moc = tach_mo_ta(fm.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
        if not td:
            vp.append("tiêu đề: thiếu dòng TITLE:")
        if moc_g:
            so_lan = int(T.frontmatter(T.FILE_CAU_HINH).get("so_lan_tu_khoa") or 0)   # 0 = không kiểm luật từ khoá
            if so_lan and not kw:
                vp.append("mô tả: thiếu dòng TU_KHOA:")
            if len(doan) != len(doan_g):
                vp.append(f"mô tả: {len(doan)} đoạn, bản gốc {len(doan_g)}")
            if [m for m, _ in moc] != [m for m, _ in moc_g]:
                vp.append(f"mô tả: mốc {[m for m, _ in moc]} khác bản gốc {[m for m, _ in moc_g]} — giữ nguyên mốc")
            if so_lan and kw:
                n = " ".join(doan).lower().count(kw.lower())
                if n != so_lan:
                    vp.append(f"mô tả: từ khoá '{kw}' xuất hiện {n} lần trong phần văn, cần {so_lan}")
                if moc and not moc[0][1].lower().startswith(kw.lower()):
                    vp.append(f"mô tả: nhãn dòng 00:00 không mở đầu bằng '{kw}'")

    # ---- dự báo độ dài từ sổ tốc độ đọc (wiki) — chỉ CẢNH BÁO, để agent chỉnh bản dịch TRƯỚC khi tốn credit
    cps = T.toc_do(nn)
    if cps is None:
        print(f"dự báo   : chưa có số đo tốc độ đọc của {nn} trong sổ — lần đọc đầu sẽ tự ghi")
    else:
        # Chấm ĐÚNG luật lt_03 (chủ kênh 2026-10-08, sau 0928): tốc độ chương + lặng dư + ngưỡng nén, qua chung hàm
        # T.toc_chuong / T.vung_dat. Bản cũ chỉ chặn dưới ở 1−gian (0,70) trong khi lt_03 bắt "viết dài thêm" từ
        # ~0,77–0,85 → khối lọt dự báo rồi phải đọc lại. Biên an toàn bien_du_bao: tốc độ đọc thật dao động theo khối.
        bien = float(ch.get("bien_du_bao") or 0.04)
        du = {}                                  # id -> (tỉ lệ dự báo, khung lời)
        for k in khoi:
            if k["id"] in dich:
                kl = T.khung_loi(k["b"] - k["a"], ch)
                du[k["id"]] = (len(dich[k["id"]][1]) / cps / kl, kl)
        lech = []
        for c in sorted({k["chuong"] for k in khoi}):
            ids = [k["id"] for k in khoi if k["chuong"] == c and k["id"] in du]
            if not ids:
                continue
            tc = T.toc_chuong([du[i][0] for i in ids], ch)
            thap, cao = T.vung_dat(tc, ch, bien)
            dich_tl = (thap + cao) / 2                   # nhắm GIỮA vùng đạt, không sát mép
            for i in ids:
                tl, kl = du[i]
                if not thap <= tl <= cao:
                    lech.append((i, tl, c, tc, len(dich[i][1]), round(cps * kl * dich_tl)))
        print(f"dự báo   : {cps:.2f} ký tự/giây lời (sổ) · lời/khung dự báo trung vị "
              f"{float(T.np.median([x[0] for x in du.values()])):.2f} · biên an toàn {bien:.2f} · "
              f"{len(lech)} khối dự báo ngoài vùng đạt")
        for i, tl, c, tc, n, nen_viet in lech:
            huong = "NGẮN lại" if tl > 1 else "DÀI thêm"
            print(f"CANH BAO: {i} dự báo {tl:.2f} (chương {c} tốc độ {tc:.2f}) — hiện {n} ký tự, viết {huong} "
                  f"khoảng {nen_viet} ký tự")

    so_ky_tu = sum(len(dich[k["id"]][1]) for k in khoi if k["id"] in dich)
    print(f"bản dịch : {f.name} · {len(dich)} khối · {so_ky_tu} ký tự (gốc {sum(len(k['goc']) for k in khoi)})")
    for x in vp:
        print(f"VI PHAM: {x}")
    print(f"Cong: {len(vp)} vi pham")
    return 1 if vp else 0


if __name__ == "__main__":
    raise SystemExit(main())
