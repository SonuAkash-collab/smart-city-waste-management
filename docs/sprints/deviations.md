# Deviations from the submitted SRS, SAD and Test Plan

These are the places where the built system differs from the documents submitted on 11 Oct 2026, and why. They are explained during the final demo.

| # | Document | What the document says | What we built | Why |
|---|---|---|---|---|
| 1 | Part 2 plan | Sprint 1: 19–23 Oct, Sprint 2: 26–30 Oct | Sprint 1: 29 Oct–1 Nov, Sprint 2: 2–4 Nov, testing (Sprint 3): 5–6 Nov | The team received the Part 2 instructions late. |
| 2 | SAD 3.6 | React web frontend | React 18 loaded as browser builds with `htm` templates, served by FastAPI from `frontend/`; no bundler | One command runs the whole app; no Node build step for anyone on the team. |
| 3 | SAD 3.6 | PostgreSQL | SQLite by default for development, tests and demos; PostgreSQL works by setting `DATABASE_URL` | No database server to install on every laptop; the SQLAlchemy code is the same for both. |
| 4 | SAD 4.3 Route Service | Base path `/api`; `PATCH /api/routes/{route_id}/stops/{request_id}/status`; responses with `success` | Base path `/api/v1` like all other APIs; `PATCH /api/v1/routes/{id}/stops/{stopId}`; `GET /api/v1/routes/assigned` kept; no `success` field (errors use the common error body) | One consistent API; facility stops have no request id, so stops are addressed by their own id. |
| 5 | SAD 4.3 | JSON field names only shown for requests | camelCase JSON for every API (snake_case input is still accepted) | Consistency with the Request Service contract. |
| 6 | SRS F-040, F-021 | Routes use Available vehicles | Only Available vehicles **with an assigned driver**; vehicles take turns choosing their next stop; each route ends with an unloading stop when the vehicle carries waste | A route nobody drives cannot be run; turns spread work over the fleet; loads must be emptied (F-023). |
| 7 | SRS F-012 / design question | — | No `scheduled_date` column: a request's date is read from its route | Avoids storing the same date twice. |
| 8 | SRS F-050 | Email through an email provider | SMTP when `SMTP_HOST` is set, otherwise each email is written to `email-outbox.log` | The demo works without a mail server; MailHog can be plugged in through `SMTP_HOST`. |
| 9 | SRS F-010 | Location by map pin or address | The API needs coordinates; the web app turns a typed address into coordinates with OpenStreetMap Nominatim | Routing needs coordinates; geocoding belongs to the Map Service. |
| 10 | SRS SEC-005 | Lockout; status code not stated | Locked accounts get HTTP 403 with code `ACCOUNT_LOCKED` | 403 = known user, not allowed right now. |
| 11 | SAD security | bcrypt (rounds not stated) | 10 rounds, pool of 20 + 30 database connections | Defects D-1 and D-2 found in the load test (see `sprint-3.md`). |
| 12 | SRS SEC-003 | All traffic over HTTPS | HTTPS comes from the server's certificate; `FORCE_HTTPS=1` redirects HTTP; the local demo runs on HTTP | Certificates belong to deployment, not to the code. |
| 13 | Test cases | Waste types Wet, Dry, Household; some fields not defined | Agreed waste type codes (MIXED, RECYCLABLE, ...); test cases updated with the real endpoints and fields | Test data now matches the API. |
| 14 | SRS F-003 | Admin manages accounts | The first Admin is created with `backend/scripts/create_admin.py`; Admins cannot create other Admins from the app | There must be a first Admin, and Admin rights should not be handed out from the web page. |
| 15 | SRS F-020 | Vehicle management is Admin-only | Operators may also read the vehicle list | Operators pick the delivering vehicle when they record an intake (F-031). |
