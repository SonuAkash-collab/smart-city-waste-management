### TC-REQ-01: Submit a collection request

| Field | Content |
|---|---|
| TC ID | TC-REQ-01 |
| Title | Submit a valid collection request with and without an optional photo; reject a request with missing location |
| Requirement(s) | SCW-F-010 |
| Type | Functional |
| Objective | Verify that a Citizen can submit a collection request with the required location, waste type and estimated quantity, that the photo is optional, and that a missing location is rejected. |
| Preconditions | 1. The Request Service is reachable in the test environment using the configured REST/JSON API under `/api/v1`. 2. An authenticated Citizen request context is available for the Citizen's own requests. Working assumption: the test environment supplies its configured API base URL and a Citizen identity with a bearer token, as described in the Test Environment; this case does not prescribe a URL, credential, or provisioning method. |
| Test data | Valid request without photo: `{"latitude":12.97,"longitude":77.59,"address":"...","wasteType":"HAZARDOUS","estimatedQuantityKg":25}`. Valid request with photo: same fields plus `"photo":"<base64-encoded photo fixture>"`. Working assumption: use a syntactically valid base64-encoded photo fixture; this case asserts no undocumented image-format or size limits. Missing-location request: omit `latitude`, `longitude`, and `address` from an otherwise valid request. |
| Steps | 1. Using the authenticated Citizen request context, send `POST /api/v1/requests` with the valid request without a photo. 2. Send the same endpoint with the base64-encoded photo fixture included. 3. Use the documented `GET /api/v1/requests/{id}` endpoint as the request owner to retrieve the request submitted in step 2. 4. Send the POST endpoint with the missing-location request. Record the HTTP status and response body for each request. |
| Expected result | Steps 1 and 2: HTTP 201. Each response contains `id`, `status`, `priority`, and `createdAt`; the API example is `{"id":101,"status":"SUBMITTED","priority":"HIGH","createdAt":"2026-10-10T10:00:00Z"}`. `HAZARDOUS` is assigned `HIGH` under SCW-F-011. The photo submission is accepted and its photo is associated with the stored request as required by SCW-F-010. Step 3: HTTP 200 with the full request object, through which the saved request and photo association can be checked. Working assumption: use the returned full request as the observation point; no photo-specific response property or representation is prescribed. Step 4: HTTP 422 with the common API error body and code `LOCATION_REQUIRED`; the missing-location request is rejected. |
| Pass/fail criteria | Pass if both valid submissions return HTTP 201 with the documented response fields and applicable values, the owner GET returns HTTP 200 and provides evidence that the submitted photo is associated with the saved request, and the missing-location submission returns HTTP 422 with error code `LOCATION_REQUIRED`. Fail if any of these outcomes does not occur. Working assumption: evaluate photo association from the full request returned by the documented GET endpoint without requiring an undocumented property name or representation. |
| Actual result | |
| Status | Not run |

The `id` and `createdAt` shown in the response example are example values, not fixed values for each test execution. The API contract also lists HTTP 401 for POST; authentication-failure behavior is outside the registered TC-REQ-01 scope.
