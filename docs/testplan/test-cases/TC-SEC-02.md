# TC-SEC-02: JWT Expiry and Role-Based Access Control

| Field | Details |
|---|---|
| TC ID | TC-SEC-02 |
| Title | Verify JWT expiry, role-based access control, and HTTPS security |
| Requirement(s) | SCW-SEC-002, SCW-SEC-003, SCW-SEC-004 |
| Type | Security |
| Priority | High |
| Preconditions | The application and authentication service are running. Test accounts with Admin and Citizen roles are available. HTTPS is configured in the test environment. |
| Test Data | Valid Admin token, valid Citizen token, expired token, malformed token, missing token, and an endpoint restricted to Admin users. |
| Status | Not run |

## Test Steps

### Part A: JWT Authentication and Expiry

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in using valid credentials. | Authentication succeeds and a JWT is issued. |
| 2 | Inspect the token expiry configuration or claims. | The token expires after 30 minutes, according to SCW-SEC-002. |
| 3 | Access a protected endpoint using a valid token. | The request succeeds if the user is authorized. |
| 4 | Access a protected endpoint using an expired token. | The request is rejected with HTTP 401 Unauthorized. |
| 5 | Submit a malformed or forged token. | The request is rejected with HTTP 401 Unauthorized. |
| 6 | Access a protected endpoint without a token. | The request is rejected with HTTP 401 Unauthorized. |

### Part B: Server-Side Role-Based Access Control

| Step | Action | Expected Result |
|---|---|---|
| 7 | Access an Admin-only endpoint using a valid Admin token. | The request is permitted if all other authorization conditions are satisfied. |
| 8 | Access the same Admin-only endpoint using a valid Citizen token. | The request is rejected with HTTP 403 Forbidden. |
| 9 | Attempt to change the role through client-side data or request parameters. | The server does not grant additional privileges based on client-side role changes. |
| 10 | Submit a request to a restricted endpoint without the required role. | The server rejects the request, and protected data is not exposed. |

### Part C: HTTPS Transport Security

| Step | Action | Expected Result |
|---|---|---|
| 11 | Attempt to access the application or protected API over plain HTTP. | Plain HTTP is rejected or redirected to HTTPS without exposing protected data over an insecure connection. |
| 12 | Inspect the HTTPS connection configuration. | TLS 1.2 or higher is supported for secure transport. |

## Pass/Fail Criteria

**Pass:** JWTs expire after 30 minutes; missing, malformed, forged, and expired tokens are rejected; server-side role checks prevent unauthorized access; client-side role manipulation cannot bypass authorization; and protected traffic is secured using HTTPS with TLS 1.2 or higher.

**Fail:** Expired or invalid tokens are accepted, Citizens can access Admin-only endpoints, client-side role changes grant privileges, or protected data is exposed over insecure HTTP.

## Evidence

Record the test environment, actual HTTP status codes, relevant sanitized logs, and test results. Do not include passwords, complete JWTs, or other secrets in screenshots or reports.