import urllib.request
import urllib.error
import json

ALLOWED_HOSTS = [
    "generativelanguage.googleapis.com",
    "api.deepseek.com"
]

class SafeHTTPError(Exception):
    pass

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not allow redirects at all
        raise SafeHTTPError(f"Redirects are disabled. Attempted redirect to {newurl}")

def safe_post(url: str, payload: dict, headers: dict, timeout: int = 15, max_bytes: int = 10_000_000):
    if not url.startswith("https://"):
        raise SafeHTTPError("HTTPS required.")

    req = urllib.request.Request(url, method="POST")
    if req.host not in ALLOWED_HOSTS:
        raise SafeHTTPError(f"Host {req.host} not in allowlist.")

    for k, v in headers.items():
        req.add_header(k, v)

    req.add_header("Content-Type", "application/json")
    data = json.dumps(payload).encode("utf-8")

    opener = urllib.request.build_opener(NoRedirectHandler())
    
    try:
        with opener.open(req, data=data, timeout=timeout) as response:
            # Enforce bounded response size
            raw_body = response.read(max_bytes)
            if response.read(1):
                raise SafeHTTPError("Response exceeded maximum allowed size.")
            
            return json.loads(raw_body.decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SafeHTTPError(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise SafeHTTPError(f"URL Error: {e.reason}")
    except json.JSONDecodeError:
        raise SafeHTTPError("Response was not valid JSON.")
    except SafeHTTPError:
        raise
    except Exception as e:
        raise SafeHTTPError("Unexpected HTTP error.")
