## 14. Test Metrics & Reporting

### 14.1 Test Metrics

| Metric | Definition | Target |
|---|---|---|
| Test execution rate | Test cases executed ÷ total planned test cases × 100 | 100% of the 14 test cases executed in each test cycle |
| Pass rate | Test cases passed ÷ test cases executed × 100 | 100% for High-priority requirements; ≥ 90% overall before release |
| Requirements coverage | Requirement IDs with at least one passed test case or verified sprint test ÷ total requirement IDs × 100 | 100% (all 34 FR, NFR and SEC IDs) |
| Defect count by severity | Open defects grouped as Critical, Major, Minor | 0 Critical and 0 Major open at release |
| Defect density | Defects found ÷ number of components under test | Reported per cycle; no fixed target |
| Defect fix turnaround | Average time from a defect being logged to its fix being verified | ≤ 2 working days for Critical and Major defects |
| Defect reopen rate | Defects reopened after fix ÷ defects fixed × 100 | ≤ 10% |
| Unit-test coverage | Lines of service-layer code executed by unit tests ÷ total service-layer lines × 100 (measured with `pytest-cov`) | ≥ 70% (SCW-NF-005) |
| Performance results | Route generation time for 200 requests / 20 vehicles; 95th-percentile API response time at 100 concurrent users | ≤ 10 s (SCW-NF-001); ≤ 2 s (SCW-NF-002) |

**Defect severity definitions:**

| Severity | Definition | Example |
|---|---|---|
| Critical | Security breach, data loss, or a core function unusable with no workaround | Citizen can call an Admin endpoint; route exceeds vehicle capacity |
| Major | A requirement not met, with a workaround available | Notification email not sent, but in-app notification shown |
| Minor | Cosmetic or low-impact issue | Misaligned label on the dashboard |

### 14.2 Reporting

| Report | Content | Frequency | Prepared by | Audience |
|---|---|---|---|---|
| Test cycle report | Commit hash under test, test cases run, pass/fail/blocked counts, new defects by severity | End of each test cycle | Test case owners; compiled by Sonu Akash | Team 04 |
| Defect report | GitHub Issue per defect: TC ID, requirement ID, steps to reproduce, expected vs actual result, severity, screenshot or log | When a defect is found | Tester who found it | Developer responsible for the component |
| Traceability status | Section 13 matrix with the latest status of each requirement | End of each test cycle | Sonu Akash | Team 04, course instructor |
| Performance report | Locust/JMeter results for TC-PERF-01: response-time percentiles, throughput, error rate | Each performance test run | Rottela Haritej | Team 04 |
| Test summary report | Final metrics against the targets in Section 14.1, open defects, and a release recommendation | End of testing | Sonu Akash | Team 04, course instructor |

Test results (Actual result and Status) are recorded in each test case file in `docs/testplan/test-cases/`. Defects are tracked as GitHub Issues in the project repository, labelled `bug` and the severity (`critical`, `major`, `minor`).
