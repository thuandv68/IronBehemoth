"""Bước 1 — chia khối nghĩa từ SRT gốc, gán chữ kịch bản cho từng khối. Chạy MỘT lần, dùng chung cho mọi ngôn ngữ.

Dùng:  python lt_01_chia_khoi.py "<thư mục tập>" [--ghi-de]
Sinh:  _tmp_skill/long-tieng/khoi.json · khoi_goc.txt (bản ngôn ngữ gốc cho agent dịch) · nguon_tieu_de_mo_ta.txt
"""
import argparse, json, re, statistics
from pathlib import Path

import lt_lib as T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("v")
    ap.add_argument("--ghi-de", action="store_true")
    a = ap.parse_args()
    v = Path(a.v).resolve()
    T.kiem_kenh(v)
    ch = T.cau_hinh()
    d = T.tm(v)
    if (d / "khoi.json").exists() and not a.ghi_de:
        T.dung(f"{d / 'khoi.json'} đã có — các bản dịch đang bám theo nó. Chỉ dùng --ghi-de khi chắc chắn làm lại từ đầu")

    script = T.tim_script(v).read_text(encoding="utf-8")
    if "SCRIPT:" not in script:
        T.dung("kịch bản không có khối SCRIPT:")
    than = script.split("SCRIPT:", 1)[1]
    srt = v / "voice" / f"{v.name}.srt"
    if not srt.is_file():
        T.dung(f"chưa có {srt} — cần voice gốc + SRT trước")
    cue = T.doc_srt(srt)

    khoi = T.chia_khoi(cue, ch)
    so_marker = len(T.MARKER.findall(than))
    if khoi[-1]["chuong"] != so_marker:
        T.dung(f"đếm được {khoi[-1]['chuong']} ranh giới chương trong SRT nhưng kịch bản có {so_marker} marker")
    khop = T.gan_chu(khoi, cue, than)
    if khop < 0.9:
        T.dung(f"chỉ khớp {khop:.1%} từ SRT với kịch bản — kịch bản đã sửa sau khi đọc voice?")

    d.mkdir(parents=True, exist_ok=True)
    (d / "khoi.json").write_text(json.dumps(khoi, ensure_ascii=False, indent=1), encoding="utf-8")
    T.ghi_khoi(d / "khoi_goc.txt", khoi, "goc")
    # tiêu đề + mô tả lấy thẳng từ file kịch bản: khối TITLE: và DESCRIPTION:
    mo_ta = T.khoi(script, "DESCRIPTION")
    nguon = f"TITLE: {T.khoi(script, 'TITLE') or ''}\nDESCRIPTION:\n" + (mo_ta or "(chưa có mô tả gốc)")
    (d / "nguon_tieu_de_mo_ta.txt").write_text(nguon + "\n", encoding="utf-8")

    L = [k["b"] - k["a"] for k in khoi]
    print(f"✓ {len(khoi)} khối · {khoi[-1]['chuong'] + 1} chương · khớp chữ {khop:.1%}")
    print(f"  độ dài khối: trung vị {statistics.median(L):.1f} s · ngắn nhất {min(L):.1f} · dài nhất {max(L):.1f}")
    print(f"  12–20 s: {sum(12 <= x <= 20 for x in L)} · < 8 s: {sum(x < 8 for x in L)} · > 20 s: {sum(x > 20 for x in L)}")
    if not mo_ta:
        print("⚠️  kịch bản chưa có khối DESCRIPTION: — bản dịch chỉ có tiêu đề (thêm khối DESCRIPTION: vào kịch bản rồi chạy lại --ghi-de)")
    print(f"→ {d / 'khoi_goc.txt'}")


if __name__ == "__main__":
    main()
