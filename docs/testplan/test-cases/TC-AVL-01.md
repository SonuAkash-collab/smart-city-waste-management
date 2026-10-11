# TC-AVL-01: System Availability Verification

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-AVL-01 |
| Requirement ID | SCW-NF-003 |
| Test Type | Availability |
| Priority | High |
| Status | Not run |

## Objective

Verify that the system maintains at least 99% uptime over a continuous 24-hour measurement window.

## Preconditions

- The application is deployed in the designated test environment.
- The health-check endpoint and its expected healthy response are documented.
- The monitoring mechanism is configured to execute a health check every 1 minute.
- Test-environment access and monitoring logs are available.

## Test Data and Configuration

- Measurement duration: 24 continuous hours.
- Health-check interval: 1 minute.
- Expected number of scheduled checks: 1,440.
- Minimum acceptable uptime: 99%.

## Test Steps and Expected Results

| Step | Action | Expected Result |
|---|---|---|
| 1 | Start the availability measurement and record the start time. | The monitoring window begins and the timestamp is recorded. |
| 2 | Execute a health check every minute for 24 continuous hours. | Each scheduled check records its timestamp and success or failure. |
| 3 | Record checks that return the expected healthy response as successful; record all other results as failed. | Results are recorded consistently, including endpoint errors and timeouts. |
| 4 | At the end of the window, count successful checks and total scheduled checks. | The report includes both counts and any missing observations. |
| 5 | Calculate uptime using successful checks divided by total scheduled checks, multiplied by 100. | The calculated percentage is reproducible from the recorded data. |
| 6 | Compare the calculated uptime with the 99% acceptance threshold. | Pass if uptime is at least 99%; otherwise, fail. |

## Acceptance Criteria

- Monitoring runs for a continuous 24-hour window at one-minute intervals.
- Uptime is calculated as:

  `Uptime (%) = (Successful health checks / Total scheduled health checks) × 100`

- The test passes when calculated uptime is **at least 99%**.
- For 1,440 scheduled checks, at least 1,426 must be successful to meet the threshold.
- Missing or failed checks must not be silently omitted from the calculation.

## Actual Results

- Measurement start/end:
- Total scheduled checks:
- Successful checks:
- Failed or missing checks:
- Calculated uptime:
- Evidence/log location:

## Outcome

- Status: Not run
- Defects or observations: To be recorded after execution.