# TC-PERF-02: API Response Time Under Concurrent Load

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-PERF-02 |
| Requirement ID | SCW-NF-002 |
| Test Type | Performance / Load Testing |
| Priority | High |
| Status | Not run |

## Objective

Verify that at least 95% of API calls complete within 2 seconds while the system is subjected to a load of 100 concurrent users, using Locust.

## Preconditions

- The application is deployed in the designated test environment.
- The backend API and required database are available.
- Locust is installed and configured.
- Representative test data and authorized test accounts are prepared.
- The API endpoints included in the workload are identified and documented.
- The test environment is not shared with production workloads.

## Test Configuration

- Load-testing tool: Locust
- Concurrent users: 100
- Response-time threshold: 2 seconds
- Required proportion of API calls within threshold: at least 95%
- Target endpoints: The agreed representative API endpoints used by the application's main workflows.

## Test Steps and Expected Results

| Step | Action | Expected Result |
|---|---|---|
| 1 | Configure Locust tasks to exercise the agreed API endpoints using representative requests and valid test data. | The workload represents the selected application workflows. |
| 2 | Configure the load test to reach 100 concurrent users. | Locust reports the configured user load and successful user startup. |
| 3 | Run the workload against the test environment and collect response-time measurements. | Response times, request counts, failures, and endpoint-level statistics are recorded. |
| 4 | Verify that the intended concurrent load was sustained during measurement. | The results identify the actual user count and any load-generation interruptions. |
| 5 | Calculate the percentage of measured API calls completed within 2 seconds. | The calculation is based on recorded response times for the agreed workload. |
| 6 | Review HTTP errors, timeouts, and failed requests alongside response times. | Failures are reported and are not hidden by the response-time summary. |
| 7 | Compare the measured percentage with the acceptance threshold. | Pass if at least 95% of measured API calls complete within 2 seconds; otherwise, fail. |

## Acceptance Criteria

- The test uses Locust and reaches 100 concurrent users.
- The selected workload and measurement period are recorded.
- At least 95% of measured API calls complete within 2 seconds.
- Failed requests and timeouts are reported separately and included in the test report.
- The report includes total requests, successful requests, failed requests, and response-time statistics.
- The test passes only when the required load is achieved and the response-time criterion is satisfied.

## Results and Calculation

- Test start/end:
- Target environment:
- Endpoints tested:
- Actual concurrent users:
- Total requests:
- Failed requests/timeouts:
- Requests completed within 2 seconds:
- Percentage completed within 2 seconds:
- Locust report/evidence location:

Calculation:

`Percentage within 2 seconds = (API calls completed within 2 seconds / Total measured API calls) × 100`

## Outcome

- Status: Not run
- Performance issues or defects: To be recorded after execution.