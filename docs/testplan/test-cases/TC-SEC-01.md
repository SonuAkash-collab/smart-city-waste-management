# TC-SEC-01: Password Hashing and Account Lockout

| Field | Content |
|---|---|
| TC ID | TC-SEC-01 |
| Title | Verify bcrypt password storage and login lockout |
| Requirement(s) | SCW-SEC-001, SCW-SEC-005 |
| Type | Security |
| Preconditions | 1. The system is deployed in a test environment over HTTPS. 2. A test account exists with known credentials. 3. The account is initially active and unlocked. |
| Test data | Email: `citizen1@test.local`; valid password: `Citizen@123`; invalid password: `Wrong@123`. |
| Steps | 1. Register or inspect the test account using an authorized test database or administrative test tool. 2. Verify that the stored password is a bcrypt hash and is not the plaintext password. 3. Submit four consecutive login attempts with an incorrect password. 4. Verify that the account has not yet been locked. 5. Submit a fifth consecutive incorrect login attempt. 6. Attempt to log in with the correct password during the 15-minute lockout. 7. After 15 minutes have elapsed, attempt to log in with the correct password. 8. After a successful login, perform a new sequence of failed login attempts and verify that the counter starts from zero. |
| Expected result | 1. The stored password is a bcrypt hash; plaintext passwords are not stored. 2. The first four consecutive failures do not trigger lockout. 3. The fifth consecutive failure triggers a 15-minute lockout. 4. Login is blocked during the lockout, even with the correct password. 5. After the lockout expires, valid credentials permit login. 6. A successful login resets the consecutive-failure counter. |
| Actual result | To be filled during testing. |
| Status | Not run |