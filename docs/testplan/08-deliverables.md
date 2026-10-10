# Test Plan

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 8. Test Deliverables

The following deliverables are defined by the project context, SRS, or Test Plan. The project commitment is to complete project work today and submit tomorrow; no separate calendar due dates are documented for individual test deliverables.

| Deliverable | Purpose and expected contents | Owner / timing |
|---|---|---|
| Test Plan | Defines the test scope, test items, features to be tested or excluded, approach, security validation, environment, schedule, deliverables, roles, risks, assumptions, suspension criteria, traceability, metrics and approvals. The plan is organized into one Markdown file per section. | Section owners are assigned in the project work division: Sonu Akash—Sections 1, 2, 13, 14 and 15; Rottela Haritej—Sections 3–5; Rishit V N S—Sections 6–9; Purushothama KC—Sections 5.1 and 10–12. No per-section due dates are specified. |
| Test case files | Fourteen test cases verify registered functional, non-functional and security requirements. Each case uses the documented fields: TC ID, Title, Requirement(s), Type, Preconditions, Test data, Steps, Expected result, Actual result and Status. The Actual result and Status are recorded during a test cycle. | The project work division assigns the cases to their owners listed below. The project context specifies one Markdown file per test case under `docs/testplan/test-cases/`. |
| Test case execution results | Record the observed Actual result and Status (Not run, Pass, Fail or Blocked) in each test case file. Results are used to report test execution and traceability status. | Test case owner records results during each test cycle. |
| Test cycle report | Reports the commit hash under test, test cases run, pass/fail/blocked counts and new defects by severity. | Prepared by test case owners and compiled by Sonu Akash at the end of each test cycle; audience: Team 04. |
| Defect report | A GitHub Issue per defect, labelled `bug` and with severity `critical`, `major` or `minor`; includes TC ID, requirement ID, reproduction steps, expected versus actual result, severity, and screenshot or log. | Prepared by the tester who finds the defect when it is found; intended audience: the developer responsible for the component. |
| Traceability status | Section 13 matrix updated with the latest status of each requirement. | Prepared by Sonu Akash at the end of each test cycle; audience: Team 04 and the course instructor. |
| Performance report | Locust/JMeter results for TC-PERF-01, including response-time percentiles, throughput and error rate. | Prepared by Rottela Haritej for each performance test run; audience: Team 04. |
| Test summary report | Final metrics against Section 14.1 targets, open defects and a release recommendation. | Prepared by Sonu Akash at the end of testing; audience: Team 04 and the course instructor. |
| Test Plan approvals | Signatures and dates recording review of the Test Plan and agreement with its scope, approach, schedule and responsibilities. The approval table includes the four team members and a course instructor / faculty reviewer. Testing starts only after all approvals are recorded. | Signers are the listed team members and course instructor / faculty reviewer. No approval date is specified. |

### Test Case Inventory

| TC ID | Coverage | Owner |
|---|---|---|
| TC-AUTH-01 | SCW-F-001: valid and invalid login | Sonu Akash |
| TC-AUTH-02 | SCW-F-002, SCW-SEC-004: Citizen blocked from Admin endpoint | Sonu Akash |
| TC-NOT-01 | SCW-F-050: notification on status change | Sonu Akash |
| TC-REQ-01 | SCW-F-010: valid request submission and rejection of missing location | Rishit V N S |
| TC-REQ-02 | SCW-F-011: automatic priority and Admin override | Rishit V N S |
| TC-REQ-03 | SCW-F-012, SCW-F-013: status tracking and cancellation before Scheduled | Rishit V N S |
| TC-RT-01 | SCW-F-040, SCW-F-041: route ordering by priority then distance | Rottela Haritej |
| TC-RT-02 | SCW-F-042, SCW-F-023: vehicle capacity and facility detour | Rottela Haritej |
| TC-RT-03 | SCW-F-043, SCW-F-044: route viewing and stop updates | Rottela Haritej |
| TC-PERF-01 | SCW-NF-001, SCW-NF-002: route generation and API performance | Rottela Haritej |
| TC-VEH-01 | SCW-F-020, SCW-F-021: vehicle management and availability | Purushothama KC |
| TC-FAC-01 | SCW-F-031, SCW-F-032: waste intake, capacity update and facility exclusion | Purushothama KC |
| TC-SEC-01 | SCW-SEC-001, SCW-SEC-005: password hashing and account lockout | Purushothama KC |
| TC-SEC-02 | SCW-SEC-002, SCW-SEC-004: token expiry and role enforcement | Purushothama KC |

The SRS defines measurable acceptance criteria and verification for requirements; test cases map to those requirements through Section 13. Requirements without a dedicated test case are identified as covered in sprint testing. The sources do not define a separate acceptance certificate or additional completion evidence beyond recorded test results, reports, traceability status and the Test Plan approvals described above.

### Open Deliverable Decisions

- No calendar due dates or durations are provided for individual deliverables, test cycles, reports or approvals.
- The source documents do not specify a storage location or file format for test cycle, defect, performance or summary reports beyond defect reports being GitHub Issues and execution results being recorded in test case files.
- The source documents do not define acceptance/sign-off evidence separate from the SRS acceptance criteria, test results, reports and Test Plan approval records.
