import time
import requests
import json
import socket
import ssl
import urllib.parse
import re
from datetime import datetime


TIMEOUT = 10

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Alex"
}


def fetch(url, timeout=10):
    """Returneaza obiectul response pentru URL-ul primit."""
    response = requests.get(
        url,
        timeout=timeout,
        headers=DEFAULT_HEADERS
    )
    return response


def get_status(url):
    """Returneaza codul de stare HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


def get_title(html):
    """Returneaza titlul unei pagini HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")

    return html[start:end].strip()


def security_headers(url):
    """Verifica prezenta antetelor de securitate."""
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


def check_paths(base, paths):
    """Returneaza codul de stare pentru fiecare cale."""
    results = {}

    for path in paths:
        response = requests.get(
            base + path,
            timeout=TIMEOUT
        )

        results[path] = response.status_code

    return results


def score_headers(results):
    """Calculeaza scorul antetelor de securitate."""
    score = 0

    for value in results.values():
        if value:
            score = score + 1

    return str(score) + "/" + str(len(results))


def fetch_robots(base):
    """Returneaza continutul robots.txt sau None."""
    try:
        response = requests.get(
            base + "/robots.txt",
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Extrage caile Disallow din robots.txt."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        if line.startswith("Disallow:"):
            path = line.replace(
                "Disallow:",
                ""
            ).strip()

            paths.append(path)

    return paths


def extract_links(html):
    """Extrage linkurile din codul HTML."""
    links = re.findall(
        r'href="([^"]+)"',
        html
    )

    return list(set(links))


def split_links(links, domain):
    """Imparte linkurile in interne si externe."""
    internal = []
    external = []

    for link in links:
        full_url = urllib.parse.urljoin(
            "https://" + domain,
            link
        )

        link_domain = urllib.parse.urlparse(
            full_url
        ).netloc

        if link_domain == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


def resolve(hostname):
    """Returneaza adresa IP a domeniului."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname):
    """Returneaza numarul de zile pana la expirarea certificatului."""
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443)
    ) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_sock:

            cert = secure_sock.getpeercert()

    expire_text = cert["notAfter"]

    expire_seconds = ssl.cert_time_to_seconds(
        expire_text
    )

    expire_date = datetime.fromtimestamp(
        expire_seconds
    )

    now = datetime.now()

    return (expire_date - now).days

def site_report(url):
    """Genereaza raportul complet pentru un site si il salveaza in report.json."""

    response = fetch(url)

    status = response.status_code
    final_url = response.url
    title = get_title(response.text)

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname

    ip = resolve(hostname)

    time.sleep(1)

    http_url = "http://" + hostname
    redirect_response = requests.get(
        http_url,
        timeout=TIMEOUT
    )

    redirects = []

    for item in redirect_response.history:
        redirects.append(
            str(item.status_code) + " -> " + item.url
        )

    if redirect_response.history:
        redirects.append(
            "Final -> " + redirect_response.url
        )

    time.sleep(1)

    headers = security_headers(url)
    security_score = score_headers(headers)

    days_left = cert_days_left(hostname)

    links = extract_links(response.text)
    internal, external = split_links(links, hostname)

    time.sleep(1)

    robots_text = fetch_robots(
        urllib.parse.urlparse(final_url).scheme
        + "://"
        + urllib.parse.urlparse(final_url).netloc
    )

    disallowed = disallowed_paths(robots_text)

    report = {
        "url": url,
        "status": status,
        "final_url": final_url,
        "title": title,
        "ip": ip,
        "redirects": redirects,
        "security_score": security_score,
        "certificate_days_left": days_left,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": disallowed
    }

    print("=== Raport site:", url, "===")
    print("Cod de stare:", status)
    print("URL final:", final_url)
    print("Titlu:", title)
    print("Adresa IP:", ip)
    print("Redirectionari:", redirects)
    print("Scor securitate:", security_score)
    print("Certificat:", days_left, "zile ramase")
    print(
        "Legaturi:",
        len(internal),
        "interne,",
        len(external),
        "externe"
    )
    print("Cai interzise:", disallowed)

    with open("report.json", "w") as file:
        json.dump(report, file, indent=2)

    print("Salvat in report.json")

    return report

if __name__ == "__main__":
    print(
        "Autotest:",
        get_status("https://cybercor.org")
    )
