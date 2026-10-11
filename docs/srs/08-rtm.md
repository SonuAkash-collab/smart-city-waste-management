## 8. Requirements Traceability Matrix (RTM)

This matrix links every requirement ID in this SRS to the design component that implements it (primary component from SAD Section 3.8) and to the test cases that verify it (Test Plan Section 13). IDs and test case references follow `docs/requirements-registry.md`.

### 8.1 Authentication & Roles

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-F-001 | Users register/login with email + password; 4 roles | Auth & User Service | TC-AUTH-01 |
| SCW-F-002 | Role-based access: each role sees only its features | Auth & User Service | TC-AUTH-02 |
| SCW-F-003 | Admin creates/deactivates Driver and Operator accounts | Auth & User Service | TC-ADM-01 |

### 8.2 Collection Requests

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-F-010 | Citizen submits request: location (map pin/address), waste type, estimated quantity, optional photo | Request Service | TC-REQ-01 |
| SCW-F-011 | System auto-assigns priority (High/Medium/Low) from waste type and request age; admin can override | Request Service | TC-REQ-02 |
| SCW-F-012 | Citizen tracks status: Submitted → Approved → Scheduled → Collected / Rejected / Missed | Request Service | TC-REQ-03 |
| SCW-F-013 | Citizen can cancel a request only before it is Scheduled | Request Service | TC-REQ-03 |
| SCW-F-014 | Admin views, filters, approves and rejects requests | Request Service | TC-REQ-04 |

### 8.3 Vehicle Management

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-F-020 | Admin adds/edits vehicle: registration no., capacity (kg), waste types, depot location | Fleet Service | TC-VEH-01 |
| SCW-F-021 | Vehicle status Available / On Route / Maintenance; only Available vehicles are used in routing | Fleet Service | TC-VEH-01 |
| SCW-F-022 | Admin assigns a driver to a vehicle | Fleet Service | TC-VEH-02 |
| SCW-F-023 | System tracks current load vs capacity during a route | Fleet Service | TC-RT-02 |

### 8.4 Facility Management

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-F-030 | Admin adds facility: location, accepted waste types, daily capacity | Facility Service | TC-FAC-02 |
| SCW-F-031 | Operator records incoming waste (vehicle, weight); remaining capacity updates | Facility Service | TC-FAC-01 |
| SCW-F-032 | Facilities that are full or don't accept the waste type are excluded | Facility Service | TC-FAC-01 |

### 8.5 Route Generation

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-F-040 | Admin generates routes for a date from all Approved requests | Route Optimization Engine | TC-RT-01 |
| SCW-F-041 | Stops ordered by priority first, then shortest distance | Route Optimization Engine | TC-RT-01 |
| SCW-F-042 | Vehicle load never exceeds capacity; when full, route goes to the nearest suitable facility | Route Optimization Engine | TC-RT-02, TC-RT-04 |
| SCW-F-043 | Driver views assigned route as ordered stops on a map | Route Optimization Engine | TC-RT-03 |
| SCW-F-044 | Driver marks each stop Collected/Missed; request status updates automatically | Route Optimization Engine | TC-RT-03 |

### 8.6 Notifications & Reports

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-F-050 | Citizen is notified (in-app/email) on every status change | Notification & Reporting Service | TC-NOT-01 |
| SCW-F-051 | Admin dashboard: pending requests, active vehicles, facility capacity | Notification & Reporting Service | TC-RPT-01 |
| SCW-F-052 | Admin exports daily collection report as CSV | Notification & Reporting Service | TC-RPT-01 |

### 8.7 Non-Functional Requirements

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-NF-001 | Route generation completes in ≤ 10 s for 200 requests and 20 vehicles | Route Optimization Engine | TC-PERF-01 |
| SCW-NF-002 | 95% of API responses ≤ 2 s with 100 concurrent users | All services (Auth & User, Request, Fleet, Facility, Route Optimization Engine, Notification & Reporting) | TC-PERF-01, TC-PERF-02 |
| SCW-NF-003 | ≥ 99% monthly availability | All services | TC-AVL-01 |
| SCW-NF-004 | A first-time citizen can submit a request in ≤ 3 minutes without training; UI works on screens ≥ 360 px wide | Web Frontend | TC-USE-01 |
| SCW-NF-005 | Modular services; ≥ 70% unit-test coverage of the service layer | All services | TC-MNT-01 |

### 8.8 Security Objectives and Requirements

| Req ID | Description | Design component (SAD 3.8) | Test case(s) |
|---|---|---|---|
| SCW-SO-1 | Objective: confidentiality of user personal data and home locations | Auth & User Service | TC-SEC-01, TC-SEC-02, TC-SEC-03, TC-AUTH-02 (via SCW-SEC-001 – SCW-SEC-005) |
| SCW-SO-2 | Objective: integrity and accountability of request, route and facility data | All services | TC-SEC-02, TC-AUTH-02, TC-SEC-04 (via SCW-SEC-004, SCW-SEC-006) |
| SCW-SEC-001 | Passwords stored only as bcrypt hashes | Auth & User Service | TC-SEC-01 |
| SCW-SEC-002 | JWT access tokens expire after 30 minutes | Auth & User Service | TC-SEC-02 |
| SCW-SEC-003 | All traffic over HTTPS (TLS 1.2+) | Web Frontend | TC-SEC-03 |
| SCW-SEC-004 | Role checks enforced on the server for every API call | Auth & User Service | TC-SEC-02, TC-AUTH-02 |
| SCW-SEC-005 | Account locked for 15 minutes after 5 consecutive failed logins | Auth & User Service | TC-SEC-01 |
| SCW-SEC-006 | All admin actions (approve/reject, route generation, account changes) written to an audit log | Auth & User Service | TC-SEC-04 |

### 8.9 Coverage Summary

| Category | Requirement IDs | IDs with at least one test case | Coverage |
|---|---|---|---|
| Functional (SCW-F) | 23 | 23 | 100% |
| Non-functional (SCW-NF) | 5 | 5 | 100% |
| Security objectives (SCW-SO) | 2 | 2 (through security requirement test cases) | 100% |
| Security requirements (SCW-SEC) | 6 | 6 | 100% |
| **Total** | **36** | **36** | **100%** |

- Every one of the 36 requirement IDs maps to a design component in SAD Section 3.8 and to at least one of the 26 test cases in the Test Plan.
- Every test case traces back to at least one requirement ID (Test Plan Section 13.3).
