import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
     return "https://"+ host + "/" + path.lstrip("/")

    """Returnează o adresă completă, de exemplu https://example.com/login."""
    pass


def is_https(url):
        return url.startswith("https://")

    """Returnează True dacă adresa începe cu https://, altfel False."""
    pass


def show_response(url):
 try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))
    except requests.exceptions.RequestException as e:
        print("Eroare:", str(e))
    """Trimite un GET la url și afișează statusul și Content-Type."""
    pass


def check_site(url):
             try:
        response = requests.get(url, timeout=5)

        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown")
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }



    """Returnează un dicționar cu: status, content_type, length, server."""
    pass
       

def scan_sites():
   


      for url in SITES:
        rezultat = check_site(url)
        rezultate.append((url, rezultat))

    reusite = []

    for url, rezultat in rezultate:
        if rezultat["status"] == 200:
            reusite.append((url, rezultat))

    reusite.sort(
        key=lambda x: x[1]["length"],
        reverse=True
    )

    for url, rezultat in reusite:
        print(url, "->", rezultat["status"],
              ",", rezultat["length"], "octeti")

    print("Reusite:", len(reusite),
          "| Esuate:", len(rezultate) - len(reusite))


 """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    pass


def check_headers(url):
   try:
        response = requests.get(url, timeout=5)

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header in response.headers:
                present.append(header)
            else:
                missing.append(header)

        score = int(len(present) / len(SECURITY_HEADERS) * 100)

        return {
            "present": present,
            "missing": missing,
            "score": score
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }
 

"""Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    
def retry_check(url, attempts=3):
    last_status = None
    last_error = None
    received_response = False

    for i in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            received_response = True

            if last_status < 500:
                return {
                    "status": last_status,
                    "attempts": i + 1
                }

        except requests.exceptions.RequestException as e:
            last_error = str(e)

    rezultat = {
        "status": last_status,
        "attempts": max(0, attempts)
    }

    if not received_response:
        rezultat["error"] = last_error or "Cererea a esuat"

    return rezultat




    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
