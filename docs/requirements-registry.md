# Requirements Registry

This registry is the single reference for all requirement, security and test case IDs used in the SRS, SAD and Test Plan of the Smart City Waste Management System. Do not change or add IDs without informing the lead (Sonu Akash).

All IDs carry the prefix **`SCW-`** (e.g. `SCW-F-010`). Acceptance criteria IDs are `AC-SCW-F-010`, etc.

## 1. Functional Requirements (23)

| ID | Requirement (short) | Owner | Test case |
|---|---|---|---|
| SCW-F-001 | Users register/login with email + password; 4 roles | Sonu | TC-AUTH-01 |
| SCW-F-002 | Role-based access: each role sees only its features | Sonu | TC-AUTH-02 |
| SCW-F-003 | Admin creates/deactivates Driver and Operator accounts | Sonu | TC-ADM-01 |
| SCW-F-010 | Citizen submits request: location (map pin/address), waste type, estimated quantity, optional photo | Rishit | TC-REQ-01 |
| SCW-F-011 | System auto-assigns priority (High/Medium/Low) from waste type and request age; admin can override | Rishit | TC-REQ-02 |
| SCW-F-012 | Citizen tracks status: Submitted → Approved → Scheduled → Collected / Rejected / Missed | Rishit | TC-REQ-03 |
| SCW-F-013 | Citizen can cancel a request only before it is Scheduled | Rishit | TC-REQ-03 |
| SCW-F-014 | Admin views, filters, approves and rejects requests | Rishit | TC-REQ-04 |
| SCW-F-020 | Admin adds/edits vehicle: registration no., capacity (kg), waste types, depot location | Purushothama | TC-VEH-01 |
| SCW-F-021 | Vehicle status Available / On Route / Maintenance; only Available vehicles are used in routing | Purushothama | TC-VEH-01 |
| SCW-F-022 | Admin assigns a driver to a vehicle | Purushothama | TC-VEH-02 |
| SCW-F-023 | System tracks current load vs capacity during a route | Purushothama | TC-RT-02 |
| SCW-F-030 | Admin adds facility: location, accepted waste types, daily capacity | Purushothama | TC-FAC-02 |
| SCW-F-031 | Operator records incoming waste (vehicle, weight); remaining capacity updates | Purushothama | TC-FAC-01 |
| SCW-F-032 | Facilities that are full or don't accept the waste type are excluded | Purushothama | TC-FAC-01 |
| SCW-F-040 | Admin generates routes for a date from all Approved requests | Haritej | TC-RT-01 |
| SCW-F-041 | Stops ordered by priority first, then shortest distance | Haritej | TC-RT-01 |
| SCW-F-042 | Vehicle load never exceeds capacity; when full, route goes to the nearest suitable facility | Haritej | TC-RT-02, TC-RT-04 |
| SCW-F-043 | Driver views assigned route as ordered stops on a map | Haritej | TC-RT-03 |
| SCW-F-044 | Driver marks each stop Collected/Missed; request status updates automatically | Haritej | TC-RT-03 |
| SCW-F-050 | Citizen is notified (in-app/email) on every status change | Sonu | TC-NOT-01 |
| SCW-F-051 | Admin dashboard: pending requests, active vehicles, facility capacity | Sonu | TC-RPT-01 |
| SCW-F-052 | Admin exports daily collection report as CSV | Sonu | TC-RPT-01 |

Every functional requirement has at least one dedicated test case. Owners may add extra test cases with their own prefix (e.g. TC-REQ-04); inform the lead so the RTM is updated.

## 2. Non-Functional Requirements (owner: Haritej)

| ID | Requirement | Test case |
|---|---|---|
| SCW-NF-001 | Route generation completes in ≤ 10 s for 200 requests and 20 vehicles | TC-PERF-01 |
| SCW-NF-002 | 95% of API responses ≤ 2 s with 100 concurrent users | TC-PERF-01, TC-PERF-02 |
| SCW-NF-003 | ≥ 99% monthly availability | TC-AVL-01 |
| SCW-NF-004 | A first-time citizen can submit a request in ≤ 3 minutes without training; UI works on screens ≥ 360 px wide | TC-USE-01 |
| SCW-NF-005 | Modular services; ≥ 70% unit-test coverage of the service layer | TC-MNT-01 |

