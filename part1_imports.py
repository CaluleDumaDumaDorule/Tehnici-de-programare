# Laborator: funcții, metode și importuri pe web
# Student: <Alex Chistruga>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 1

import requests
print(requests.__version__)

import urllib.request

# requests este o bibliotecă externă și trebuie instalată cu pip.
# urllib face parte din biblioteca standard Python și nu trebuie instalată separat.

# Exercițiul 2

response = requests.get(BASE_URL, timeout=TIMEOUT)
print(response.status_code)

from requests import get

response2 = get(BASE_URL, timeout=TIMEOUT)
print(response2.status_code)

# Avantaj import requests: se vede clar din ce modul vine funcția get.
# Avantaj from requests import get: codul este mai scurt.


# Exercitiul 3

import requests as rq

response3 = rq.get(BASE_URL, timeout=TIMEOUT)
print(response3.status_code)

# Alias-ul face codul mai ușor de citit când numele modulului este lung.
# Poate face codul mai greu de citit dacă alias-ul este neclar sau neobișnuit.

# Exercițiul 4

request = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

response4 = urllib.request.urlopen(request, timeout=TIMEOUT)

print(response4.status)

body = response4.read().decode("utf-8")
print(body[:200])

# Exercițiul 5

print(dir(requests))

# get este o funcție.
# Session este o clasă.
# exceptions este un modul.


# Exercițiul 6

help(requests.get)

response6 = requests.get(BASE_URL, timeout=TIMEOUT)
print(response6.status_code)

# Exercitiul 7

import time 

start = time.perf_counter()

response7 = requests.get(BASE_URL, timeout=TIMEOUT)

end = time.perf_counter()

durata = end - start

print("Durata cu perf_counter:", durata)
print("Durata din response.elapsed:", response7.elapsed.total_seconds())

# Exercitiul 8

try:
    import bs4
    print("Modulul bs4 este instalat.")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
