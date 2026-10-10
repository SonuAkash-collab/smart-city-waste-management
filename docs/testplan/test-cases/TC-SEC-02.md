# TC-SEC-02: JWT Expiry and Role-Based Access Control

| Field | Details |
|---|---|
| TC ID | TC-SEC-02 |
| Title | Verify JWT expiration, token validation, HTTPS enforcement and server-side role checks |
| Requirement(s) | SCW-SEC-002, SCW-SEC-003, SCW-SEC-004 |
| Type | Security |
| Priority | High |
| Preconditions | 1. The authentication service and protected API endpoints are available. 2. Active Admin and Citizen test accounts exist. 3. The test environment supports HTTPS. |
| Test Data | Valid Admin JWT, valid Citizen JWT, expired JWT, forged or malformed JWT, missing JWT, and an endpoint requiring Admin privileges. |
| Actual Result | To be recorded during test execution. |
| Status | Not run |

## Test Steps

### Part A: JWT Validation and Expiry

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in using valid Admin credentials and obtain a JWT. | Authentication succeeds and a JWT is issued. |
| 2 | Inspect the token's issuance and expiry times using an authorized test tool. | The token expires 30 minutes after issuance. |
| 3 | Send a request to a protected endpoint using the valid Admin token. | The request succeeds if the Admin is authorized for the action. |
| 4 | Send a request using an expired JWT. | The request is rejected with HTTP 401. |
| 5 | Send a request using a forged, malformed, or invalidly signed JWT. | The request is rejected with HTTP 401. |
| 6 | Send a request without an access token to a protected endpoint. | The request is rejected with HTTP 401. |

### Part B: Server-Side Role Checks

| Step | Action | Expected Result |
|---|---|---|
| 7 | Access an Admin-only endpoint using a valid Admin JWT. | The authorized action is permitted. |
| 8 | Access the same Admin-only endpoint using a valid Citizen JWT. | The request is rejected with HTTP 403. |
| 9 | Attempt to access a protected endpoint while manipulating client-side role information. | The server enforces permissions using trusted server-side authorization information. |

### Part C: HTTPS Enforcement

| Step | Action | Expected Result |
|---|---|---|
| 10 | Attempt to access a protected endpoint over unencrypted HTTP, if an HTTP endpoint is exposed in the test environment. | The request is rejected or redirected to HTTPS, and protected data is not returned over unencrypted HTTP. |
| 11 | Access the protected endpoint over HTTPS. | The connection uses TLS 1.2 or later. |

## Pass/Fail Criteria

**Pass:** JWTs expire after 30 minutes; expired, forged, malformed and missing tokens are rejected; server-side role checks enforce permissions; and protected communication uses HTTPS with TLS 1.2 or later.

**Fail:** An invalid token is accepted, token expiry is incorrect, role restrictions can be bypassed, or protected data is exposed over unencrypted HTTP.

## Evidence

Record the endpoint, request conditions, HTTP status code, observed result, and relevant logs for each step. Do not include live access tokens or secrets in screenshots or reports. Keep the status as Not run until the test has been executed.