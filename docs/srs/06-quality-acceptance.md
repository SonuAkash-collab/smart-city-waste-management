## 6. Quality Requirements and Acceptance Criteria

The following criteria use the registered non-functional requirements and security IDs. Acceptance targets not specified in the project context are identified as open specification items for confirmation by the project team.

### 6.1 Performance

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-001 | Route generation shall complete within the specified limit for the defined workload. | ≤ 10 s for 200 requests and 20 vehicles. | Generate routes for 200 requests and 20 vehicles; record elapsed time. Pass if completion time is ≤ 10 s. Test: TC-PERF-01. |
| SCW-NF-002 | API responses shall meet the specified response-time target under concurrent load. | 95% of API responses ≤ 2 s with 100 concurrent users. | Run the API load test with 100 concurrent users and measure response times. Pass if at least 95% of responses are ≤ 2 s. Test: TC-PERF-01. |

### 6.2 Reliability

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-003 | The system shall meet the monthly availability target. | ≥ 99% monthly availability. | Measure system availability over a calendar month. Pass if measured monthly availability is ≥ 99%. Test: covered in sprint testing; no dedicated test case is listed in the registry. |

### 6.3 Usability

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-004 | A first-time Citizen shall be able to submit a collection request without training, and the UI shall support the specified minimum screen width. | Request submission in ≤ 3 minutes; supported screen width ≥ 360 px. | Have a first-time Citizen with no training submit a request using a screen 360 px wide. Pass if the interface supports the screen width and submission completes in ≤ 3 minutes. Test: covered in sprint testing; no dedicated test case is listed in the registry. |

### 6.4 Security

#### Security Objectives

| ID | Objective | Acceptance / verification |
|---|---|---|
| SCW-SO-1 | Confidentiality of user personal data and home locations. | The project context does not define a measurable acceptance threshold or verification method for this objective. The project team must confirm one; do not treat individual security controls below as proof of the full objective. |
| SCW-SO-2 | Integrity and accountability of request, route and facility data. | The project context does not define a measurable acceptance threshold or verification method for this objective. The project team must confirm one; do not treat individual security controls below as proof of the full objective. |

#### Security Requirements

| Req ID | Security requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-SEC-001 | Passwords shall be stored only as bcrypt hashes. | No plaintext passwords in persistent storage; stored password values use bcrypt. | Inspect stored credentials for test accounts; pass if each is a bcrypt hash and no plaintext password is stored. Test: TC-SEC-01. |
| SCW-SEC-002 | JWT access tokens shall expire after 30 minutes. | Token lifetime: 30 minutes. | Verify that an otherwise valid access token is rejected after its 30-minute expiry. Test: TC-SEC-02. |
| SCW-SEC-003 | All traffic shall use HTTPS with TLS 1.2 or later. | HTTPS; TLS version ≥ 1.2. | Verify browser-to-backend traffic uses HTTPS and negotiates TLS 1.2 or later. Open specification item: the project context names OpenStreetMap and an SMTP email provider but does not define whether SCW-SEC-003 covers these external-service connections or how their transport security is to be verified; the project team must confirm both scope and verification method. Test: covered in sprint testing; no dedicated test case is listed in the registry. |
| SCW-SEC-004 | Role checks shall be enforced on the server for every API call. | Server-side role check on every API call. | Verify the TC-AUTH-02 case: a Citizen calling an Admin-only endpoint receives HTTP 403; verify the TC-SEC-02 expired/forged-token cases are rejected. These cases do not by themselves establish role enforcement for every API endpoint; sprint testing must verify role enforcement across all API endpoints. Test: TC-SEC-02, TC-AUTH-02. |
| SCW-SEC-005 | An account shall be locked for 15 minutes after 5 consecutive failed logins. | Lock after 5 consecutive failures; lock duration 15 minutes. | Submit 5 consecutive failed login attempts; pass if the account is locked for 15 minutes. Test: TC-SEC-01. |
| SCW-SEC-006 | All Admin actions—approve/reject, route generation and account changes—shall be written to an audit log. | Each listed Admin action is recorded in the audit log. | Perform each listed type of Admin action and verify a corresponding audit-log entry. Test: covered in sprint testing; no dedicated test case is listed in the registry. |

### 6.5 Maintainability

| Req ID | Quality requirement | Metric / target | Acceptance test / verification |
|---|---|---|---|
| SCW-NF-005 | Services shall be modular, and the service layer shall meet the unit-test coverage target. | ≥ 70% unit-test coverage of the service layer. | Run the service-layer unit tests with coverage measurement. Pass if measured coverage is ≥ 70%. The project context does not define a separate measurable criterion for “modular services”; the project team must confirm how modularity is to be assessed. Test: covered in sprint testing; no dedicated test case is listed in the registry. |
