## 13. Test Case Management & Traceability

### 13.1 Test Case Management

- Each test case is stored as one Markdown file in `docs/testplan/test-cases/TC-<AREA>-<NN>.md`, using the fields TC ID, Title, Requirement(s), Type, Preconditions, Test data, Steps, Expected result, Actual result and Status.
- Test case IDs are fixed in the Requirements Registry. New test cases use the owner's prefix with the next free number (e.g. `TC-REQ-04`) and are added to this matrix and to the SRS RTM by the lead (Sonu Akash).
- Status values: **Not run**, **Pass**, **Fail**, **Blocked**. Actual result and Status are filled in during each test cycle.
- Failed test cases are logged as GitHub Issues labelled `bug`, referencing the TC ID and requirement ID; the test case is re-run after the fix (regression).

### 13.2 Requirements → Test Cases

Every requirement ID has at least one dedicated test case. Security objectives (SCW-SO-x) are verified through the test cases of the security requirements that implement them.

#### Functional requirements

| Req ID | Requirement (short) | Test case(s) | Coverage |
|---|---|---|---|
| SCW-F-001 | Register/login with email + password; 4 roles | TC-AUTH-01 | Test case |
| SCW-F-002 | Role-based access: each role sees only its features | TC-AUTH-02 | Test case |
| SCW-F-003 | Admin creates/deactivates Driver and Operator accounts | TC-ADM-01 | Test case |
| SCW-F-010 | Citizen submits request: location, waste type, quantity, optional photo | TC-REQ-01 | Test case |
| SCW-F-011 | Priority auto-assigned from waste type and age; admin override | TC-REQ-02 | Test case |
| SCW-F-012 | Citizen tracks request status | TC-REQ-03 | Test case |
| SCW-F-013 | Citizen cancels only before Scheduled | TC-REQ-03 | Test case |
| SCW-F-014 | Admin views, filters, approves and rejects requests | TC-REQ-04 | Test case |
| SCW-F-020 | Admin adds/edits vehicle | TC-VEH-01 | Test case |
| SCW-F-021 | Vehicle status; only Available vehicles routed | TC-VEH-01 | Test case |
| SCW-F-022 | Admin assigns a driver to a vehicle | TC-VEH-02 | Test case |
| SCW-F-023 | Track current load vs capacity during a route | TC-RT-02 | Test case |
| SCW-F-030 | Admin adds facility: location, waste types, daily capacity | TC-FAC-02 | Test case |
| SCW-F-031 | Operator records incoming waste; remaining capacity updates | TC-FAC-01 | Test case |
| SCW-F-032 | Full or unsuitable facilities excluded | TC-FAC-01 | Test case |
| SCW-F-040 | Admin generates routes for a date from Approved requests | TC-RT-01 | Test case |
| SCW-F-041 | Stops ordered by priority, then shortest distance | TC-RT-01 | Test case |
| SCW-F-042 | Load never exceeds capacity; detour to nearest suitable facility | TC-RT-02, TC-RT-04 | Test case |
| SCW-F-043 | Driver views assigned route on a map | TC-RT-03 | Test case |
| SCW-F-044 | Driver marks stop Collected/Missed; request status updates | TC-RT-03 | Test case |
| SCW-F-050 | Citizen notified on every status change | TC-NOT-01 | Test case |
| SCW-F-051 | Admin dashboard: pending requests, vehicles, facility capacity | TC-RPT-01 | Test case |
| SCW-F-052 | Admin exports daily collection report as CSV | TC-RPT-01 | Test case |

#### Non-functional requirements

| Req ID | Requirement (short) | Test case(s) | Coverage |
|---|---|---|---|
| SCW-NF-001 | Route generation ≤ 10 s for 200 requests and 20 vehicles | TC-PERF-01 | Test case |
| SCW-NF-002 | 95% of API responses ≤ 2 s with 100 concurrent users | TC-PERF-01, TC-PERF-02 | Test case |
| SCW-NF-003 | ≥ 99% monthly availability | TC-AVL-01 | Test case |
| SCW-NF-004 | First-time citizen submits a request in ≤ 3 min; UI works at ≥ 360 px | TC-USE-01 | Test case |
| SCW-NF-005 | Modular services; ≥ 70% unit-test coverage of the service layer | TC-MNT-01 | Test case |

#### Security objectives and requirements

