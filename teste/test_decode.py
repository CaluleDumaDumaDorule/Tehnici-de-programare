import hashlib
from arsenal.forensics.decode import (
    ghici_strat, desfa, citibil, decodeaza_complet, sparge_xor, sparge_hash
)


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    assert desfa("48656c6c6f") == ("hex", b"Hello")


def test_url():
    assert desfa("%2Fetc") == ("url", b"/etc")


def test_citibil():
    assert citibil(b"Salut 123")
    assert not citibil(b"\x00\xff")


def test_xor():
    clar = b"FLAG{test_xor}"
    date = bytes(b ^ 42 for b in clar)
    k, rezultat, _ = sparge_xor(date)
    assert k == 42
    assert rezultat == clar


def test_hash_md5():
    tinta = hashlib.md5(b"parola").hexdigest()
    assert sparge_hash(tinta, ["abc", "parola", "xyz"]) == ("md5", "parola")
