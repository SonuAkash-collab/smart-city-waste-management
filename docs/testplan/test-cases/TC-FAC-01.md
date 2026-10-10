# TC-FAC-01: Facility Waste Intake and Capacity Validation

| Field | Details |
|---|---|
| TC ID | TC-FAC-01 |
| Title | Facility waste intake, remaining capacity updates and unsuitable facility exclusion |
| Requirement(s) | SCW-F-031, SCW-F-032 |
| Type | Functional |
| Priority | High |
| Preconditions | 1. The system and database are available. 2. An authorized Facility Operator account exists. 3. A registered waste collection vehicle exists. 4. A facility is registered with accepted waste types and a daily capacity. |
| Test Data | Facility: FAC-001; accepted waste type: Wet; unsupported waste type: Hazardous; initial remaining capacity: 1000 kg; valid delivery: 300 kg; excess delivery: 800 kg; invalid weights: 0 kg and -50 kg. |
| Actual Result | To be recorded during test execution. |
| Status | Not run |

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