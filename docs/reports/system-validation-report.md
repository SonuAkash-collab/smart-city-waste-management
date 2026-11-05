# System Validation Report

All 26 test cases of the Test Plan were run against the finished system (development frozen on 4 Nov 2026). Functional and security cases ran as automated end-to-end API tests through the running FastAPI app (CI on every pull request), plus a browser walkthrough of every page for all four roles at desktop width and 360 px. Performance cases ran with `scripts/run_perf.py` (see `perf-summary.md`).

## Summary

| Test cases | Pass | Fail | Not run yet |
|---|---|---|---|
| 26 | 24 | 0 | 2 (TC-AVL-01, TC-USE-01) |

The two cases not run yet need people or time rather than code: TC-USE-01 needs five first-time users, and TC-AVL-01 needs a 24-hour monitoring window. Their procedures and scripts are ready; results are added to the test case files when run.

## Results by test case

| TC | Requirements | Actual result | Status |
|---|---|---|---|
| TC-ADM-01 | SCW-F-003 | Driver and Operator accounts were created and logged in with 200 and the right role claim; after deactivation login returned 401 and the old token was refused. | Pass |
| TC-AUTH-01 | SCW-F-001 | All four roles got 200 and a JWT with the right role and a 30-minute lifetime; wrong password and unknown email gave the same 401 INVALID_CREDENTIALS without a token; empty email 422. | Pass |
| TC-AUTH-02 | SCW-F-002, SCW-SEC-004 | Citizen calls to route generation and request approval returned 403 FORBIDDEN and changed nothing; the Admin's call succeeded. In the browser the Citizen menu showed only My requests, Request pickup and Notifications. | Pass |
| TC-AVL-01 | SCW-NF-003 | To be filled after the 24-hour window. | Not run yet |
| TC-FAC-01 | SCW-F-031, SCW-F-032 | 1000 kg facility: 300 kg delivery left 700 kg; 800 kg delivery rejected 409 and capacity stayed 700 kg; 0 and -50 kg rejected 422; unknown vehicle and Hazardous waste rejected 422; full, wrong-type and too-small facilities were excluded from routing. | Pass |
| TC-FAC-02 | SCW-F-030 | Valid facility saved and read back; missing location, empty or unknown waste types, zero and negative capacity rejected 422; Citizen 403; Operator can read but not edit. | Pass |
| TC-MNT-01 | SCW-NF-005 | Service-layer statement coverage 97.9% (808 of 825 statements). See `docs/reports/code-coverage-report.md`. | Pass |
| TC-NOT-01 | SCW-F-050 | Submit, approve, submit, reject produced exactly 4 in-app notifications for the citizen with request id, status and time, and 4 matching emails; no other user was notified. | Pass |
| TC-PERF-01 | SCW-NF-001, SCW-NF-002 | Route generation through the API: 0.94 s, 0.89 s and 0.93 s for 200 requests and 20 vehicles. Load test: see TC-PERF-02. Details in `docs/reports/perf-summary.md`. | Pass |
| TC-PERF-02 | SCW-NF-002 | 100 users for 40 s: 1,493 requests, 0 failures, median 17 ms, 95th percentile 400 ms (target 2,000 ms). First run before the fixes: 103 requests, 28 failures, 95th percentile 31 s. | Pass |
| TC-REQ-01 | SCW-F-010, SCW-F-011 | Without photo: 201 with id, status SUBMITTED, priority HIGH, createdAt. With photo: 201, and GET returned `hasPhoto: true` and the same photo. Missing location: 422 LOCATION_REQUIRED. | Pass |
| TC-REQ-02 | SCW-F-011 | All 7 waste types got the agreed priority; Low became Medium and Medium became High after 48 h, High stayed High, both for Submitted and Approved requests; overrides to HIGH, MEDIUM and LOW were saved and returned by GET. | Pass |
| TC-REQ-03 | SCW-F-012, SCW-F-013 | GET returned each of the seven statuses; DELETE on SUBMITTED and APPROVED returned 200 with status CANCELLED; DELETE on SCHEDULED, COLLECTED, REJECTED, MISSED and CANCELLED returned 409 and the status did not change. A request was followed from SUBMITTED to COLLECTED through the real route flow. | Pass |
| TC-REQ-04 | SCW-F-014 | Each filter and the combined filter returned only matching requests with `items`, `page`, `size`, `total`; approve and reject returned 200 and GET showed the new status; Citizen PATCH returned 403 FORBIDDEN. | Pass |
| TC-RPT-01 | SCW-F-051, SCW-F-052 | Dashboard counts matched the test records; the CSV had the header and exactly one row per route stop for the date (2 pickups + 1 facility visit), with matching values; another date gave only the header. | Pass |
| TC-RT-01 | SCW-F-040, SCW-F-041 | Four approved requests and one Submitted request: the Submitted one was left out; the High request came first, then the two Medium requests nearest-next, then Low. Route saved with date and driver. | Pass |
| TC-RT-02 | SCW-F-023, SCW-F-042 | Vehicle capacity 100 kg, three 60 kg requests: planned load never above 100 kg; the route detoured to the facility after the first pickup and again at the end. Unsuitable facilities (wrong type, too little room) were skipped. | Pass |
| TC-RT-03 | SCW-F-043, SCW-F-044 | Stops listed in saved order with coordinates; marking Collected and Missed set the requests to COLLECTED and MISSED, the third request stayed SCHEDULED; other drivers got 403. Browser check: numbered pins shown on the map. | Pass |
| TC-RT-04 | SCW-F-042 | Capacity 100 kg, two 90 kg requests, facility with 10 kg left: route kept one pickup (load 90 kg), alert listed vehicle and load, Admin notification created, second request left Approved. | Pass |
| TC-SEC-01 | SCW-SEC-001, SCW-SEC-005 | Stored value is a bcrypt hash; 4 failures did not lock; the 5th locked the account for 15 minutes and the right password was refused; login worked after expiry; a good login reset the counter. | Pass |
| TC-SEC-02 | SCW-SEC-002, SCW-SEC-003, SCW-SEC-004 | Token lifetime exactly 30 minutes; expired, forged, malformed and missing tokens 401; Citizen, Driver and Operator 403 on an Admin endpoint; a token claiming ADMIN for a citizen still got 403; plain HTTP redirected to HTTPS when FORCE_HTTPS=1. | Pass |
| TC-SEC-03 | SCW-SEC-003 | Local server with a self-signed certificate: TLS 1.3 negotiated, TLS 1.1 refused; protected endpoint over HTTPS without a token returned 401; plain HTTP redirected with no data. | Pass |
| TC-SEC-04 | SCW-SEC-006 | Approve, reject, route generation and account deactivation each created a record with the Admin's id, action, affected id and time; failed calls and reads were not recorded; non-Admins got 403. | Pass |
| TC-USE-01 | SCW-NF-004 | To be filled after the sessions with five first-time users. | Not run yet |
| TC-VEH-01 | SCW-F-020, SCW-F-021 | Valid vehicle saved; duplicate registration 409; missing, zero and negative capacity 422; edits saved; Maintenance and On Route vehicles were not given routes; vehicle returned to Available after its route. | Pass |
| TC-VEH-02 | SCW-F-022 | Driver assigned and returned in vehicle details; nonexistent driver 404, non-driver or inactive user 422; same driver on a second vehicle 409; Citizen 403. | Pass |

## Defects found during validation

| ID | Found by | Defect | Fix | Status |
|---|---|---|---|---|
| D-1 | TC-PERF-02 | At 100 users the database connection pool (5 + 10) ran out; 28 of 103 requests failed after 30 s | Pool raised to 20 + 30 connections (`app/db.py`) | Fixed, re-tested: 0 failures |
| D-2 | TC-PERF-02 | 100 simultaneous logins queued behind 12-round bcrypt (about 0.25 s each); 95th percentile 31 s | 10 rounds, the OWASP minimum (`app/core/config.py`) | Fixed, re-tested: 95th percentile 400 ms |
| D-3 | Browser walkthrough | Facilities and Notifications pages crashed the app when you navigated away | Effect hooks no longer return a promise | Fixed before merge |
