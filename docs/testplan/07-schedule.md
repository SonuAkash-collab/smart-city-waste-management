# Test Plan

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 7. Test Schedule

The project context states that project work is to be completed today and submission is tomorrow. It does not state calendar dates for test activities or their durations. Accordingly, the sequence below is a dependency-based planning order, not a dated or duration-based commitment. The project team must confirm the execution dates and any changes needed to meet the submission deadline.

| Sequence | Testing activity / milestone | Dependency | Completion criterion |
|---|---|---|---|
| 1 | Confirm the test-cycle baseline and environment | The test environment and test-cycle version must be identified before execution. | Select the build of the `main` branch tagged for the test cycle and record its commit hash, as specified in Section 2. Confirm the environment and configuration decisions listed in Section 6. |
| 2 | Prepare test data and accounts | Requires the environment and baseline to be confirmed. | Test data and accounts are available for the registered test cases and SRS acceptance criteria. The dataset and database setup/reset process require team confirmation (Section 6). |
| 3 | Execute unit and integration testing | Requires the baseline, environment and test data. | Run applicable Pytest unit and integration checks across the test items in Section 2; record each test result using the status values in Section 13. |
| 4 | Execute functional, system and acceptance testing | Requires the relevant unit and integration checks and test data. | Execute the registered functional cases: TC-AUTH-01, TC-AUTH-02, TC-NOT-01, TC-REQ-01 through TC-REQ-03, TC-VEH-01, TC-FAC-01, and TC-RT-01 through TC-RT-03. Record results against their SRS requirements. Verify requirements without dedicated cases through sprint testing as identified in Section 13. |
| 5 | Execute security validation | Requires the baseline, configured authentication and HTTPS environment, and test accounts. | Execute TC-SEC-01 and TC-SEC-02 and the security validation activities in Section 5.1. Record the outcomes against the applicable security requirements. |
| 6 | Execute performance testing | Requires the performance test data and selected load-testing tool. | Execute TC-PERF-01 against the SRS workloads: route generation for 200 requests and 20 vehicles, and API response-time testing with 100 concurrent users. Record measurements against SCW-NF-001 and SCW-NF-002. |
| 7 | Retest fixes and run regression checks | Requires a failed test to be fixed; Section 13 specifies rerunning a failed case after its fix. | Rerun each affected failed test case and record its updated result. Run regression checks for affected behavior and record their results. |
| 8 | Complete test-cycle reporting and approvals | Requires the test execution and any required retesting to be complete. | Record the test metrics and results using Section 14 and complete the approvals specified in Section 15. No overall pass threshold or approval date is defined in the source documents; the team must confirm these. |

The project context sets the overall commitment as completion today and submission tomorrow; it provides no dated milestones, durations, tester availability, or per-activity deadlines. Activity dates, durations, the exact execution order beyond dependency-driven preparation and retesting after fixes, and the overall exit criteria require team confirmation.
