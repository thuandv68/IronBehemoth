"""Công thức trộn tiếng của skill long-tieng (chép nguyên từ bước dựng video của bản gốc).

ffmpeg: biến môi trường FFMPEG trỏ tới ffmpeg.exe, không có thì gọi `ffmpeg` trong PATH.
"""
import os

FF = os.environ.get("FFMPEG", "ffmpeg")
LUFS_RA = -14.0


def loc_tron_am(T, sr, vo, nh, sx):
    """Công thức trộn tiếng DUY NHẤT của kênh: giọng + nhạc (sidechain theo giọng) + SFX → [a]. Bản gốc dùng đúng hàm
    này cho cả bước dựng video lẫn skill long-tieng — để bản lồng tiếng luôn trộn y hệt bản gốc. vo/nh/sx = nhãn đầu vào.
    2026-10-08 đã thử bỏ sidechain (nhạc chỉ lên ở nghỉ chương) và thử sidechain chỉ ở mở bài — chủ kênh nghe cả hai
    đều chưa ổn, khôi phục nguyên bản này."""
    return [f"{vo}atrim=0:{T:.3f},asetpts=PTS-STARTPTS,aresample={sr},"
            f"afade=t=out:st={T - 0.5:.3f}:d=0.5,asplit=2[vo][vsc]",
            f"{nh}[vsc]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=350[md]",
            f"{sx}aresample={sr},pan=stereo|c0=c0|c1=c0[sx]",
            f"[vo][md][sx]amix=inputs=3:normalize=0:duration=first,afade=t=out:st={T - 0.6:.3f}:d=0.6,"
            f"loudnorm=I={LUFS_RA}:TP=-1.5:LRA=11,aresample={sr}[a]"]
