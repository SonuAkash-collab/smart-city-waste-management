# TC-FAC-02: Facility Registration and Validation

| Field | Content |
|---|---|
| TC ID | TC-FAC-02 |
| Title | Verify facility registration and input validation |
| Requirement(s) | SCW-F-030 |
| Type | Functional |
| Preconditions | 1. The system is available in the test environment. 2. An authorized Admin account exists. 3. The facility registration API is available. |
| Test data | Valid facility location: Facility A, Bengaluru; accepted waste types: Wet and Dry; daily capacity: 5000 kg. Invalid data: missing location, empty accepted waste types, zero capacity and negative capacity (-100 kg). |
| Steps | 1. Log in as Admin. 2. Register a facility using a valid location, at least one accepted waste type and a positive daily capacity. 3. Retrieve the facility and verify that the submitted values are stored correctly. 4. Attempt to register a facility with a missing location. 5. Attempt to register a facility with no accepted waste types. 6. Attempt to register facilities with zero and negative daily capacities. 7. Log in as a Citizen and attempt to register a facility. |
| Expected result | 1. Valid facility details are saved successfully. 2. The facility's location, accepted waste types and daily capacity match the submitted values. 3. Missing location, empty waste types and zero or negative capacity are rejected with HTTP 422 and a suitable validation error. 4. A Citizen cannot register a facility; the request is rejected with HTTP 403 Forbidden. |
| Actual result | See the execution record below. |
| Status | Pass |

## Execution record (Part 3, November 2026)

| Field | Details |
|---|---|
| Changes after the sprints | Accepted waste types use the agreed codes; JSON uses camelCase. |
| Automated tests | `test_facilities.py` (registration tests) |
| Actual result | Valid facility saved and read back; missing location, empty or unknown waste types, zero and negative capacity rejected 422; Citizen 403; Operator can read but not edit. |
| Status | Pass |
