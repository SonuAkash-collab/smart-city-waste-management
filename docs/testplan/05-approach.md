# Test Approach

## 1. Testing Strategy

Testing will verify that the Smart City Waste Management System satisfies its functional requirements, non-functional requirements, security requirements, and documented error-handling behavior.

The testing strategy combines:

- **Unit testing:** Validate individual service functions and business rules.
- **Integration testing:** Verify interactions between the FastAPI backend, PostgreSQL database, and connected services.
- **Functional testing:** Validate request processing, route generation, vehicle capacity, facility selection, driver workflows, and reporting.
- **Security testing:** Verify authentication, role-based authorization, password handling, token expiration, HTTPS, and audit logging.
- **Performance testing:** Measure route-generation time and API response times under the specified workloads.
- **Usability testing:** Measure how quickly first-time users can submit a request on mobile and desktop screens.
- **Availability testing:** Monitor health-check results over a continuous 24-hour test window.

## 2. Test Environment

- **Frontend:** React application, tested in a desktop browser and at a mobile viewport width of 360 CSS pixels.
- **Backend:** FastAPI application running in a test environment.
- **Database:** PostgreSQL test database containing controlled test data.
- **Unit testing and coverage:** Pytest and pytest-cov.
- **Load testing:** Locust.
- **API validation:** FastAPI endpoints tested using automated requests or an API client.
- **Route and map testing:** Use controlled request, vehicle, facility, capacity, and location data. Verify route decisions independently of external map-service availability wherever possible.

Tests must use test data and must not modify production records.

## 3. Functional Test Approach

Functional tests will verify the following behaviors:

1. Request submission, validation, and status changes.
2. Route generation from approved requests.
3. Stop ordering by priority and then nearest-next distance.
4. Vehicle capacity enforcement and diversion to a suitable facility.
5. Driver access to assigned routes and the ability to mark stops as Collected or Missed.
6. Facility and vehicle registration, validation, and status handling.
7. Dashboard counts and daily collection CSV exports.
8. Correct handling of invalid input, unauthorized access, unavailable facilities, and other documented error conditions.

Expected results must be derived from the requirements registry and the corresponding test case. A test must not introduce a new business rule that has not been approved and documented.

## 4. Non-Functional Test Approach

### 4.1 Route-generation performance

Use a controlled dataset containing 200 approved requests and 20 vehicles. Measure route-generation duration from the request to generate routes until a successful result is returned. The target is **10 seconds or less**.

### 4.2 API performance

Use Locust to simulate **100 concurrent users**. Record API response times and calculate the percentage of measured API calls completed within 2 seconds. The acceptance criterion is **at least 95%**.

### 4.3 Availability

Perform a health check every **1 minute for a continuous 24-hour window**. Calculate uptime as:

`successful health checks / total scheduled health checks × 100`

The acceptance criterion is **at least 99% uptime** during the measurement window. A health check is successful only when the configured health endpoint returns the expected healthy response. Record failed checks and investigate their causes.

### 4.4 Usability

Recruit **five first-time users** who have not received task-specific training. Each participant must submit a request on both a desktop layout and a mobile layout with a viewport width of **360 CSS pixels**. Measure elapsed time from the start of the task to successful submission. Each participant must complete each attempt in **3 minutes or less**.

Record completion time, success or failure, and any usability issue. Do not count a failed submission as a successful result.

### 4.5 Maintainability and code coverage

Run `pytest --cov` against the backend service layer using the project's configured test suite and coverage source. The service layer must achieve **at least 70% statement coverage**. Record the command, test result, and coverage report. Coverage alone does not prove that all requirements are correctly implemented.

## 5. Security Test Approach

Security tests will verify:

- Passwords are stored as bcrypt hashes rather than plaintext.
- Accounts are locked for 15 minutes after five consecutive failed login attempts.
- JWT access tokens expire after 30 minutes.
- Protected endpoints reject missing, invalid, malformed, or expired tokens.
- Server-side role checks prevent unauthorized access.
- HTTPS uses TLS 1.2 or later.
- Required administrative actions are recorded in audit logs.

Security tests must be performed in the test environment using test accounts. Results must be recorded against the corresponding security requirements and test cases.

## 6. Test Data and Execution

Prepare controlled test records for citizens, requests, vehicles, drivers, facilities, capacities, route assignments, and collections.

For repeatable tests:

1. Record the preconditions and required test data.
2. Execute the documented steps.
3. Compare actual results with expected results.
4. Capture relevant API responses, logs, timing measurements, or reports.
5. Record the result as **Pass**, **Fail**, or **Blocked** after execution. Before execution, retain the status **Not run**.
6. Record defects with reproduction steps, expected behavior, actual behavior, and supporting evidence.

Performance and availability results must include the measurement window, workload, total observations, failures, and calculated acceptance metric.

## 7. Entry and Exit Criteria

### Entry criteria

- The relevant application build is available in the test environment.
- Required configuration and test data are prepared.
- Dependencies needed for the test are accessible.
- Test cases and expected results are documented.
- The test environment is separated from production.

### Exit criteria

- All planned test cases have an explicitly recorded status.
- Failed and blocked tests have documented explanations and associated defects where applicable.
- Required functional and non-functional acceptance criteria have been evaluated.
- Performance, availability, usability, and coverage evidence has been recorded for the relevant tests.
- Outstanding defects and limitations are reported to the project team.

A test plan or test case must not be reported as passed solely because it has been documented. Acceptance is based on recorded execution evidence.

## 8. Traceability and Reporting

Map every test case to its corresponding requirement ID in `docs/requirements-registry.md`. Keep the features-to-test mapping and requirement verification references synchronized with the actual test cases.

Any new or changed requirement, acceptance threshold, or business rule must be reviewed with the project lead and reflected in the authoritative requirements registry before the traceability mapping is treated as final.

Test reports will summarize test coverage, execution status, failures, defects, measured results, and any unmet acceptance criteria.