| Req ID | Requirement (short) | Test case(s) | Coverage |
|---|---|---|---|
| SCW-SO-1 | Objective: confidentiality of user personal data and home locations | TC-SEC-01, TC-SEC-02, TC-SEC-03, TC-AUTH-02 | Objective; verified through SCW-SEC-001 – SCW-SEC-005 |
| SCW-SO-2 | Objective: integrity and accountability of request, route and facility data | TC-SEC-02, TC-AUTH-02, TC-SEC-04 | Objective; verified through SCW-SEC-004, SCW-SEC-006 |
| SCW-SEC-001 | Passwords stored only as bcrypt hashes | TC-SEC-01 | Test case |
| SCW-SEC-002 | JWT access tokens expire after 30 minutes | TC-SEC-02 | Test case |
| SCW-SEC-003 | All traffic over HTTPS (TLS 1.2+) | TC-SEC-03 | Test case |
| SCW-SEC-004 | Role checks enforced on the server for every API call | TC-SEC-02, TC-AUTH-02 | Test case |
| SCW-SEC-005 | Account locked 15 min after 5 consecutive failed logins | TC-SEC-01 | Test case |
| SCW-SEC-006 | All admin actions written to an audit log | TC-SEC-04 | Test case |

### 13.3 Test Cases → Requirements

| TC ID | Requirement(s) | Type | Owner |
|---|---|---|---|
| TC-AUTH-01 | SCW-F-001 | Functional | Sonu Akash |
| TC-AUTH-02 | SCW-F-002, SCW-SEC-004 | Security | Sonu Akash |
| TC-ADM-01 | SCW-F-003 | Functional | Sonu Akash |
| TC-NOT-01 | SCW-F-050 | Functional | Sonu Akash |
| TC-RPT-01 | SCW-F-051, SCW-F-052 | Functional | Sonu Akash |
| TC-REQ-01 | SCW-F-010 | Functional | Rishit V N S |
| TC-REQ-02 | SCW-F-011 | Functional | Rishit V N S |
| TC-REQ-03 | SCW-F-012, SCW-F-013 | Functional | Rishit V N S |
| TC-REQ-04 | SCW-F-014 | Functional | Rishit V N S |
| TC-RT-01 | SCW-F-040, SCW-F-041 | Functional | Rottela Haritej |
| TC-RT-02 | SCW-F-042, SCW-F-023 | Functional | Rottela Haritej |
| TC-RT-03 | SCW-F-043, SCW-F-044 | Functional | Rottela Haritej |
| TC-RT-04 | SCW-F-042 | Functional | Rottela Haritej |
| TC-PERF-01 | SCW-NF-001, SCW-NF-002 | Performance | Rottela Haritej |
| TC-PERF-02 | SCW-NF-002 | Performance | Rottela Haritej |
| TC-AVL-01 | SCW-NF-003 | Reliability | Rottela Haritej |
| TC-USE-01 | SCW-NF-004 | Usability | Rottela Haritej |
| TC-MNT-01 | SCW-NF-005 | Maintainability | Rottela Haritej |
| TC-VEH-01 | SCW-F-020, SCW-F-021 | Functional | Purushothama KC |
| TC-VEH-02 | SCW-F-022 | Functional / Authorization | Purushothama KC |
| TC-FAC-01 | SCW-F-031, SCW-F-032 | Functional | Purushothama KC |
| TC-FAC-02 | SCW-F-030 | Functional | Purushothama KC |
| TC-SEC-01 | SCW-SEC-001, SCW-SEC-005 | Security | Purushothama KC |
| TC-SEC-02 | SCW-SEC-002, SCW-SEC-004 | Security | Purushothama KC |
| TC-SEC-03 | SCW-SEC-003 | Security | Purushothama KC |
| TC-SEC-04 | SCW-SEC-006 | Security | Purushothama KC |

### 13.4 Coverage Summary

| Category | Total IDs | Covered by a dedicated test case | Covered through security requirement test cases | Coverage |
|---|---|---|---|---|
| Functional (SCW-F) | 23 | 23 | – | 100% |
| Non-functional (SCW-NF) | 5 | 5 | – | 100% |
| Security requirements (SCW-SEC) | 6 | 6 | – | 100% |
| Security objectives (SCW-SO) | 2 | – | 2 | 100% |
| **Total** | **36** | **34** | **2** | **100%** |

The plan contains 26 test cases. All 26 trace to at least one requirement ID, and all 36 requirement IDs are covered by at least one test case (100% requirements coverage).
