# TC-AVL-01: System Availability Verification

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-AVL-01 |
| Requirement ID | SCW-NF-003 |
| Test Type | Availability |
| Priority | High |
| Status | Not run yet |

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

Measurement start/end (UTC):

Start: 2026-11-16 16:16:48 UTC

End (last recorded check): 2026-11-17 04:15:51 UTC

Measurement duration: Approximately 12 hours (12-hour window instead of 24; see deviation 17).

Total scheduled checks: 720

Successful checks: 720

Failed or missing checks: 0

Calculated uptime: (720 / 720) × 100 = 100.00%

Evidence/log location: backend/availability-log.csv

Result: PASS — exceeded the required 99% uptime threshold.
## Outcome

- Status: PASS
- Defects or observations: No failed health checks were observed. The 12-hour measurement window was used instead of the specified 24-hour window (see deviation 17).
## Execution record (Part 3, November 2026)

| Field | Details |
|---|---|
| Changes after the sprints | `backend/scripts/availability_monitor.py` checks `/health` every minute and writes `availability-log.csv`. |
| Automated tests | `test_health.py` (health endpoint) |
| Actual result |  720/720 successful checks; 100.00% uptime over approximately 12 hours. |
| Status | PASS (12-hour window instead of 24; see deviation 17). |

How to run: start the app, then `python scripts/availability_monitor.py --url http://localhost:8000 --hours 24` on a computer that will not sleep. Record checks run, successes and uptime here.
