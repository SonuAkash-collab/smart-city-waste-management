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