## 3. Security (owner: Purushothama)

| ID | Item | Test case |
|---|---|---|
| SCW-SO-1 | **Objective:** confidentiality of user personal data and home locations | – |
| SCW-SO-2 | **Objective:** integrity and accountability of request, route and facility data | – |
| SCW-SEC-001 | Passwords stored only as bcrypt hashes | TC-SEC-01 |
| SCW-SEC-002 | JWT access tokens expire after 30 minutes | TC-SEC-02 |
| SCW-SEC-003 | All traffic over HTTPS (TLS 1.2+) | TC-SEC-03 |
| SCW-SEC-004 | Role checks enforced on the server for every API call | TC-SEC-02, TC-AUTH-02 |
| SCW-SEC-005 | Account locked for 15 minutes after 5 consecutive failed logins | TC-SEC-01 |
| SCW-SEC-006 | All admin actions (approve/reject, route generation, account changes) written to an audit log | TC-SEC-04 |

## 4. Test Cases (26)

| TC ID | Covers | Owner |
|---|---|---|
| TC-AUTH-01 | F-001 valid/invalid login | Sonu |
| TC-AUTH-02 | F-002, SEC-004 citizen blocked from admin endpoint (403) | Sonu |
| TC-NOT-01 | F-050 notification sent on status change | Sonu |
| TC-REQ-01 | F-010 submit valid request / reject missing location | Rishit |
| TC-REQ-02 | F-011 priority auto-assignment + admin override | Rishit |
| TC-REQ-03 | F-012, F-013 status tracking; cancel blocked after Scheduled (409) | Rishit |
| TC-RT-01 | F-040, F-041 route ordering by priority then distance | Haritej |
| TC-RT-02 | F-042, F-023 capacity never exceeded; detour to facility | Haritej |
| TC-RT-03 | F-043, F-044 driver views route, marks stop, request updates | Haritej |
| TC-PERF-01 | NF-001, NF-002 load/performance | Haritej |
| TC-VEH-01 | F-020, F-021 add vehicle; Maintenance vehicle excluded | Purushothama |
| TC-FAC-01 | F-031, F-032 intake reduces capacity; full facility excluded | Purushothama |
| TC-SEC-01 | SEC-001, SEC-005 hashed password; lockout after 5 failures | Purushothama |
| TC-SEC-02 | SEC-002, SEC-004 expired/forged token rejected | Purushothama |
| TC-ADM-01 | F-003 Admin creates and deactivates Driver/Operator accounts | Rishit |
| TC-RPT-01 | F-051, F-052 Admin dashboard figures and daily CSV report export | Haritej |
| TC-REQ-04 | F-014 Admin views, filters, approves and rejects requests | Rishit |
| TC-RT-04 | F-042 nearest suitable facility chosen when vehicle is full | Haritej |
| TC-PERF-02 | NF-002 API response time under 100 concurrent users | Haritej |
| TC-AVL-01 | NF-003 monthly availability ≥ 99% | Haritej |
| TC-USE-01 | NF-004 first-time citizen submits request in ≤ 3 min; UI at ≥ 360 px | Haritej |
| TC-MNT-01 | NF-005 ≥ 70% unit-test coverage of the service layer | Haritej |
| TC-VEH-02 | F-022 driver assignment to a vehicle | Purushothama |
| TC-FAC-02 | F-030 add facility with input validation | Purushothama |
| TC-SEC-03 | SEC-003 HTTPS enforced with TLS 1.2+ | Purushothama |
| TC-SEC-04 | SEC-006 audit log records admin actions | Purushothama |

### Test case file format

One file per test case: `docs/testplan/test-cases/TC-XXX-NN.md`

| Field | Content |
|---|---|
| TC ID | TC-REQ-01 |
| Title | … |
| Requirement(s) | SCW-F-010 |
| Type | Functional / Performance / Security |
| Preconditions | … |
| Test data | … |
| Steps | 1. … 2. … |
| Expected result | … (measurable) |
| Actual result | (blank) |
| Status | Not run |
