# TC-VEH-01: Vehicle Registration, Validation and Status

| Field | Details |
|---|---|
| TC ID | TC-VEH-01 |
| Title | Vehicle registration, editing, validation and status management |
| Requirement(s) | SCW-F-020, SCW-F-021 |
| Type | Functional |
| Priority | High |
| Preconditions | 1. The system and vehicle management interface are available. 2. An authorized Admin account exists. 3. The vehicle management API is accessible. |
| Test Data | Valid registration: KA01AB1234; duplicate registration: KA01AB1234; capacity: 1000 kg; invalid capacities: 0 kg and -100 kg; waste types: Wet and Dry; statuses: Available, On Route, Maintenance; depot: Test Depot. |
| Actual Result | To be recorded during test execution. |
| Status | Not run |

## Test Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in as an Admin and open the vehicle management interface. | The authorized Admin can access vehicle management functions. |
| 2 | Register a vehicle using a unique registration number, positive capacity, supported waste types and a depot. | The vehicle passes validation and is saved successfully. |
| 3 | Attempt to register another vehicle using the same registration number. | The duplicate registration number is rejected with a suitable validation error. |
| 4 | Attempt to register vehicles with missing registration information, zero capacity or negative capacity. | Each invalid vehicle record is rejected. |
| 5 | Edit an existing vehicle's capacity and accepted waste types. | Valid changes are saved successfully. |
| 6 | Set the vehicle status to Available and generate a route for eligible collection requests. | The vehicle is eligible for route assignment when all other conditions are satisfied. |
| 7 | Set the vehicle status to On Route and attempt to assign it to another active route. | The vehicle is not assigned to a second active route. |
| 8 | Complete the active route and check the vehicle status. | The vehicle returns to Available unless it has been placed in Maintenance. |
| 9 | Set the vehicle status to Maintenance and generate a route using eligible collection requests. | The Maintenance vehicle is excluded from route assignment. |
| 10 | Inspect the generated route assignments. | No route is assigned to the Maintenance vehicle. |

## Pass/Fail Criteria

**Pass:** Valid vehicle details are saved; duplicate registration numbers and invalid required values are rejected; valid edits are saved; a vehicle cannot be assigned to multiple active routes; and Maintenance vehicles are excluded from route assignment.

**Fail:** Invalid vehicle details are accepted, valid changes are not saved, a vehicle is assigned to multiple active routes, or a Maintenance vehicle is selected for routing.

## Evidence

Record actual results, screenshots and relevant test logs after execution. Keep the status as Not run until all applicable steps have been tested.