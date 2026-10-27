# Laborator: functii, metode si importuri pe web
# Student: Alex Chistruga

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

# Exercitiul 9

response9 = requests.get(BASE_URL, timeout=TIMEOUT)

print(response9.status_code)
print(response9.ok)
print(response9.url)
print(response9.encoding)

# Exercitiul 10

response10 = requests.get(BASE_URL, timeout=TIMEOUT)
response10.raise_for_status()

try:
    response10_bad = requests.get(
        BASE_URL + "/this-page-does-not-exist",
        timeout=TIMEOUT
    )

    response10_bad.raise_for_status()

except requests.HTTPError:
    print("Pagina nu exista sau a aparut o eroare HTTP.")

# Exercitiul 11

response11 = requests.get(BASE_URL, timeout=TIMEOUT)

for nume, valoare in response11.headers.items():
    print(nume + ":", valoare)

# Exercitiul 12

response12 = requests.get(BASE_URL, timeout=TIMEOUT)

print(response12.headers.get("Server", "lipsește"))
print(response12.headers.get("Content-Type", "lipsește"))
print(response12.headers.get("content-type", "lipsește"))

# Exercitiul 13

response13 = requests.get(BASE_URL, timeout=TIMEOUT)

aparitii = response13.text.lower().count("cyber")

print(aparitii)

# Exercitiul 14

response14 = requests.get(BASE_URL, timeout=TIMEOUT)

html = response14.text

start = html.find("<title>") + len("<title>")
end = html.find("</title>")

titlu = html[start:end].strip()

print(titlu)

# Exercitiul 15

response15 = requests.get(BASE_URL, timeout=TIMEOUT)

lines = response15.text.splitlines()

print("Numar de linii:", len(lines))

cea_mai_lunga = max(lines, key=len)

print("Lungimea celei mai lungi linii:", len(cea_mai_lunga))

# Exercitiul 16

response16 = requests.get(BASE_URL, timeout=TIMEOUT)

if response16.url.startswith("https://"):
      print("Conexiune securizata")
else:
      print("Conexiune nesecurizata")

# Exercitiul 17

response17 = requests.get("http://cybercor.org", timeout=TIMEOUT)

for redirect in response17.history:
    print(redirect.status_code, redirect.url)

print("URL final:", response17.url)

# Exercitiul 18

response18_head = requests.head(BASE_URL, timeout=TIMEOUT)
response18_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("HEAD:", len(response18_head.content))
print("GET:", len(response18_get.content))

# Exercitiul 19

response19 = requests.get(BASE_URL, timeout=TIMEOUT)

if response19.cookies:
    for cookie in response19.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat")

# Exercitiul 20

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Alex"
})

response20 = session.get(
    ECHO_URL + "/headers",
    timeout=TIMEOUT
)

print(response20.text)
