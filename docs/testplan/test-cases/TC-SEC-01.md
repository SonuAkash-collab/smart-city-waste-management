# TC-SEC-01: Password Hashing and Account Lockout

| Field | Details |
|---|---|
| TC ID | TC-SEC-01 |
| Title | Verify bcrypt password hashing and login lockout |
| Requirement(s) | SCW-SEC-001, SCW-SEC-005 |
| Type | Security |
| Priority | High |
| Preconditions | 1. The authentication service and test database are available. 2. A dedicated test account exists with known credentials. 3. The account is active and initially unlocked. |
| Test Data | Test account: `security_test_user`; valid password: `TestPass!123`; invalid password: `WrongPass!123`; lockout threshold: five consecutive failed attempts; lockout duration: 15 minutes. |
| Actual Result | To be recorded during test execution. |
| Status | Not run |

## Test Steps

### Part A: Password Hashing

| Step | Action | Expected Result |
|---|---|---|
| 1 | Create a test account using the valid test password. | The account is created successfully. |
| 2 | Inspect the stored password value using an authorized test database or administrative test tool. | The stored value is a bcrypt hash, not the plaintext password. |
| 3 | Log in using the correct password. | Authentication succeeds. |
| 4 | Log in using an incorrect password before the account is locked. | Authentication fails without revealing sensitive information. |

### Part B: Account Lockout

| Step | Action | Expected Result |
|---|---|---|
| 5 | Submit four consecutive login attempts with an incorrect password. | All attempts are rejected, and the account is not yet locked. |
| 6 | Attempt to log in with the correct password after the four failed attempts. | Login succeeds, and the account remains unlocked. |
| 7 | Submit five consecutive login attempts with an incorrect password. | The fifth consecutive failure triggers a 15-minute lockout. |
| 8 | Attempt to log in with the correct password during the lockout period. | Login remains blocked during the lockout. |
| 9 | After 15 minutes have elapsed, attempt to log in with the correct password. | Authentication succeeds if no other restriction applies. |
| 10 | After a successful login, submit a new sequence of failed login attempts. | The consecutive-failure counter starts from zero. |

## Pass/Fail Criteria

**Pass:** Passwords are stored using bcrypt hashing; the first four consecutive failures do not trigger lockout; the fifth failure triggers a 15-minute lockout; login remains blocked during lockout; valid login works after expiry; and successful login resets the failure counter.

**Fail:** Passwords are stored in plaintext, the lockout threshold or duration is incorrect, login is permitted during lockout, or the failure counter does not reset as specified.

## Evidence

Record the test environment, actual results, and relevant logs. Do not include plaintext passwords, access tokens, or other secrets in screenshots or reports. Keep the status as Not run until the test has been executed.