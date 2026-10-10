# TC-VEH-02: Driver Assignment to Vehicle

| Field | Content |
|---|---|
| TC ID | TC-VEH-02 |
| Title | Verify authorized driver assignment and assignment conflict handling |
| Requirement(s) | SCW-F-022 |
| Type | Functional / Authorization |
| Preconditions | 1. The system is available in the test environment. 2. An authorized Admin account exists. 3. Two available vehicles and two valid driver accounts exist. 4. An invalid or nonexistent driver account is available for negative testing. |
| Test data | Vehicle A: KA01AB1234; Vehicle B: KA02CD5678; Driver A: driver1@test.local; Driver B: driver2@test.local; invalid driver: nonexistent-driver; unauthorized user: a Citizen account. |
| Steps | 1. Log in as Admin. 2. Assign Driver A to Vehicle A. 3. Retrieve Vehicle A's assignment details and verify Driver A is assigned. 4. Attempt to assign a nonexistent or invalid driver to Vehicle B. 5. Attempt to assign Driver A to Vehicle B while Driver A is already assigned to Vehicle A, according to the project's one-driver-to-one-vehicle rule. 6. Log in as a Citizen and attempt to assign Driver B to Vehicle B. |
| Expected result | 1. The authorized Admin can assign a valid driver to a vehicle successfully. 2. Vehicle assignment details show the correct driver. 3. Invalid or nonexistent driver assignments are rejected with a suitable validation error. 4. Assigning one driver to two vehicles is rejected with HTTP 409 Conflict. 5. An unauthorized Citizen assignment attempt is rejected with HTTP 403 Forbidden. |
| Actual result | To be filled during testing. |
| Status | Not run |