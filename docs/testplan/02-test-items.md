## 2. Test Items

The following components of the Smart City Waste Management System, version 1.0, are under test. Component names match SAD Section 3.4.

| # | Test item | Description | Requirements covered | Test cases | Test levels |
|---|---|---|---|---|---|
| 1 | Web Frontend | React web application (mobile-responsive) for all four roles, including map views with Leaflet/OpenStreetMap | SCW-F-002, SCW-F-043, SCW-NF-004 | TC-AUTH-02, TC-RT-03 | System, acceptance, usability |
| 2 | Auth & User Service | Registration, login, JWT issue/validation, roles, account management, lockout | SCW-F-001 – SCW-F-003, SCW-SEC-001, SCW-SEC-002, SCW-SEC-004, SCW-SEC-005 | TC-AUTH-01, TC-AUTH-02, TC-SEC-01, TC-SEC-02 | Unit, integration, system, security |
| 3 | Request Service | Create, track, cancel, approve and reject collection requests; priority assignment | SCW-F-010 – SCW-F-014 | TC-REQ-01, TC-REQ-02, TC-REQ-03 | Unit, integration, system |
| 4 | Fleet Service | Vehicles, driver assignment, vehicle status, load tracking | SCW-F-020 – SCW-F-023 | TC-VEH-01, TC-RT-02 | Unit, integration, system |
| 5 | Facility Service | Disposal facilities, waste intake, remaining capacity | SCW-F-030 – SCW-F-032 | TC-FAC-01 | Unit, integration, system |
| 6 | Route Optimization Engine | Route generation (priority, distance, capacity), driver stop updates | SCW-F-040 – SCW-F-044, SCW-NF-001 | TC-RT-01, TC-RT-02, TC-RT-03, TC-PERF-01 | Unit, integration, system, performance |
| 7 | Notification & Reporting Service | Status-change notifications, Admin dashboard, CSV report export | SCW-F-050 – SCW-F-052 | TC-NOT-01 | Unit, integration, system |
| 8 | Database (PostgreSQL) | Persistent storage of users, requests, vehicles, facilities, routes, notifications and audit log | Supports all requirements; SCW-SEC-001 (hash storage), SCW-SEC-006 (audit log) | Verified indirectly through the test cases above | Integration |
| 9 | REST API (`/api/v1`) | All service endpoints, status codes and error body format | SCW-NF-002, SCW-SEC-004 | TC-PERF-01, TC-AUTH-02, TC-SEC-02 | Integration, system, performance |

**Version under test:** build of the `main` branch tagged for each test cycle; the commit hash is recorded in each test run report (Section 14).

**Items not tested:** the Map Service (OpenStreetMap) and the email provider are external systems and are replaced by stubs or used as-is; their internals are not tested (see Section 4).
