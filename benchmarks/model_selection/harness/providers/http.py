import urllib.request
import urllib.error
import json

ALLOWED_HOSTS = [
    "generativelanguage.googleapis.com",
    "api.deepseek.com"
]

class SafeHTTPError(Exception):
    pass

class MissingCredential(Exception):
    pass

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SafeHTTPError(f"Redirects are disabled. Attempted redirect to {newurl}")

def safe_post(url: str, payload: dict, headers: dict, timeout: int = 15, max_response_bytes: int = 10_000_000, max_request_bytes: int = 5_000_000):
    def redact(text):
        for k, v in headers.items():
            k_lower = k.lower()
            if 'key' in k_lower or 'authorization' in k_lower:
                if v.startswith("Bearer "):
                    token = v[7:]
                    text = text.replace(token, "***")
                else:
                    text = text.replace(v, "***")
        return text

    if not url.startswith("https://"):
        raise SafeHTTPError("HTTPS required.")

    req = urllib.request.Request(url, method="POST")
    if req.host not in ALLOWED_HOSTS:
        raise SafeHTTPError(f"Host {req.host} not in allowlist.")

    for k, v in headers.items():
        req.add_header(k, v)

    req.add_header("Content-Type", "application/json")
    data = json.dumps(payload).encode("utf-8")

    if len(data) > max_request_bytes:
        raise SafeHTTPError("Request body exceeds maximum allowed size.")

    opener = urllib.request.build_opener(NoRedirectHandler())

    try:
        with opener.open(req, data=data, timeout=timeout) as response:
            ctype = response.headers.get("Content-Type", "")
            if not ctype.startswith("application/json"):
                raise SafeHTTPError(f"Unexpected Content-Type: {ctype}")

            raw_body = response.read(max_response_bytes)
            if response.read(1):
                raise SafeHTTPError("Response exceeded maximum allowed size.")

            return json.loads(raw_body.decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = redact(f"HTTP Error {e.code}: {e.reason}")
        raise SafeHTTPError(err_msg)
    except urllib.error.URLError as e:
        err_msg = redact(f"URL Error: {e.reason}")
        raise SafeHTTPError(err_msg)
    except json.JSONDecodeError:
        raise SafeHTTPError("Response was not valid JSON.")
    except SafeHTTPError:
        raise
    except Exception as e:
        err_msg = redact(f"Unexpected HTTP error.")
        raise SafeHTTPError(err_msg)
