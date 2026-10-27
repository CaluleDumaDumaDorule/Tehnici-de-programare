import hashlib
import ssl
from datetime import datetime
import socket
import json
import requests
import urllib.parse
from html.parser import HTMLParser
import re
BASE_URL = "https://cybercor.org"
TIMEOUT = 10


# Exercitiul 35

def parse_url():
    url = "https://cybercor.org/path?x=1#top"

    parsed = urllib.parse.urlparse(url)

    print("Scheme:", parsed.scheme)
    print("Netloc:", parsed.netloc)
    print("Path:", parsed.path)
    print("Query:", parsed.query)
    print("Fragment:", parsed.fragment)


parse_url()

# Exercitiul 36

def build_urls():
    links = [
        "/about",
        "contact.html",
        "../index.html"
    ]

    for link in links:
        full_url = urllib.parse.urljoin(BASE_URL, link)
        print(full_url)


build_urls()

# Exercitiul 37

def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)

    links_fara_duplicate = list(set(links))

    return links_fara_duplicate


response37 = requests.get(BASE_URL, timeout=TIMEOUT)

print(extract_links(response37.text))

# Exercitiul 38

def split_links(links, domain):
    internal = []
    external = []

    for link in links:
        full_url = urllib.parse.urljoin(BASE_URL, link)
        link_domain = urllib.parse.urlparse(full_url).netloc

        if link_domain == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


response38 = requests.get(BASE_URL, timeout=TIMEOUT)

links = extract_links(response38.text)

internal, external = split_links(links, "cybercor.org")

print("Interne:", internal)
print("Externe:", external)

# Exercitiul 39

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src is not None:
                self.images.append(src)
test_html="""
<html><body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fara src">
<img src="https://cdn.example.com/banner.webp" />
<a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)

print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a gasit exact imaginile asteptate"

print("Testul a trecut!")

# Exercitiul 40

def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


fingerprint1 = page_fingerprint(BASE_URL)
fingerprint2 = page_fingerprint(BASE_URL)

print(fingerprint1)
print(fingerprint2)

print("Sunt identice:", fingerprint1 == fingerprint2)

# Exercitiul 41

def save_headers_json(url):
    response = requests.get(url, timeout=TIMEOUT)

    with open("headers.json", "w") as file:
        json.dump(dict(response.headers), file, indent=2)


def load_headers_json():
    with open("headers.json", "r") as file:
        data = json.load(file)

    print(data.get("Content-Type", "lipseste"))


save_headers_json(BASE_URL)
load_headers_json()

# Exercitiul 42

def resolve(hostname):
    return socket.gethostbyname(hostname)


ip = resolve("cybercor.org")
print(ip)

# Exercitiul 43

def cert_days_left(hostname):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()

    expire_text = cert["notAfter"]
    expire_seconds = ssl.cert_time_to_seconds(expire_text)

    expire_date = datetime.fromtimestamp(expire_seconds)
    now = datetime.now()

    days_left = (expire_date - now).days

    return days_left


print(cert_days_left("cybercor.org"))
