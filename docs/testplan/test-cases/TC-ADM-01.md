### TC-ADM-01: Create and deactivate Driver and Operator accounts

| Field | Content |
|---|---|
| TC ID | TC-ADM-01 |
| Title | Verify Admin account creation and deactivated-user login rejection |
| Requirement(s) | SCW-F-003 |
| Type | Functional |
| Objective | Verify that an Admin can create Driver and Operator accounts, that each account can log in with its assigned role, and that a deactivated account cannot log in. |
| Preconditions | 1. The Auth & User Service and Web Frontend are reachable in the test environment. 2. An authenticated Admin context is available. Working assumption: the test environment supplies the configured API base URL and Admin identity with bearer token; this case prescribes no URL, credentials, or provisioning method. 3. No account used in this test is locked. The project defines a 15-minute lockout after five consecutive failed logins; this test uses successful logins and one deactivated-account login attempt. |
| Test data | Prepare distinct Driver and Operator account details with the documented fields: name, unique email address, role, and temporary password assigned by the Admin. Use the Driver account as the deactivation target. Do not use fixed credentials or assume a password value. |
| Steps | 1. As Admin, use the documented account-management function to create a Driver account with its name, email, Driver role, and temporary password. 2. Repeat to create an Operator account with its name, email, Operator role, and temporary password. 3. Using each account's assigned email and temporary password, call `POST /api/v1/auth/login`; record the HTTP result and the role claim in the returned JWT. 4. As Admin, use the documented account-management function to deactivate the Driver account. 5. Attempt to log in as that Driver using `POST /api/v1/auth/login` and its assigned email and temporary password; record the HTTP status. |
| Expected result | Steps 1–2: The Admin account-management function creates each account with its assigned role. The project documents the account fields but does not define an account-creation endpoint, request body schema, success status, or response body. Steps 3: Each login returns HTTP 200 with a JWT whose role claim matches the created account's role (Driver or Operator). Step 4: The Admin account-management function deactivates the Driver account; the project does not define a deactivation endpoint, request schema, success status, or response body. Step 5: Login for the deactivated Driver returns HTTP 401, as required by SCW-F-003; no specific error body is prescribed for this case. |
| Pass/fail criteria | Pass if the Admin can create both accounts with their assigned roles, the Driver and Operator can each log in with HTTP 200 and receive a JWT with the matching role claim, and the deactivated Driver's login returns HTTP 401. Fail if any supported outcome differs. Mark account creation or deactivation checks Blocked if the documented account-management function is unavailable; do not substitute an undocumented endpoint or payload. |
| Actual result | |
| Status | Not run |

The account fields, Admin authority, deactivation behavior, and HTTP 401 criterion are specified by SRS Section 4.1. Successful login status and role-bearing JWT behavior are specified by SRS Section 4.1; `POST /api/v1/auth/login` is used as documented in `TC-AUTH-01`. The account-creation and deactivation API contracts (paths, request schemas, success responses) are not defined in the available project documents.
