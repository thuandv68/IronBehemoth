"""Bước 3 — đọc voice một ngôn ngữ bằng ai33 rồi co giãn từng khối về khung gốc.

Dùng:  python lt_03_doc_khop.py "<thư mục tập>" --ngon-ngu tieng_anh

- Mỗi chương gửi MỘT task ai33, các khối nối bằng marker nghỉ dài (marker_tach_khoi) để tách lại chính xác.
- Chỉ đọc khối CHƯA có hoặc ĐÃ SỬA chữ (so mã băm). Sửa chữ một khối rồi chạy lại lệnh này = chỉ đọc lại khối đó.
- task_id lưu ở _tmp_skill/long-tieng/<ngôn ngữ>/tasks.json: bị ngắt thì chạy lại, polling tiếp, không trừ credit hai lần.
- Co giãn bằng bộ lọc co_gian trong ngưỡng nen_toi_da / gian_toi_da. Khối vượt ngưỡng → in VUOT, thoát 1:
  agent viết lại khối đó rồi chạy lại.
Ra:    _tmp_skill/long-tieng/<ngôn ngữ>/khop/<id>.wav · bao_cao.json
"""
import argparse, json, time
from pathlib import Path

import lt_lib as T

GIAY_CHO = 5
TRAN_CHO = 60 * 60
BAO_MOI = 60          # giây giữa hai dòng báo tiến độ khi chờ ai33


def ghi_json(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=1), encoding="utf-8")


