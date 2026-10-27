# Raport - Laboratorul 6: Informatii invizibile, forensics si steganografie

## Lucrarea A - Decoder universal

- Mesajul din `probe/mesaj.txt` a fost desfacut prin lantul: **base64 -> base64 -> hex**.
- Rezultatul final: **FLAG{straturi_de_encoding}**.
- Pentru `probe/xor.bin`, cheia gasita este **128 (0x80)**.
- Text XOR recuperat: **Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}**.
- Hash-ul tinta este de tip **md5**, iar parola gasita prin dictionar este **password**.
- Testele automate se gasesc in `teste/test_decode.py` si trec cu succes.

## Lucrarea B - Forensics pe fisiere si steganografie

- `probe/foto.jpg` este identificat dupa magic bytes ca **JPEG**.
- `probe/ascuns.png` este identificat dupa magic bytes ca **PNG**.
- Din `probe/foto.jpg` se extrag metadate EXIF si coordonate GPS: aproximativ **47.016667 N, 28.857500 E**.
- In `probe/ascuns.png` se gaseste semnatura ZIP `PK\x03\x04`; arhiva este extrasa in `gasit.zip`.
- Arhiva contine `secret.txt` cu mesajul **FLAG{ascuns_prin_carving}**.
- Mesajul ascuns prin LSB este **FLAG{ascuns_in_pixeli}** si este recuperat integral din `stego.png`.

## Provocare optionala

- `probe/challenge.bin` contine un strat Base64 peste XOR cu o cheie de un octet.
- Cheia gasita este **128 (0x80)**.
- Mesajul recuperat este **FLAG{lant_complet_despicat}**.

## Concluzie

Laboratorul a consolidat lucrul cu `str` si `bytes`, encodari Base64/Hex/URL, XOR, hash-uri, fisiere binare, magic bytes, expresii regulate, metadate EXIF/GPS, file carving si steganografie LSB. Toate operatiile au fost efectuate pe fisierele de laborator generate local.
