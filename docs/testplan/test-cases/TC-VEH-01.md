# TC-VEH-01: Vehicle Registration, Validation and Status

| Field | Content |
|---|---|
| TC ID | TC-VEH-01 |
| Title | Vehicle registration, editing, validation and status management |
| Requirement(s) | SCW-F-020, SCW-F-021 |
| Type | Functional |
| Preconditions | 1. The system is available in the test environment. 2. An authorized Admin account exists. 3. The vehicle management API is accessible. |
| Test data | Valid registration number: KA01AB1234; duplicate registration number: KA01AB1234; capacity: 1000 kg; invalid capacities: 0 kg and -100 kg; waste types: Wet and Dry; statuses: Available, On Route, Maintenance. |
| Steps | 1. Log in as an Admin. 2. Register a vehicle using a unique registration number, positive capacity and valid waste types. 3. Attempt to register another vehicle with the same registration number. 4. Attempt to register a vehicle with missing registration information or a zero/negative capacity. 5. Edit an existing vehicle's capacity and accepted waste types. 6. Set a vehicle to On Route and verify it is eligible for its active route only. 7. Attempt to assign the same vehicle to another active route. 8. End the route and verify the vehicle returns to Available unless it is placed in Maintenance. 9. Set a vehicle to Maintenance and verify it is excluded from route selection. |
| Expected result | 1. A valid vehicle is created successfully. 2. Duplicate registration numbers and missing or invalid required values are rejected with a suitable validation error. 3. Valid edits are saved. 4. A vehicle on an active route cannot be assigned to another active route. 5. After route completion, the vehicle returns to Available unless it is in Maintenance. 6. Vehicles in Maintenance are excluded from routing. |
| Actual result | To be filled during testing. |
| Status | Not run |