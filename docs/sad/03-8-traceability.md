### 3.8 Traceability to Requirements

This section maps every requirement ID in the SRS to the component that implements it (primary component) and the components it depends on (supporting components). Component names are those in Section 3.4. Test case references are those in the Test Plan; "–" means the requirement has no dedicated test case and is covered in sprint testing.

#### 3.8.1 Functional Requirements

| Req ID | Requirement (short) | Primary component | Supporting components | Test case(s) |
|---|---|---|---|---|
| SCW-F-001 | Register/login with email + password; 4 roles | Auth & User Service | Web Frontend, Database (PostgreSQL) | TC-AUTH-01 |
| SCW-F-002 | Role-based access: each role sees only its features | Auth & User Service | Web Frontend, all services (server-side role check) | TC-AUTH-02 |
| SCW-F-003 | Admin creates/deactivates Driver and Operator accounts | Auth & User Service | Web Frontend, Database (PostgreSQL) | – |
| SCW-F-010 | Citizen submits request: location, waste type, quantity, optional photo | Request Service | Web Frontend, Map Service (OpenStreetMap), Database (PostgreSQL) | TC-REQ-01 |
| SCW-F-011 | Priority auto-assigned from waste type and age; admin override | Request Service | Web Frontend, Database (PostgreSQL) | TC-REQ-02 |
| SCW-F-012 | Citizen tracks request status | Request Service | Web Frontend, Notification & Reporting Service | TC-REQ-03 |
| SCW-F-013 | Citizen cancels only before Scheduled | Request Service | Web Frontend | TC-REQ-03 |
| SCW-F-014 | Admin views, filters, approves and rejects requests | Request Service | Web Frontend, Notification & Reporting Service | – |
| SCW-F-020 | Admin adds/edits vehicle | Fleet Service | Web Frontend, Database (PostgreSQL) | TC-VEH-01 |
| SCW-F-021 | Vehicle status; only Available vehicles routed | Fleet Service | Route Optimization Engine | TC-VEH-01 |
| SCW-F-022 | Admin assigns a driver to a vehicle | Fleet Service | Auth & User Service, Web Frontend | – |
| SCW-F-023 | Track current load vs capacity during a route | Fleet Service | Route Optimization Engine | TC-RT-02 |
| SCW-F-030 | Admin adds facility: location, waste types, daily capacity | Facility Service | Web Frontend, Map Service (OpenStreetMap), Database (PostgreSQL) | – |
| SCW-F-031 | Operator records incoming waste; remaining capacity updates | Facility Service | Web Frontend, Database (PostgreSQL) | TC-FAC-01 |
| SCW-F-032 | Full or unsuitable facilities excluded | Facility Service | Route Optimization Engine | TC-FAC-01 |
| SCW-F-040 | Admin generates routes for a date from Approved requests | Route Optimization Engine | Request Service, Fleet Service, Facility Service, Web Frontend | TC-RT-01 |
| SCW-F-041 | Stops ordered by priority, then shortest distance | Route Optimization Engine | Map Service (OpenStreetMap) | TC-RT-01 |
| SCW-F-042 | Load never exceeds capacity; detour to nearest suitable facility | Route Optimization Engine | Fleet Service, Facility Service | TC-RT-02 |
| SCW-F-043 | Driver views assigned route on a map | Route Optimization Engine | Web Frontend, Map Service (OpenStreetMap) | TC-RT-03 |
| SCW-F-044 | Driver marks stop Collected/Missed; request status updates | Route Optimization Engine | Request Service, Notification & Reporting Service, Web Frontend | TC-RT-03 |
| SCW-F-050 | Citizen notified on every status change | Notification & Reporting Service | Request Service, Route Optimization Engine | TC-NOT-01 |
| SCW-F-051 | Admin dashboard: pending requests, vehicles, facility capacity | Notification & Reporting Service | Request Service, Fleet Service, Facility Service, Web Frontend | – |
| SCW-F-052 | Admin exports daily collection report as CSV | Notification & Reporting Service | Route Optimization Engine, Database (PostgreSQL) | – |

#### 3.8.2 Non-Functional Requirements

| Req ID | Requirement (short) | Primary component | Supporting components | Test case(s) |
|---|---|---|---|---|
| SCW-NF-001 | Route generation ≤ 10 s for 200 requests and 20 vehicles | Route Optimization Engine | Database (PostgreSQL) | TC-PERF-01 |
| SCW-NF-002 | 95% of API responses ≤ 2 s with 100 concurrent users | All services (Auth & User, Request, Fleet, Facility, Route Optimization Engine, Notification & Reporting) | Database (PostgreSQL) | TC-PERF-01 |
| SCW-NF-003 | ≥ 99% monthly availability | All services | Database (PostgreSQL), Web Frontend | – |
| SCW-NF-004 | First-time citizen submits a request in ≤ 3 min; UI works at ≥ 360 px | Web Frontend | Request Service, Map Service (OpenStreetMap) | – |
| SCW-NF-005 | Modular services; ≥ 70% unit-test coverage of the service layer | All services | – | – |

#### 3.8.3 Security Objectives and Requirements

| Req ID | Requirement (short) | Primary component | Supporting components | Test case(s) |
|---|---|---|---|---|
| SCW-SO-1 | Objective: confidentiality of user personal data and home locations | Auth & User Service | Request Service, Database (PostgreSQL), Web Frontend | – |
| SCW-SO-2 | Objective: integrity and accountability of request, route and facility data | All services | Database (PostgreSQL) | – |
| SCW-SEC-001 | Passwords stored only as bcrypt hashes | Auth & User Service | Database (PostgreSQL) | TC-SEC-01 |
| SCW-SEC-002 | JWT access tokens expire after 30 minutes | Auth & User Service | All services (token validation) | TC-SEC-02 |
| SCW-SEC-003 | All traffic over HTTPS (TLS 1.2+) | Web Frontend | All services | – |
| SCW-SEC-004 | Role checks enforced on the server for every API call | Auth & User Service | All services | TC-SEC-02, TC-AUTH-02 |
| SCW-SEC-005 | Account locked 15 min after 5 consecutive failed logins | Auth & User Service | Database (PostgreSQL) | TC-SEC-01 |
| SCW-SEC-006 | All admin actions written to an audit log | Auth & User Service | Request Service, Route Optimization Engine, Fleet Service, Facility Service, Database (PostgreSQL) | – |

#### 3.8.4 Component Coverage Summary

| Component | Primary for |
|---|---|
| Web Frontend | SCW-NF-004, SCW-SEC-003 |
| Auth & User Service | SCW-F-001 – SCW-F-003, SCW-SO-1, SCW-SEC-001, SCW-SEC-002, SCW-SEC-004 – SCW-SEC-006 |
| Request Service | SCW-F-010 – SCW-F-014 |
| Fleet Service | SCW-F-020 – SCW-F-023 |
| Facility Service | SCW-F-030 – SCW-F-032 |
| Route Optimization Engine | SCW-F-040 – SCW-F-044, SCW-NF-001 |
| Notification & Reporting Service | SCW-F-050 – SCW-F-052 |
| All services (shared) | SCW-NF-002, SCW-NF-003, SCW-NF-005, SCW-SO-2 |
| Database (PostgreSQL) | Supporting component for persistent storage of all requirements above |
| Map Service (OpenStreetMap) | Supporting component for SCW-F-010, SCW-F-030, SCW-F-041, SCW-F-043, SCW-NF-004 |

All 23 functional requirements, 5 non-functional requirements, 2 security objectives and 6 security requirements are assigned to at least one component.
