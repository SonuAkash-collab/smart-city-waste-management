# Sprint 3 summary (testing and fixes)

| Item | Value |
|---|---|
| Sprint | 3 (optional sprint from the Part 3 sheet, run in parallel with testing) |
| Dates | Thu 5 Nov 2026 to Fri 6 Nov 2026 |
| Goal | Run the Test Plan, fix what it finds, update the test cases and produce the four reports |

## Work done

| Item | Owner |
|---|---|
| Fix D-1: database connection pool too small for 100 users | Sonu |
| Fix D-2: bcrypt cost slowed down simultaneous logins | Sonu |
| Report generator, CI test-report artifact, Code Coverage Report, performance summary, TC-RT-01..04, TC-PERF-01/02, TC-AVL-01, TC-MNT-01 | Haritej |
| Branch Coverage Report, Security Validation Report, deviations, TC-VEH-01/02, TC-FAC-01/02, TC-SEC-01..04 | Puru |
| Unit Test Report, TC-REQ-01..04, TC-USE-01, Sprint 2 notes, user guide, README | Rishit |
| System Validation Report, TC-AUTH-01/02, TC-NOT-01, TC-ADM-01, TC-RPT-01, traceability, Test Plan document | Sonu |

## Defects found by testing

| ID | Found by | What happened | Fix |
|---|---|---|---|
| D-1 | TC-PERF-02 (Locust, 100 users) | The default pool of 5 + 10 connections ran out; requests waited 30 s and 28 of 103 failed. | Pool of 20 + 30 connections, 10 s pool timeout, pre-ping. |
| D-2 | TC-PERF-02 | 100 logins at once queued behind 12-round bcrypt; 95th percentile 31 s. | 10 bcrypt rounds (OWASP minimum). |
| D-3 | Browser walkthrough | Facilities and Notifications pages crashed the app on leaving them. | Fixed in the same pull requests before merge. |

After the fixes: 1,493 requests, 0 failures, 95th percentile 400 ms.

## Part 3 deliverables

| Deliverable | File |
|---|---|
| Updated test cases | `docs/testplan/test-cases/TC-*.md` (execution record at the end of each) |
| Updated Test Case document | `docs/final/Team04_TestPlan_Smart_City_Waste_Management.docx` (appendix B), `docs/testplan/13-traceability.md` |
| Unit Test Report | `docs/reports/unit-test-report.md` |
| System Validation Report | `docs/reports/system-validation-report.md` |
| Code Coverage Report | `docs/reports/code-coverage-report.md` |
| Branch Coverage Report | `docs/reports/branch-coverage-report.md` |
| Extra | `docs/reports/perf-summary.md`, `docs/reports/security-validation.md` |

## Still open

* TC-USE-01 (five first-time users) and TC-AVL-01 (24-hour monitor) are ready to run; their results go into the test case files.
