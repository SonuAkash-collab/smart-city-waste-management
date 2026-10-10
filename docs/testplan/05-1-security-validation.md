
# 5.1 Security Validation

## 5.1.1 Purpose

This section defines the security validation approach for the Smart City Waste Management System. The objective is to verify that authentication, authorization, password protection, secure communication, and account lockout behavior satisfy the security requirements in the SRS.

## 5.1.2 Security Requirements Under Test

| Requirement ID | Security Requirement | Validation Method | Expected Result |
|---|---|---|---|
| SCW-SEC-001 | Passwords are stored only as bcrypt hashes. | Inspect password storage and verify the stored value is a bcrypt hash rather than plaintext. | Plaintext passwords are not stored. |
| SCW-SEC-002 | JWT access tokens expire after 30 minutes. | Submit requests using a valid token and an expired token. | Expired tokens are rejected with HTTP 401. |
| SCW-SEC-003 | All traffic uses HTTPS with TLS 1.2 or later. | Inspect deployment configuration and verify the negotiated TLS version. | Protected traffic uses HTTPS with TLS 1.2 or later. |
| SCW-SEC-004 | Server-side role checks are enforced for every API call. | Access protected endpoints using authorized and unauthorized roles. | Unauthorized actions are rejected with HTTP 403. Unauthenticated requests are rejected with HTTP 401. |
| SCW-SEC-005 | Accounts are locked for 15 minutes after five consecutive failed login attempts. | Perform five consecutive failed login attempts and verify lockout behavior. | The account is locked for 15 minutes according to the configured policy. |
| SCW-SEC-006 | Administrative actions are written to audit logs. | Perform representative approval/rejection, route-generation, and account-change actions and inspect the audit records. | Required administrative events are recorded. |

## 5.1.3 Validation Procedures

### A. Password Hashing

1. Create a test account with a known test password.
2. Inspect the stored password field using an authorized test environment.
3. Verify that the stored value is a bcrypt hash and does not contain the original plaintext password.
4. Confirm that valid login succeeds and invalid credentials are rejected.

Related test case: `TC-SEC-01`.

### B. JWT Expiration and Role Authorization

1. Authenticate using a valid test account.
2. Submit a request with a valid token and confirm that access follows the assigned role.
3. Submit a request using an expired token.
4. Submit a request using a forged or invalid token.
5. Attempt to access a protected endpoint without the required role.

Expected results: expired, forged, or invalid tokens are rejected; authenticated users cannot perform actions outside their authorized role.

Related test case: `TC-SEC-02`.

### C. HTTPS and TLS

1. Inspect the deployment's HTTPS configuration.
2. Verify that the negotiated TLS version is TLS 1.2 or later.
3. Verify that protected application traffic is not transmitted over insecure HTTP.
4. Record the configuration and verification results.

This check requires a configured deployment or test environment that supports HTTPS.

### D. Account Lockout

1. Use a dedicated test account.
2. Submit five consecutive incorrect login attempts.
3. Verify that further login attempts are blocked during the 15-minute lockout period.
4. Verify behavior after the lockout expires.
5. Record the observed results.

Related test case: `TC-SEC-01`.

### E. Audit Logging

1. Perform representative administrative actions in the test environment.
2. Inspect the corresponding audit records.
3. Verify that each required event contains sufficient information to identify the action and its outcome.
4. Confirm that passwords, access tokens, and other secrets are not written to logs.

## 5.1.4 Entry Criteria

- The application and relevant authentication endpoints are available in a test environment.
- Test accounts with appropriate roles have been prepared.
- The database and logging configuration are accessible to authorized testers.
- HTTPS is configured for deployment-level TLS verification.

## 5.1.5 Exit Criteria

- All applicable security validation checks have been executed.
- Expected and actual results are documented.
- Failed checks are recorded as defects for review.
- Any unexecuted checks are documented with the reason they could not be performed.

## 5.1.6 Evidence and Reporting

For each validation, record the test date, environment, procedure, expected result, actual result, status, and any supporting evidence. Tests that have not been executed must remain marked as not run; they must not be reported as passed.
