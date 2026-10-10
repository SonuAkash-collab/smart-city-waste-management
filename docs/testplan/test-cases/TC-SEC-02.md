# TC-SEC-02: JWT Expiry and Role-Based Access Control

| Field | Content |
|---|---|
| TC ID | TC-SEC-02 |
| Title | Verify JWT expiration and protected API authorization |
| Requirement(s) | SCW-SEC-002, SCW-SEC-004 |
| Type | Security |
| Preconditions | 1. The system is available in the test environment over HTTPS. 2. An active Admin account and an active Citizen account exist. 3. Protected API endpoints are available. |
| Test data | Valid Admin JWT; valid Citizen JWT; expired JWT; missing JWT; endpoint requiring Admin privileges. |
| Steps | 1. Log in as Admin and obtain a JWT. 2. Verify the token's expiration time is 30 minutes after issuance. 3. Call a protected endpoint with the valid Admin token. 4. Call the same endpoint without a token. 5. Call the endpoint using an expired token. 6. Call an Admin-only endpoint using a valid Citizen token. 7. Attempt to access a protected endpoint over unencrypted HTTP, if the test environment exposes an HTTP endpoint. |
| Expected result | 1. The JWT expires 30 minutes after issuance. 2. A valid authorized token permits access. 3. Missing or expired tokens are rejected with HTTP 401. 4. An authenticated user without the required role is rejected with HTTP 403. 5. Protected data is not returned over unencrypted HTTP; the request is rejected or redirected to HTTPS. |
| Actual result | To be filled during testing. |
| Status | Not run |