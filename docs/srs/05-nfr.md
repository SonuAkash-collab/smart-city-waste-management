# 5. Non-Functional Requirements

This section defines the measurable non-functional requirements of the Smart City Waste Management System. These requirements specify the expected performance, reliability, usability, responsiveness, and maintainability of the system.

| Req ID | Requirement | Category | Priority | Acceptance criteria / Verification |
|---|---|---|---|---|
| SCW-NF-001 | The system shall generate collection routes within 10 seconds for a workload of 200 approved collection requests and 20 vehicles. | Performance | High | Route generation completes in ≤ 10 seconds for the specified workload. Test: TC-PERF-01 |
| SCW-NF-002 | The system shall ensure that at least 95% of API responses complete within 2 seconds under a load of 100 concurrent users. | Performance | High | Under 100 concurrent users, at least 95% of measured API responses have a response time ≤ 2 seconds. Test: TC-PERF-01 |
| SCW-NF-003 | The system shall maintain monthly service availability of at least 99%, excluding no periods unless an exclusion policy is formally agreed upon. | Reliability / Availability | High | Monthly availability measurements demonstrate availability ≥ 99%. Verification: availability monitoring and monthly reports. Test: covered in sprint testing |
| SCW-NF-004 | The system shall allow a first-time citizen to submit a collection request within 3 minutes without training and shall support user-interface layouts on screens at least 360 pixels wide. | Usability / Responsiveness | Medium | A first-time citizen completes request submission within 3 minutes without training, and the interface remains usable at a viewport width of 360 pixels. Test: covered in sprint testing |
| SCW-NF-005 | The system shall use modular services and achieve at least 70% unit-test coverage of the service layer. | Maintainability / Testability | High | Service-layer unit-test coverage is ≥ 70%, measured using a coverage report. Verification: automated unit tests and coverage report. Test: covered in sprint testing |

## Verification Notes

- Performance measurements shall use the workload and concurrency specified in the relevant requirement.
- Availability shall be calculated from recorded service uptime and downtime over a calendar month.
- Usability testing shall measure the time taken by a first-time citizen to complete a collection request without training.
- Responsive-interface testing shall include a viewport width of 360 pixels.
- Service-layer test coverage shall be measured using an automated code-coverage tool.

## Traceability

The requirement IDs and targets in this section follow `docs/requirements-registry.md`. SCW-NF-001 and SCW-NF-002 are covered by TC-PERF-01. Verification of the remaining requirements shall be included in sprint testing and the final test plan.