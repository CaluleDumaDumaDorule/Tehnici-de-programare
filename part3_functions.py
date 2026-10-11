import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercitiul 21

def fetch(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response

response21 = fetch(BASE_URL)

print(response21.status_code)

# Exercitiul 22

def get_status(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print(get_status(BASE_URL + "/"))
time.sleep(1)

print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)

print(get_status(BASE_URL + "/sitemap.xml"))

# Exercitiul 23

def fetch(url, timeout=10):
    response = requests.get(url, timeout=timeout)
    return response

response23_1 = fetch(BASE_URL)
print(response23_1.status_code)

response23_2 = fetch(BASE_URL, timeout=3)
print(response23_2.status_code)

# Exercitiul 24

def get_title(html):
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    return title


response24 = requests.get(BASE_URL, timeout=TIMEOUT)

print(get_title(response24.text))

# Exercitiul 25

def get_title(html):
    """Returneaza titlul unei pagini HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    return title

help(get_title)

# Exercitiul 26

def get_status(url: str) -> int:
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print(get_status(BASE_URL))

# Exercitiul 27

def page_exists(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True

    except requests.RequestException:
        return False


print(page_exists(BASE_URL))
print(page_exists("https://this-domain-does-not-exist.invalid"))

# Exercitiul 28

def check_paths(base, paths):
    results = {}

    for path in paths:
        response = requests.get(base + path, timeout=TIMEOUT)
        results[path] = response.status_code
        time.sleep(1)

    return results


paths = ["/", "/robots.txt", "/sitemap.xml"]

print(check_paths(BASE_URL, paths))

# Exercitiul 29

def get_header(url, name, default="lipsește"):
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)


print(get_header(BASE_URL, name="Server"))

# Exercitiul 30

def security_headers(url):
    response = requests.get(url, timeout=TIMEOUT)

    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    results = {}

    for header in headers_to_check:
        results[header] = header in response.headers

    return results


print(security_headers(BASE_URL))

# Exercitiul 31

def score_headers(results):
    score = 0

    for value in results.values():
        if value:
            score = score + 1

    return str(score) + "/" + str(len(results))


print(score_headers(security_headers(BASE_URL)))

# Exercitiul 32

def fetch_robots(base):
    try:
        response = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        if line.startswith("Disallow:"):
            path = line.replace("Disallow:", "").strip()
            paths.append(path)

    return paths


robots = fetch_robots(BASE_URL)
print(disallowed_paths(robots))

# Exercitiul 33

def response_times(*urls):
    results = {}

    for url in urls:
        start = time.perf_counter()

        requests.get(url, timeout=TIMEOUT)

        end = time.perf_counter()

        results[url] = end - start

    return results


print(response_times(
    BASE_URL,
    BASE_URL + "/robots.txt"
))

# Exercitiul 34

def log(message, **details):
    text = message

    for key, value in details.items():
        text = text + " | " + key + "=" + str(value)

    print(text)


log("verificat", url=BASE_URL, status=200)
