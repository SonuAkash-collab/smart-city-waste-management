"""Transport security (SCW-SEC-003).

* With FORCE_HTTPS=1 every plain-HTTP request is redirected to HTTPS.
* Security headers go on every response; HSTS is added when HTTPS is forced.

TLS itself is handled by the web server, for example:
    uvicorn app.main:app --ssl-keyfile key.pem --ssl-certfile cert.pem
"""

import os

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, hsts: bool = False):
        super().__init__(app)
        self.hsts = hsts

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        if self.hsts:
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000")
        return response


def apply_transport_security(app: FastAPI, force_https: bool | None = None) -> None:
    if force_https is None:
        force_https = os.getenv("FORCE_HTTPS", "0") == "1"
    app.add_middleware(SecurityHeadersMiddleware, hsts=force_https)
    if force_https:
        app.add_middleware(HTTPSRedirectMiddleware)
