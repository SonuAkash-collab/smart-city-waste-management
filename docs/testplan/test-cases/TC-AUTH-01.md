### TC-AUTH-01: Valid and invalid login

| Field | Content |
|---|---|
| TC ID | TC-AUTH-01 |
| Title | Valid and invalid login with email and password |
| Requirement(s) | SCW-F-001 |
| Type | Functional |
| Preconditions | 1. System is deployed in the test environment and reachable over HTTPS. 2. One active account exists for each role: Citizen, Driver, Admin, Operator. 3. No account is currently locked. |
| Test data | Citizen: `citizen1@test.local` / `Citizen@123`; Driver: `driver1@test.local` / `Driver@123`; Admin: `admin1@test.local` / `Admin@123`; Operator: `operator1@test.local` / `Operator@123`; wrong password: `Wrong@123`; unregistered email: `nobody@test.local` |
| Steps | 1. Send `POST /api/v1/auth/login` with the Citizen's email and correct password. 2. Decode the returned JWT and read its role claim. 3. Repeat steps 1–2 for the Driver, Admin and Operator accounts. 4. Send `POST /api/v1/auth/login` with the Citizen's email and the wrong password. 5. Send `POST /api/v1/auth/login` with the unregistered email and any password. 6. Send `POST /api/v1/auth/login` with an empty email field. |
| Expected result | Steps 1–3: HTTP 200 for each of the 4 accounts; response contains a JWT whose role claim equals the account role (Citizen, Driver, Admin, Operator) and whose expiry is 30 minutes after issue. Steps 4–5: HTTP 401, body `{ "error": { "code": "INVALID_CREDENTIALS", … } }`, no token returned; the response does not reveal whether the email exists. Step 6: HTTP 422 with a validation error and no token. |
| Actual result | |
| Status | Not run |
