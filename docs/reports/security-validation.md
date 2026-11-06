# Security Validation Report

Covers Test Plan section 5.1 and SCW-SO-1, SCW-SO-2, SCW-SEC-001 to SCW-SEC-006.
Automated checks run in CI on every pull request; the TLS check was run by hand on a local server.

| Requirement | Check | Evidence | Result |
|---|---|---|---|
| SCW-SEC-001 bcrypt | Stored password starts with `$2b$` and never contains the plain text | `test_security_lockout.py::test_password_stored_as_bcrypt_hash`, `test_auth.py::test_register_creates_citizen` | Pass |
| SCW-SEC-002 30-minute JWT | `exp - iat` is 1,800 s; tokens 31 minutes old are refused (401 TOKEN_EXPIRED) | `test_auth.py::test_login_returns_token_with_role`, `test_expired_token_rejected` | Pass |
| SCW-SEC-003 HTTPS / TLS 1.2+ | Local uvicorn with a self-signed certificate: TLS 1.3 negotiated, TLS 1.1 refused. FORCE_HTTPS=1 redirects plain HTTP (307) without data and adds HSTS. | `test_transport.py`; manual run with Python `ssl` | Pass (local) |
| SCW-SEC-004 server-side roles | Every protected endpoint uses `require_roles`; the role comes from the database, so a token that claims ADMIN for a citizen still gets 403 | `test_auth.py::test_role_comes_from_database_not_token`, 403 tests in every API test file | Pass |
| SCW-SEC-005 lockout | 5 failures in a row lock for 15 minutes; a good login resets the counter | `test_security_lockout.py` | Pass |
| SCW-SEC-006 audit log | Approve, reject, route generation and account changes are logged with actor, action, record id and time | `test_audit.py` | Pass |
| Input validation | Bad email, short password, missing location, non-positive weights and capacities, unknown waste types all return 422 with the common error body | `test_auth.py`, `test_requests_submit.py`, `test_facilities.py`, `test_vehicles.py` | Pass |
| Injection | All database access goes through SQLAlchemy with bound parameters; no SQL is built from strings | Code review of `app/services` | Pass |
| Error bodies | Errors use `{"error": {"code", "message"}}`; unexpected errors return a generic 500 without stack traces | `app/core/errors.py`, `test_web.py::test_unknown_api_path_gives_json_error` | Pass |
| Security headers | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin` on every response | `test_transport.py::test_security_headers_always_present` | Pass |

## STRIDE follow-up (SAD 3.9)

| Threat | Mitigation in the code |
|---|---|
| Spoofing | bcrypt passwords, signed JWTs, lockout after 5 failures |
| Tampering | Role checks on the server for every change; status transitions validated (409 INVALID_STATUS_TRANSITION) |
| Repudiation | Audit log of Admin actions |
| Information disclosure | Citizens only see their own requests (403 otherwise); login does not reveal whether an email exists |
| Denial of service | Load test: 100 users, 95th percentile 400 ms after fixes D-1 and D-2 (`perf-summary.md`) |
| Elevation of privilege | Self-registration always creates a Citizen; staff accounts only by an Admin |

## Open points

* Production needs a real certificate and `FORCE_HTTPS=1`; the local demo runs on HTTP.
* `SECRET_KEY` must be set to a long random value outside development.
