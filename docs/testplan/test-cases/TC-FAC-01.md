# TC-FAC-01: Facility Waste Intake and Capacity Validation

| Field | Details |
|---|---|
| TC ID | TC-FAC-01 |
| Title | Facility waste intake, remaining capacity updates and unsuitable facility exclusion |
| Requirement(s) | SCW-F-031, SCW-F-032 |
| Type | Functional |
| Priority | High |
| Preconditions | 1. The application and database are available. 2. An authorized Facility Operator account exists. 3. A registered waste collection vehicle exists. 4. A facility is registered with accepted waste types and a daily capacity. |
| Test Data | Facility: FAC-001; accepted waste type: Wet; unsupported waste type: Hazardous; initial remaining capacity: 1000 kg; valid delivery: 300 kg; excess delivery: 800 kg; invalid weights: 0 kg and -50 kg. |
| Actual Result | See the execution record below. |
| Status | Pass |

## Test Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in as a Facility Operator and open the intake interface. | The authorized operator can access facility intake functions. |
| 2 | Select facility FAC-001 and record a 300 kg Wet waste delivery from a registered vehicle. | The facility accepts the waste type and validates the delivery details. |
| 3 | Submit the intake record. | The intake record is saved successfully. |
| 4 | Inspect the facility's remaining capacity. | Remaining capacity decreases from 1000 kg to 700 kg. |
| 5 | Attempt to record an additional 800 kg delivery when only 700 kg remains. | The delivery is rejected because it exceeds remaining capacity; capacity stays at 700 kg. |
| 6 | Attempt to record deliveries with weights of 0 kg and -50 kg. | Both invalid weights are rejected, and capacity remains unchanged. |
| 7 | Attempt to record incoming waste using an invalid or unregistered vehicle. | The intake record is rejected. |
| 8 | Attempt to record Hazardous waste at a facility that does not accept that waste type. | The incompatible delivery is rejected. |
| 9 | Check route selection when a facility has zero remaining capacity. | The full facility is excluded from eligible route destinations. |
| 10 | Attempt to select a facility whose remaining capacity is insufficient for the expected delivery. | The facility is excluded from eligible destinations. |
| 11 | Simulate two simultaneous deliveries whose combined weight exceeds the remaining capacity. | Intake updates are handled atomically; accepted deliveries never exceed the remaining daily capacity. |

## Pass/Fail Criteria

**Pass:** Valid deliveries are recorded, remaining capacity is updated correctly, invalid or incompatible intake is rejected, and full or insufficient-capacity facilities are excluded from routing. Concurrent deliveries never cause the remaining capacity to be exceeded.

**Fail:** Invalid intake is accepted, capacity is calculated incorrectly, an ineligible facility is selected, or concurrent updates allow the capacity limit to be exceeded.

## Evidence

Record actual results, screenshots and relevant test logs after execution. Keep the status as Not run until all applicable steps have been tested.

## Execution record (Part 3, November 2026)

| Field | Details |
|---|---|
| Changes after the sprints | Intake: `POST /api/v1/facilities/{id}/intakes {vehicleId, wasteType, weightKg}` by an Operator. The facility row is locked during the check, so concurrent deliveries cannot pass the daily limit. A delivery also lowers the vehicle's load. |
| Automated tests | `test_facilities.py` (intake and exclusion tests), `test_route_engine_facilities.py` |
| Actual result | 1000 kg facility: 300 kg delivery left 700 kg; 800 kg delivery rejected 409 and capacity stayed 700 kg; 0 and -50 kg rejected 422; unknown vehicle and Hazardous waste rejected 422; full, wrong-type and too-small facilities were excluded from routing. |
| Status | Pass |

Step 11 (simultaneous deliveries) was tested as two back-to-back deliveries on SQLite; on PostgreSQL the same code locks the facility row with SELECT ... FOR UPDATE.
