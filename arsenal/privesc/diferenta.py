import os

from arsenal.privesc.enum import GTFO, citeste_linii, nume


def cai(fisier):
    """Întoarce mulțimea căilor din fișier."""
    return set(citeste_linii(fisier))


def compara(baza_fisier, acum_fisier):
    """Compară starea curată cu cea actuală și întoarce rezultatele."""
    baza = cai(baza_fisier)
    acum = cai(acum_fisier)
    noi = acum - baza
    risc = {
        nume(c): ("mare" if nume(c) in GTFO else "normal")
        for c in noi
    }
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    return baza, acum, noi, risc, periculoase


def main():
    start = os.path.join(os.path.dirname(__file__), "start")
    baza_fisier = os.path.join(start, "baza_suid.txt")
    acum_fisier = os.path.join(start, "suid.txt")

    baza, acum, noi, risc, periculoase = compara(baza_fisier, acum_fisier)

    print("baza:", len(baza), " acum:", len(acum))
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()
