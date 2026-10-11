## 6. Quality Requirements and Acceptance Criteria

The following criteria use the registered non-functional requirements and security IDs. Where the project context and SRS Sections 4 and 5 leave a verification detail open, this section states a narrow working assumption for acceptance; it does not imply team confirmation.

### 6.1 Performance

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-001 | Route generation shall complete within 10 seconds for 200 approved requests and 20 vehicles. | ≤ 10 s for 200 requests and 20 vehicles. | Generate routes for 200 approved requests and 20 vehicles; record elapsed time. Pass if completion time is ≤ 10 s. Test: TC-PERF-01. |
| SCW-NF-002 | At least 95% of API responses shall complete within 2 seconds under 100 concurrent users. | 95% of API responses ≤ 2 s with 100 concurrent users. | Run the API load test with 100 concurrent users and measure response times. Pass if at least 95% of responses are ≤ 2 s. Test: TC-PERF-01. |

### 6.2 Reliability

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-003 | The system shall maintain at least 99% monthly availability. | ≥ 99% monthly availability. | Working assumption: calculate monthly availability as recorded uptime divided by recorded uptime plus recorded downtime. Apply only downtime exclusions documented and formally agreed before measurement begins, as required by SCW-NF-003. Pass if availability is ≥ 99%. Test: covered in sprint testing; no dedicated test case is listed in the registry. |

### 6.3 Usability

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-004 | A first-time Citizen shall be able to submit a collection request without training, and the UI shall support screens at least 360 px wide. | Request submission in ≤ 3 minutes; supported screen width ≥ 360 px. | Have a first-time Citizen with no training submit a request using a screen 360 px wide. Pass if the interface supports the screen width and submission completes in ≤ 3 minutes. Test: covered in sprint testing; no dedicated test case is listed in the registry. |

### 6.4 Security

#### Security Objectives

| ID | Objective | Acceptance / verification |
|---|---|---|
| SCW-SO-1 | Confidentiality of user personal data and home locations. | Working assumption: use the defined controls as limited acceptance evidence by verifying stored passwords are bcrypt hashes (SCW-SEC-001) and protected API requests enforce authentication and role checks (SCW-SEC-004). These checks do not establish protection against every possible disclosure path. |
| SCW-SO-2 | Integrity and accountability of request, route and facility data. | Working assumption: use the defined controls as limited acceptance evidence by verifying protected API requests enforce role checks (SCW-SEC-004) and each listed Admin action creates an audit record with the actor, action, timestamp and affected record identifier where applicable (SCW-SEC-006). This does not establish a separate system-wide data-integrity guarantee. |

#### Security Requirements

| Req ID | Security requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-SEC-001 | Passwords shall be stored only as bcrypt hashes. | No plaintext passwords in persistent storage; stored password values use bcrypt. | Inspect stored credentials for test accounts; pass if each is a bcrypt hash and no plaintext password is stored. Test: TC-SEC-01. |
| SCW-SEC-002 | JWT access tokens shall expire after 30 minutes. | Token lifetime: 30 minutes. | Verify that an otherwise valid access token is rejected after its 30-minute expiry. Test: TC-SEC-02. |
| SCW-SEC-003 | All traffic shall use HTTPS with TLS 1.2 or later. | HTTPS; TLS version ≥ 1.2. | Working assumption: apply this acceptance check to browser-to-backend client-server traffic, matching the detailed wording of SCW-SEC-003 in SRS Section 5.1. Verify HTTPS and negotiated TLS 1.2 or later. This check does not assert a separate verification criterion for connections to OpenStreetMap or the SMTP email provider. Test: TC-SEC-03. |
| SCW-SEC-004 | Role checks shall be enforced on the server for every protected API request. | Server-side role check on every protected API request. | Verify the TC-AUTH-02 case: a Citizen calling an Admin-only endpoint receives HTTP 403; verify the TC-SEC-02 expired/forged-token cases are rejected. As those cases alone do not cover every protected endpoint, sprint testing must verify role enforcement across all protected API endpoints. Test: TC-SEC-02, TC-AUTH-02. |
| SCW-SEC-005 | An account shall be locked for 15 minutes after 5 consecutive failed logins. | Lock after 5 consecutive failures; lock duration 15 minutes. | Verify the first four consecutive failures do not trigger lockout and the fifth does; further attempts are blocked during the 15-minute lockout, valid login is permitted after expiry, and successful login resets the failure counter. Test: TC-SEC-01. |
| SCW-SEC-006 | All Admin actions—approve/reject, route generation and account changes—shall be written to an audit log. | Each listed Admin action is recorded in the audit log. | Perform each listed type of Admin action and verify its audit record contains the actor, action, timestamp and affected record identifier where applicable. Test: TC-SEC-04. |

### 6.5 Maintainability

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-005 | Services shall be modular, and the service layer shall meet the unit-test coverage target. | ≥ 70% unit-test coverage of the service layer. | Run the service-layer unit tests with coverage measurement. Pass if measured coverage is ≥ 70%. Working assumption: assess modularity by reviewing whether service responsibilities map to the named components and layered architecture in project context Sections 4.2–4.3. This is a qualitative review and does not add a separate quantitative threshold. Test: covered in sprint testing; no dedicated test case is listed in the registry. |
