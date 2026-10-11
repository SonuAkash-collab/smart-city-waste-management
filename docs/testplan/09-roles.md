# Test Plan

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 9. Roles and Responsibilities

This section distinguishes Team 04's documented project and testing assignments from the user roles whose functions are tested. Test case owners and Test Plan section owners follow the project work division and Test Plan reporting conventions.

### 9.1 Team 04 Responsibilities

| Team member | Project/team role | Test Plan sections assigned | Testing and reporting responsibilities documented in the sources |
|---|---|---|---|
| Sonu Akash | Lead / integrator; repo owner | Sections 1, 2, 13, 14 and 15 | Owns TC-AUTH-01, TC-AUTH-02 and TC-NOT-01. Test case owners record their test results; test case owners prepare the test cycle report, which Sonu compiles. Sonu prepares the traceability status at the end of each test cycle and the test summary report at the end of testing. |
| Rishit V N S | Team member | Sections 6–9 | Owns TC-REQ-01, TC-REQ-02 and TC-REQ-03. As a test case owner, records the Actual result and Status for assigned cases during test cycles. |
| Rottela Haritej | Team member | Sections 3–5 | Owns TC-RT-01, TC-RT-02, TC-RT-03 and TC-PERF-01. Prepares the performance report for each performance test run. As a test case owner, records the Actual result and Status for assigned cases during test cycles. |
| Purushothama KC | Team member | Sections 5.1 and 10–12 | Owns TC-VEH-01, TC-FAC-01, TC-SEC-01 and TC-SEC-02. As a test case owner, records the Actual result and Status for assigned cases during test cycles. |

When a tester finds a defect, the tester prepares the defect report as a GitHub Issue with the documented TC ID, requirement ID, reproduction steps, expected and actual results, severity, and screenshot or log. Its intended audience is the developer responsible for the component. Working assumption: defect handling in this plan ends with the documented GitHub Issue and its intended audience; this section assigns no defect triage, issue-assignment, or escalation responsibility.

The approval section lists the four team members for signatures confirming review of the Test Plan and agreement with its scope, approach, schedule and responsibilities. It identifies Sonu Akash as lead / integrator and test manager, Rishit V N S as tester for collection requests, Rottela Haritej as tester for route generation and performance, and Purushothama KC as tester for vehicles, facilities and security. Testing starts only after all approvals are recorded.

### 9.2 System User Roles in Test Scope

These are application roles described in the SRS, not additional Test Plan owners or test staff assignments.

| System role | Documented system responsibility |
|---|---|
| Citizen | Submits and tracks waste collection requests, cancels requests before they become Scheduled, and receives status notifications. |
| Collection Vehicle Driver | Views the assigned route and marks stops Collected or Missed. |
| Admin / Municipal Officer | Approves or rejects requests, overrides priority, manages vehicles, facilities and accounts, generates routes, views the dashboard, and exports reports. |
| Disposal Facility Operator | Records incoming waste and manages facility capacity. |

The test cases may use these roles as test actors where specified in their preconditions or steps. Application-role actors are not assigned responsibility for conducting or approving system tests; test execution ownership is limited to the team assignments in Section 9.1, and approval is recorded by the signatories listed in Section 15.

### 9.3 Open Responsibility Decisions

- Working assumption: system-wide activities without a named test case owner have no additional individual execution owner assigned by this section; the documented named test case owners retain responsibility for their cases.
- The project context assigns PR reviewer pairs (Sonu Akash ↔ Rishit V N S; Rottela Haritej ↔ Purushothama KC) for pull requests. Those pairs are not assigned Test Plan or test-result review responsibilities here; approval remains limited to the signatures and testing-start condition documented in Section 15.
