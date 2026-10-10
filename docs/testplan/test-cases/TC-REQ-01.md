### TC-REQ-01: Submit a collection request

| Field | Content |
|---|---|
| TC ID | TC-REQ-01 |
| Title | Submit a valid collection request with and without an optional photo; reject a request with missing location |
| Requirement(s) | SCW-F-010 |
| Type | Functional |
| Objective | Verify that a Citizen can submit a collection request with the required location, waste type and estimated quantity, that the photo is optional, and that a missing location is rejected. |
| Preconditions | 1. The Request Service is reachable in the test environment using the configured REST/JSON API under `/api/v1`. 2. An authenticated Citizen request context is available for the Citizen's own requests. The environment-specific API base URL and the approved method of provisioning a test Citizen identity and bearer token require team confirmation. |
| Test data | Valid request without photo: `{"latitude":12.97,"longitude":77.59,"address":"...","wasteType":"HAZARDOUS","estimatedQuantityKg":25}`. Valid request with photo: same fields plus `"photo":"<base64, optional>"`, replaced during execution by a valid base64-encoded photo fixture. Missing-location request: omit `latitude`, `longitude`, and `address` from an otherwise valid request. The photo fixture's format and size limits are not specified and require confirmation. |
| Steps | 1. Using the authenticated Citizen request context, send `POST /api/v1/requests` with the valid request without a photo. 2. Send the same endpoint with a valid base64-encoded photo included. 3. Send the endpoint with the missing-location request. Record the HTTP status and response body for each request. |
| Expected result | Steps 1 and 2: HTTP 201. Each response contains `id`, `status`, `priority`, and `createdAt`; the documented example is `{"id":101,"status":"SUBMITTED","priority":"HIGH","createdAt":"2026-10-10T10:00:00Z"}`. `HAZARDOUS` is assigned `HIGH` under SCW-F-011. The request with a photo is accepted, and the supplied photo is associated with the stored request as specified by SCW-F-010. Step 3: HTTP 422 with `{"error":{"code":"LOCATION_REQUIRED","message":"..."}}`. The missing-location request is rejected. |
| Pass/fail criteria | Pass if both valid submissions return HTTP 201 with the documented response fields and values applicable to the supplied test data, the missing-location submission returns HTTP 422 with error code `LOCATION_REQUIRED`, and the supplied photo is verified as associated with the stored request using a team-confirmed method. Fail if any verified requirement outcome does not occur. Until the team confirms how photo association can be observed, that part of the test cannot be evaluated. |
| Actual result | |
| Status | Not run |

The `id` and `createdAt` shown in the response example are example values; the source documents do not define fixed values for each test execution. The API contract lists HTTP 401 as another POST error, but authentication-failure behavior is outside the registered TC-REQ-01 scope.
