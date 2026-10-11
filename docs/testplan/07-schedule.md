# Test Plan

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 7. Test Schedule

The project context sets the overall commitment as completing project work today and submitting tomorrow. It gives no calendar dates or durations for individual test activities. The sequence below is therefore a dependency-based planning order, not a dated or duration-based commitment; no per-activity timing or completion guarantee is implied. Test execution begins only after the Test Plan approvals required by Section 15 are recorded.

| Sequence | Testing activity / milestone | Dependency | Completion criterion |
|---|---|---|---|
| 1 | Identify the test-cycle baseline and environment | Test Plan approvals must be recorded before execution; identify the test environment and application build before running tests. | Select the application build under test and record its source revision or commit hash as described in Section 6. Use the environment and configuration described in Section 6. |
| 2 | Prepare test data and accounts | Depends on the environment and application build selected in Sequence 1. | Prepare test data and accounts needed for registered test cases and SRS acceptance criteria. Working assumption: use the separate test database and initialize or reset test records as needed to meet each test case's preconditions, as described in Section 6. |
| 3 | Execute unit and integration testing | Requires the baseline, environment and test data. | Run applicable Pytest unit and integration checks across the test items in Section 2; record each test result using the status values in Section 13. |
| 4 | Execute functional, system and acceptance testing | Requires the relevant unit and integration checks and test data. | Execute the registered functional cases: TC-AUTH-01, TC-AUTH-02, TC-NOT-01, TC-REQ-01 through TC-REQ-03, TC-VEH-01, TC-FAC-01, and TC-RT-01 through TC-RT-03. Record results against their SRS requirements. Verify requirements without dedicated cases through sprint testing as identified in Section 13. |
| 5 | Execute security validation | Requires the baseline, configured authentication and HTTPS environment, and test accounts. | Execute TC-SEC-01 and TC-SEC-02 and the security validation activities in Section 5.1. Record the outcomes against the applicable security requirements. |
| 6 | Execute performance testing | Requires the performance test data and selected load-testing tool. | Execute TC-PERF-01 against the SRS workloads: route generation for 200 approved requests and 20 vehicles, and API response-time testing with 100 concurrent users. Record measurements against SCW-NF-001 and SCW-NF-002. |
| 7 | Retest fixes and run regression checks | Requires a failed test to be fixed; Section 13 specifies rerunning a failed case after its fix. | Rerun each affected failed test case and record its updated result. Run regression checks for affected behavior and record their results. |
| 8 | Complete test-cycle reporting | Requires test execution and any required retesting to be complete. | Record the test metrics and results using Section 14. Section 15 approvals apply to the Test Plan and must be recorded before test execution. Working assumption: report the outcome using the individual test case statuses in Section 13 and measured results against their criteria; this schedule sets no additional overall pass threshold. |

The project context provides no dated milestones, activity durations, tester availability, or per-activity deadlines. Working assumption: follow the listed sequence and dependency relationships when scheduling the work, while allowing activities to overlap only when their stated dependencies are met. No dates, effort estimates, tester assignments beyond those elsewhere in the Test Plan, or completion guarantees are added here.
