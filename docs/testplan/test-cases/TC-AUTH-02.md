### TC-AUTH-02: Citizen blocked from Admin endpoint

| Field | Content |
|---|---|
| TC ID | TC-AUTH-02 |
| Title | Citizen is blocked from Admin-only endpoints (role-based access) |
| Requirement(s) | SCW-F-002, SCW-SEC-004 |
| Type | Security |
| Preconditions | 1. System is deployed in the test environment. 2. An active Citizen account and an active Admin account exist. 3. At least one collection request in status Submitted exists. |
| Test data | Citizen: `citizen1@test.local` / `Citizen@123`; Admin: `admin1@test.local` / `Admin@123`; route date: `2026-10-11`; ID of an existing Submitted request |
| Steps | 1. Log in as the Citizen and store the JWT. 2. With the Citizen's JWT, send `POST /api/v1/routes/generate` with body `{ "date": "2026-10-11" }`. 3. With the Citizen's JWT, send `PATCH /api/v1/requests/{id}/status` with body `{ "status": "APPROVED" }` for the Submitted request. 4. Send the request from step 2 directly to the API (e.g. with Postman), bypassing the Web Frontend. 5. Log in to the Web Frontend as the Citizen and check the navigation menu. 6. Log in as the Admin and repeat step 2 with the Admin's JWT. |
| Expected result | Steps 2–4: HTTP 403 with body `{ "error": { "code": "FORBIDDEN", … } }` in every attempt; no route is created and the request remains in status Submitted. Step 5: the Citizen's menu shows no Admin, Driver or Operator items. Step 6: HTTP 200 or 201 (Admin is allowed), confirming the 403 in steps 2–4 is caused by the role check. |
| Actual result | |
| Status | Not run |
