# 5. Non-Functional Requirements

This section defines the measurable non-functional requirements of the Smart City Waste Management System. These requirements specify the expected performance, reliability, usability, responsiveness, and maintainability of the system.

| Req ID | Requirement | Category | Priority | Acceptance Criteria / Verification |
|---|---|---|---|---|
| SCW-NF-001 | The system shall generate collection routes within 10 seconds for a workload of 200 approved collection requests and 20 vehicles. | Performance | High | Route generation completes in ≤ 10 seconds for the specified workload. Test: TC-PERF-01 |
| SCW-NF-002 | The system shall ensure that at least 95% of API responses complete within 2 seconds under a load of 100 concurrent users. | Performance | High | Under 100 concurrent users, at least 95% of measured API responses have a response time ≤ 2 seconds. Tests: TC-PERF-01, TC-PERF-02 |
| SCW-NF-003 | The system shall maintain monthly service availability of at least 99%. Availability shall be measured using a documented measurement method. Any exclusions from the availability calculation must be documented and formally agreed upon by the project stakeholders before measurement begins. | Reliability / Availability | High | Monthly availability measurements demonstrate availability ≥ 99%. Verification: availability monitoring and monthly reports. Test: TC-AVL-01 |
| SCW-NF-004 | The system shall allow a first-time citizen to submit a collection request within 3 minutes without training and shall support user-interface layouts on screens at least 360 pixels wide. | Usability / Responsiveness | Medium | Five first-time users each complete request submission within 3 minutes on desktop and at a mobile viewport width of 360 CSS pixels. Test: TC-USE-01 |
| SCW-NF-005 | The system shall use modular services and achieve at least 70% unit-test coverage of the service layer. | Maintainability / Testability | High | Service-layer statement coverage is ≥ 70%, measured using an automated coverage report. Test: TC-MNT-01 |

## Verification Notes

- **SCW-NF-001:** Measure route-generation time using 200 approved collection requests and 20 vehicles. Verify that route generation completes within 10 seconds using TC-PERF-01.
- **SCW-NF-002:** Use Locust to test 100 concurrent users and verify that at least 95% of measured API calls complete within 2 seconds using TC-PERF-02. TC-PERF-01 also verifies the route-generation performance workload.
- **SCW-NF-003:** Perform a health check every minute over a continuous 24-hour test window. Calculate uptime as successful health checks divided by total scheduled health checks, multiplied by 100. Verify uptime of at least 99% using TC-AVL-01. This test provides a 24-hour measurement; monthly availability reporting remains subject to the requirement's monthly measurement method.
- **SCW-NF-004:** Have five first-time users submit a collection request without task-specific training on desktop and a mobile viewport 360 CSS pixels wide. Each attempt must succeed within 3 minutes using TC-USE-01.
- **SCW-NF-005:** Run the backend service-layer test suite using pytest and pytest-cov. Verify statement coverage of at least 70% using TC-MNT-01.

## Traceability

The requirement IDs and acceptance criteria in this section follow `docs/requirements-registry.md`. The verification mapping is as follows: SCW-NF-001 is verified by TC-PERF-01; SCW-NF-002 is verified by TC-PERF-01 and TC-PERF-02; SCW-NF-003 is verified by TC-AVL-01; SCW-NF-004 is verified by TC-USE-01; and SCW-NF-005 is verified by TC-MNT-01.

All test cases remain Not run until they have been executed and supported by recorded evidence.