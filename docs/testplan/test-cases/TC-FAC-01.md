# TC-FAC-01: Facility Waste Intake and Capacity Validation

| Field | Content |
|---|---|
| TC ID | TC-FAC-01 |
| Title | Facility waste intake, remaining capacity updates and unsuitable facility exclusion |
| Requirement(s) | SCW-F-031, SCW-F-032 |
| Type | Functional |
| Preconditions | 1. The system is available in the test environment. 2. An authorized Facility Operator account exists. 3. A registered waste collection vehicle exists. 4. A facility is registered with accepted waste types and daily capacity. 5. The facility has 1000 kg remaining capacity for the operating day. |
| Test data | Facility: FAC-001; accepted waste type: Wet; unsupported waste type: Hazardous; remaining capacity: 1000 kg; valid incoming waste: 300 kg; excess incoming waste: 800 kg after the first delivery; invalid weights: 0 kg and -50 kg. |
| Steps | 1. Log in as a Facility Operator. 2. Record a 300 kg Wet waste delivery from a registered vehicle. 3. Check the facility's remaining capacity. 4. Attempt to record an additional 800 kg delivery. 5. Attempt to record zero or negative incoming weight. 6. Attempt to record incoming waste for an invalid vehicle. 7. Check that a facility with zero remaining capacity is excluded from route selection. 8. Check that a facility not accepting the required waste type is excluded. 9. Check that a facility with insufficient remaining capacity for the expected delivery is excluded. 10. Simulate two simultaneous deliveries whose combined weight exceeds the remaining capacity. |
| Expected result | 1. A valid 300 kg delivery is recorded successfully. 2. Remaining capacity decreases from 1000 kg to 700 kg. 3. The additional 800 kg delivery is rejected because it exceeds remaining capacity. 4. Invalid weights and invalid vehicles are rejected. 5. Full, incompatible and insufficient-capacity facilities are excluded from routing. 6. Concurrent intake updates are handled atomically so total accepted weight never exceeds the facility's remaining daily capacity. |
| Actual result | To be filled during testing. |
| Status | Not run |