def doc_json(p, mac_dinh):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else mac_dinh


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
        T.dung(f"ngôn ngữ '{nn}' không có trong quy tắc kênh")
    khoi = T.doc_khoi(v)
    f = T.file_dich(v, nn)
    if not f.is_file():
        T.dung(f"chưa có {f}")
    dich = T.doc_dich(f)
    if [k["id"] for k in khoi] != list(dich) or any(not dich[k["id"]][1] for k in khoi):
        T.dung("bản dịch lệch khoi.json hoặc có khối rỗng — chạy lt_02_kiem_dich.py tới PASS trước")

    d = T.tm(v) / nn
    (d / "raw").mkdir(parents=True, exist_ok=True)
    (d / "khop").mkdir(exist_ok=True)
    meta = doc_json(d / "meta.json", {})
    tasks = doc_json(d / "tasks.json", {})

    # ---- khối cần đọc: chưa có hoặc chữ đã đổi; gom theo chương
    can = [k for k in khoi if meta.get(k["id"], {}).get("bam") != T.bam(dich[k["id"]][1])]
    nhom = {}
    for k in can:
        nhom.setdefault(k["chuong"], []).append(k["id"])
    sep = f"\n\n{ch['marker_tach_khoi']}\n\n"
    viec = []
    for c, ids in sorted(nhom.items()):
        van = sep.join(dich[i][1] for i in ids)
        viec.append(dict(khoa=T.bam(van), ids=ids, van=van, chuong=c))

    loi = []
    moi = []                     # khối vừa đọc trong lượt này (để ghi sổ tốc độ)
    credit_luot = 0
    if viec:
        dv = T.doc_voice()
        cv = dv.doc_cau_hinh()
        cv["with_transcript"] = "false"
        api = dv.Ai33(dv.lay_key(cv["tts_provider"]))
        print(f"{nn}: đọc {len(can)} khối trong {len(viec)} task · {sum(len(x['van']) for x in viec)} ký tự · "
              f"giọng {cv['voice_id']} speed {cv['speed']} · credit {api.credits()}")
        for x in viec:
            if x["khoa"] in tasks:
                print(f"  chương {x['chuong']}: tiếp tục task {tasks[x['khoa']]['task_id']}")
                continue
            tid = api.gui(x["van"], cv, f"{v.name}_{nn}_c{x['chuong']}")
            tasks[x["khoa"]] = dict(task_id=tid, ids=x["ids"], chuong=x["chuong"],
                                    gui_luc=time.strftime("%Y-%m-%d %H:%M:%S"))
            ghi_json(d / "tasks.json", tasks)
            print(f"  chương {x['chuong']}: gửi task {tid} ({len(x['ids'])} khối)")

        bd = time.time()
        con = {x["khoa"]: x for x in viec}
        bao_luc = time.time()
        while con:
            pct = {}
            for khoa in list(con):
                t = api.task(tasks[khoa]["task_id"])
                st = t.get("status")
                pct[con[khoa]["chuong"] if khoa in con else -1] = t.get("progress")
                if st == "error":
                    loi.append(f"chương {con[khoa]['chuong']}: task {tasks[khoa]['task_id']} lỗi: {t.get('error_message')}")
                    tasks.pop(khoa)
                    con.pop(khoa)
                elif st == "done":
                    x = con.pop(khoa)
                    mp3 = d / f"task_{khoa}.mp3"
                    dv.tai(t["metadata"]["audio_url"], mp3)
                    doan, ly_do = T.tach_doan(T.doc_am(mp3), len(x["ids"]))
                    if doan is None:
                        loi.append(f"chương {x['chuong']}: không tách được {len(x['ids'])} khối — {ly_do}. "
                                   f"Giữ {mp3.name} để xem")
                    else:
                        for i, seg in zip(x["ids"], doan):
                            T.ghi_am(seg, d / "raw" / f"{i}.wav")
                            meta[i] = dict(bam=T.bam(dich[i][1]), giay=round(len(seg) / T.SR, 3))
                            moi.append(i)
                        mp3.unlink()
                    tasks.pop(khoa)
                    ghi_json(d / "meta.json", meta)
                    print(f"  chương {x['chuong']}: xong · credit {t.get('credit_cost')}")
                    credit_luot += int(t.get("credit_cost") or 0)
                ghi_json(d / "tasks.json", tasks)
            if con and time.time() - bao_luc >= BAO_MOI:
                # nhịp báo tiến độ: agent chính đọc dòng này để báo user, chứng minh máy không treo (chủ kênh 2026-10-08)
                da = len(viec) - len(con)
                cho = ", ".join(f"c{c} {p if p is not None else '?'}%" for c, p in sorted(pct.items()) if c >= 0)
                print(f"  [{int(time.time() - bd) // 60}:{int(time.time() - bd) % 60:02d}] {nn}: {da}/{len(viec)} task xong"
                      f" · đang chờ: {cho}", flush=True)
                bao_luc = time.time()
            if con:
                if time.time() - bd > TRAN_CHO:
                    T.dung(f"quá {TRAN_CHO // 60} phút chưa xong — chạy lại lệnh để chờ tiếp")
                time.sleep(GIAY_CHO)
        print(f"  credit còn {api.credits()}")

    # ---- credit: cộng credit_cost của từng task, cộng dồn vào credit.json của ngôn ngữ. ⛔ Không đo bằng hiệu số dư
    # tài khoản: các agent chạy song song cùng một tài khoản ai33 (0928, 2026-10-08: số dư lẫn cả 5 ngôn ngữ).
    so_credit = doc_json(d / "credit.json", dict(tong=0, luot=[]))
    if credit_luot:
        so_credit["tong"] += credit_luot
        so_credit["luot"].append(dict(luc=time.strftime("%Y-%m-%d %H:%M:%S"), credit=credit_luot, khoi=len(moi)))
        ghi_json(d / "credit.json", so_credit)
    print(f"CREDIT: lượt này {credit_luot} · cộng dồn {nn} {so_credit['tong']} ({len(so_credit['luot'])} lượt đọc)")

    # ---- sổ tốc độ đọc: chỉ lần đọc ĐẦU (≥ 50% số khối) của tập + ngôn ngữ — lần đọc lại vài khối không đại diện
    if len(moi) >= len(khoi) / 2:
        kk = {k["id"]: k for k in khoi}
        cps = sum(len(dich[i][1]) for i in moi) / sum(meta[i]["giay"] for i in moi)
        tv = float(T.np.median([meta[i]["giay"] / T.khung_loi(kk[i]["b"] - kk[i]["a"], ch) for i in moi]))
        if T.ghi_so(v.name, nn, cps, tv, len(moi)):
            print(f"  SO TOC DO: ghi {v.name} · {nn} · {cps:.2f} ký tự/giây lời · lời/khung lần đầu {tv:.2f} "
                  f"→ {T.FILE_SO.name}")

    # ---- co giãn — MỘT tốc độ chung cho cả chương (chủ kênh 2026-10-08: tốc độ nhảy từ khối này sang khối kia
    # nghe giật). Tốc độ chương = trung vị lời/khung-lời các khối trong chương. Khối ngắn hơn: đọc đúng tốc độ
    # chương rồi để lặng; khối dài hơn: nén riêng vừa đủ. Khối lệch quá xa → VUOT, agent viết lại.
    gian, nen, tho = float(ch["gian_toi_da"]), float(ch["nen_toi_da"]), float(ch["khong_co_gian"])
    du_lang = float(ch["du_lang_toi_da"])
    ky = T.chu_ky(ch)
    co = {}                              # id -> (khung, khung lời, tỉ lệ)
    for k in khoi:
        m = meta.get(k["id"])
        if m and m.get("bam") == T.bam(dich[k["id"]][1]):
            khung = k["b"] - k["a"]
            kl = T.khung_loi(khung, ch)
            co[k["id"]] = (khung, kl, m["giay"] / kl)
    toc = {}
    for c in sorted({k["chuong"] for k in khoi}):
        r = [co[k["id"]][2] for k in khoi if k["chuong"] == c and k["id"] in co]
        if r:
            toc[c] = T.toc_chuong(r, ch)                  # chương gần khớp sẵn: giữ giọng thô
    bao, vuot = [], []
    for k in khoi:
        if k["id"] not in co:
            vuot.append((k["id"], None, "chưa có voice"))
            continue
        m = meta[k["id"]]
        khung, kl, tl = co[k["id"]]
        tc = toc[k["chuong"]]
        t = max(tc, tl)                                  # ngắn hơn: theo tốc độ chương · dài hơn: nén riêng
        lang = kl - m["giay"] / t                        # lặng dư sau lời (ngoài nghi_cuoi_khoi)
        dong = dict(id=k["id"], khung=round(khung, 3), loi=m["giay"], ti_le=round(tl, 4), toc_chuong=round(tc, 4),
                    toc=round(t, 4))
        if tl > 1 + nen:
            ly = f"lời {m['giay']:.2f}s / khung lời {kl:.2f}s = {tl:.2f} → viết NGẮN lại khoảng {(tl - 1) * 100:.0f}%"
        elif lang > du_lang * kl:
            can = round((1 - du_lang / 2) * kl * tc / m["giay"] * 100 - 100)
            ly = (f"lời {m['giay']:.2f}s ở tốc độ chương {tc:.2f} còn lặng {lang:.1f}s / khung lời {kl:.2f}s "
                  f"→ viết DÀI thêm khoảng {can}%")
        else:
            ly = None
        if ly:
            dong["dat"] = False
            vuot.append((k["id"], tl, ly))
        else:
            out = d / "khop" / f"{k['id']}.wav"
            dau = m["bam"] + ky + f"|{t:.4f}"
            if m.get("khop") != dau or not out.is_file():
                x = T.doc_am(d / "raw" / f"{k['id']}.wav")
                n = int(round(khung * T.SR))
                y = x if t == 1.0 else T.gian(x, m["giay"] / t, ch["co_gian"])
                y = T.np.pad(y, (0, max(0, n - len(y))))[:n]
                T.ghi_am(y, out)
                m["khop"] = dau
            dong["dat"] = True
            dong["giu_tho"] = t == 1.0
        bao.append(dong)
    if toc:
        print(f"{nn}: tốc độ theo chương · " + " · ".join(f"c{c} {t:.2f}" for c, t in sorted(toc.items())))
    ghi_json(d / "meta.json", meta)
    ghi_json(d / "bao_cao.json", bao)

    tl = [b["ti_le"] for b in bao]
    if tl:
        print(f"{nn}: {sum(b['dat'] for b in bao)}/{len(khoi)} khối đạt · tỉ lệ lời/khung {min(tl):.2f}–{max(tl):.2f} "
              f"(ngưỡng {1 - gian:.2f}–{1 + nen:.2f}) · giữ giọng thô {sum(b.get('giu_tho', False) for b in bao)} khối")
    for i, _, ly in vuot:
        print(f"VUOT: {i} · {ly}")
    for x in loi:
        print(f"LOI: {x}")
    return 1 if vuot or loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
