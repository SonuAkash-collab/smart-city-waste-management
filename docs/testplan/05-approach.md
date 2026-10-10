# 5. Test Approach

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04  
**Date:** 10-10-2026  
**Status:** Draft

## 5.1 Testing Strategy

The testing strategy verifies that the Smart City Waste Management System satisfies its specified functional and non-functional requirements. Testing will focus on route generation, stop ordering, vehicle capacity enforcement, driver route operations, and performance.

Tests will be designed from the requirements registry and executed using documented preconditions, test data, steps, expected results, actual results, and execution status.

## 5.2 Testing Levels

| Testing Level | Purpose | Example |
|---|---|---|
| Unit Testing | Verify individual functions and service-layer logic in isolation. | Test stop-ordering rules and vehicle-capacity calculations. |
| Integration Testing | Verify interactions between services and the database. | Verify retrieval of approved requests and persistence of generated routes. |
| System Testing | Verify end-to-end behavior across the integrated application. | Generate a route and confirm that the ordered stops are available to the driver. |
| Acceptance Testing | Verify that implemented behavior meets the documented requirements and stakeholder expectations. | Confirm route ordering, capacity handling, and driver status updates against their acceptance criteria. |

## 5.3 Testing Types

| Testing Type | Purpose |
|---|---|
| Functional Testing | Verify route generation, stop ordering, capacity handling, driver route viewing, and collection-status updates. |
| Performance Testing | Measure route-generation time and API response times under the specified workloads. |
| Regression Testing | Re-run relevant tests after changes to ensure that existing behavior remains correct. |
| Security Testing | Verify authentication and authorization behavior relevant to protected route and driver operations. |
| Usability Testing | Assess whether the relevant workflows can be completed clearly by their intended users. |

## 5.4 Test Cases and Coverage

| Test Case | Requirements Covered | Objective |
|---|---|---|
| TC-RT-01 | SCW-F-040, SCW-F-041 | Verify route generation from approved requests and ordering by priority followed by shortest distance. |
| TC-RT-02 | SCW-F-042, SCW-F-023 | Verify that vehicle capacity is never exceeded and that a full vehicle is directed to a suitable disposal facility. |
| TC-RT-03 | SCW-F-043, SCW-F-044 | Verify driver route viewing, collection outcome recording, and automatic request-status updates. |
| TC-PERF-01 | SCW-NF-001, SCW-NF-002 | Verify route-generation and API response-time targets. |

## 5.5 Test Environment and Tools

Testing should use a controlled environment with the application services, PostgreSQL database, representative test data, and access to the map integration where required.

Potential tools include:

- **Pytest:** Unit and automated service-level tests, where applicable.
- **Postman:** API request and response verification.
- **Locust or JMeter:** Load and performance testing.
- **Browser developer tools:** Inspection of frontend behavior and API communication.

The actual tools and environment used must be recorded during test execution.

## 5.6 Entry Criteria

Testing may begin when:

- The relevant functionality is available in the test environment.
- Required test data and accounts are prepared.
- The applicable requirements and test cases are documented.
- Required services and database dependencies are accessible.

## 5.7 Exit Criteria

Testing is considered complete for a test case when its steps have been executed and the actual results have been recorded.

The assigned test scope is ready for review when:

- All planned test cases have an execution status.
- Failures and deviations are documented.
- Relevant defects are recorded for follow-up.
- Performance results are compared with their specified targets.

Passing results must not be reported until supported by actual test execution.

## 5.8 Security Validation

Security validation should include the following checks where the corresponding functionality is available:

- Verify that protected endpoints reject unauthenticated requests.
- Verify that users without the required role cannot access protected administrative operations.
- Verify that input validation rejects invalid route-generation parameters.
- Verify that sensitive information is not exposed in error responses.
- Verify HTTPS and other security controls according to the project's security requirements and test plan.

## 5.9 Defect Reporting and Retesting

When actual results differ from expected results:

1. Record the test case ID and relevant requirement IDs.
2. Describe the observed behavior and expected behavior.
3. Capture reproducible steps and relevant evidence.
4. Report the issue for correction.
5. Re-run the affected test after a fix and record the new result.

## 5.10 Traceability

Test cases must retain the requirement IDs defined in the authoritative requirements registry. Any proposed changes to requirement or test case IDs must be coordinated with the project lead before updating the related documents.