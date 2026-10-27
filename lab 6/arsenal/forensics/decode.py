import argparse
import base64
import hashlib
import json
import os
import re
from urllib.parse import unquote


def demonstratie_text_octeti():
    s = "Salut"
    b = s.encode()
    return {
        "text": s,
        "bytes": b,
        "primul_octet": b[0],
        "hex": b.hex(),
        "refacut": bytes.fromhex(b.hex()),
    }


def ghici_strat(s: str) -> str:
    s = s.strip()
    if not s:
        return "necunoscut"
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9A-Fa-f]+", s):
        return "hex"
    if len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"


def desfa(s: str):
    s = s.strip()
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode()
    return "necunoscut", s.encode()


def citibil(b: bytes) -> bool:
    return len(b) > 0 and all(32 <= c < 127 for c in b)


def decodeaza_complet(text: str, max_iter: int = 8):
    curent = text.strip()
    lant = []
    for _ in range(max_iter):
        strat = ghici_strat(curent)
        if strat == "necunoscut":
            break
        strat, rezultat = desfa(curent)
        lant.append(strat)
        if not citibil(rezultat):
            return lant, rezultat
        curent = rezultat.decode("ascii")
    return lant, curent.encode("ascii", errors="replace")


def scor_text(b: bytes) -> float:
    if not citibil(b):
        return float("-inf")
    low = b.lower()
    scor = 0.0
    if b"flag{" in low:
        scor += 10000
    scor += sum(3 for c in low if 97 <= c <= 122)
    scor += sum(2 for c in low if c in b" _{}.!,-")
    return scor


def sparge_xor(date: bytes):
    cel_mai_bun = (None, b"", float("-inf"))
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        sc = scor_text(clar)
        if sc > cel_mai_bun[2]:
            cel_mai_bun = (k, clar, sc)
    return cel_mai_bun


def algoritm_din_lungime(hash_hex: str):
    return {32: "md5", 40: "sha1", 64: "sha256"}.get(len(hash_hex))


def sparge_hash(hash_tinta: str, cuvinte):
    hash_tinta = hash_tinta.strip().lower()
    alg = algoritm_din_lungime(hash_tinta)
    if alg is None:
        return None, None
    for cuv in cuvinte:
        cuv = cuv.strip()
        if not cuv:
            continue
        candidat = hashlib.new(alg, cuv.encode()).hexdigest()
        if candidat == hash_tinta:
            return alg, cuv
    return alg, None


def analiza_hash(cale_hashuri: str, cale_wordlist: str):
    tinta = open(cale_hashuri, encoding="utf-8").readline().strip()
    with open(cale_wordlist, encoding="latin1") as f:
        alg, parola = sparge_hash(tinta, f)
    return tinta, alg, parola


def main():
    p = argparse.ArgumentParser(description="Decoder universal - Lab 6")
    p.add_argument("intrare", help="sir codificat sau cale catre fisier")
    p.add_argument("--fisier", action="store_true", help="trateaza intrarea ca fisier text")
    p.add_argument("--xor", default="probe/xor.bin", help="fisier XOR")
    p.add_argument("--hashuri", default="probe/hashuri.txt")
    p.add_argument("--wordlist", default="probe/wordlist.txt")
    p.add_argument("--iesire", default="arsenal/forensics/fisa.json")
    a = p.parse_args()

    if a.fisier:
        text = open(a.intrare, encoding="utf-8").read().strip()
    else:
        text = a.intrare

    lant, rezultat = decodeaza_complet(text)
    rezultat_text = rezultat.decode("utf-8", errors="replace")
    print("Lant:", " -> ".join(lant) if lant else "necunoscut")
    print("Rezultat:", rezultat_text)

    fisa = {"straturi": lant, "rezultat": rezultat_text}

    if os.path.exists(a.xor):
        date = open(a.xor, "rb").read()
        k, clar, _ = sparge_xor(date)
        fisa["xor"] = {"cheie": k, "cheie_hex": hex(k) if k is not None else None,
                       "rezultat": clar.decode("utf-8", errors="replace")}
        print("XOR:", k, fisa["xor"]["rezultat"])

    if os.path.exists(a.hashuri) and os.path.exists(a.wordlist):
        tinta, alg, parola = analiza_hash(a.hashuri, a.wordlist)
        fisa["hash"] = {"tinta": tinta, "algoritm": alg, "parola": parola}
        print("Hash:", alg, "parola =", parola)

    os.makedirs(os.path.dirname(a.iesire), exist_ok=True)
    with open(a.iesire, "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=2, ensure_ascii=False)
    print("Fisa salvata:", a.iesire)


if __name__ == "__main__":
    main()
