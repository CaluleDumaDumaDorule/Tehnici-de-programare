import os
import re
import zipfile
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PIL import Image


def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return "necunoscut (" + cap.hex() + ")"


def extrage_strings(cale, minim=4):
    date = open(cale, "rb").read()
    sablon = rb"[ -~]{%d,}" % minim
    return [m.decode("ascii", errors="ignore") for m in re.findall(sablon, date)]


def dms_la_zecimal(dms, ref):
    grade, minute, secunde = (float(x) for x in dms)
    val = grade + minute / 60 + secunde / 3600
    return -val if ref in ("S", "W") else val


def extrage_exif_gps(cale):
    img = Image.open(cale)
    exif = img.getexif()
    meta = {}
    for tag_id, val in exif.items():
        meta[str(tag_id)] = val

    gps = None
    try:
        gps = exif.get_ifd(0x8825)
    except Exception:
        pass
    if not gps:
        raw = img._getexif() or {}
        gps = raw.get(34853)

    coord = None
    if gps:
        lat_ref = gps.get(1, "N")
        lat_dms = gps.get(2)
        lon_ref = gps.get(3, "E")
        lon_dms = gps.get(4)
        if lat_dms and lon_dms:
            coord = (dms_la_zecimal(lat_dms, lat_ref), dms_la_zecimal(lon_dms, lon_ref))
    return meta, coord


def carving_zip(cale_png, iesire="gasit.zip"):
    date = open(cale_png, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None, None
    open(iesire, "wb").write(date[i:])
    continut = []
    with zipfile.ZipFile(iesire) as z:
        for nume in z.namelist():
            continut.append((nume, z.read(nume).decode("utf-8", errors="replace").strip()))
    return i, continut


def ascunde_lsb(cale_sursa, mesaj: str, cale_iesire="stego.png"):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())
    date = mesaj.encode("utf-8") + b"\x00"
    biti = "".join(f"{x:08b}" for x in date)
    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul nu incape in imagine")

    px_nou = []
    idx = 0
    for r, g, b in px:
        canale = [r, g, b]
        for c in range(3):
            if idx < len(biti):
                canale[c] = (canale[c] & ~1) | int(biti[idx])
                idx += 1
        px_nou.append(tuple(canale))

    img.putdata(px_nou)
    img.save(cale_iesire, "PNG")
    return cale_iesire


def dezvaluie_lsb(cale_stego="stego.png"):
    px = list(Image.open(cale_stego).convert("RGB").getdata())
    biti = []
    for r, g, b in px:
        biti.extend([str(r & 1), str(g & 1), str(b & 1)])

    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        val = int("".join(biti[i:i+8]), 2)
        if val == 0:
            break
        octeti.append(val)
    return octeti.decode("utf-8", errors="replace")


def main():
    print("=== B1 Magic bytes ===")
    for cale in ("probe/foto.jpg", "probe/ascuns.png"):
        print(cale, "->", tip_real(cale))

    print("\n=== B2 Strings ===")
    siruri = extrage_strings("probe/ascuns.png")
    print("Numar siruri:", len(siruri))
    for s in siruri:
        if "secret" in s.lower() or "flag" in s.lower() or "PK" in s:
            print("indiciu:", s)

    print("\n=== B3 EXIF/GPS ===")
    meta, coord = extrage_exif_gps("probe/foto.jpg")
    print("EXIF disponibil:", bool(meta))
    print("GPS:", coord)

    print("\n=== B4 File carving ===")
    offset, continut = carving_zip("probe/ascuns.png", "gasit.zip")
    print("Offset ZIP:", offset)
    print("Continut:", continut)

    print("\n=== B5-B6 LSB ===")
    mesaj = "FLAG{ascuns_in_pixeli}"
    ascunde_lsb("probe/foto.jpg", mesaj, "stego.png")
    print("Mesaj recuperat:", dezvaluie_lsb("stego.png"))


if __name__ == "__main__":
    main()
