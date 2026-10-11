# 4.5 Route Generation

**Description:** The system shall generate collection routes for a selected date using approved waste collection requests, available vehicles, vehicle capacity, request priority, geographic distance, and suitable disposal facilities. Routes shall be assigned to vehicles and displayed to their drivers as ordered stops on a map.

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance criteria / Test case ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-040 | The system shall allow an authorized administrator to generate collection routes for a selected date using all approved collection requests for that date. | Functional | High | Admin / Municipal Officer | AC-SCW-F-040: For a selected date, every eligible approved request is considered for route generation, and the generated routes are saved successfully. Test: TC-RT-01 | Depends on Request Service, Fleet Service, Facility Service, and Route Optimization Engine. |
| SCW-F-041 | The system shall order collection stops by request priority first and shortest geographic distance second. | Functional | High | Admin / Municipal Officer | AC-SCW-F-041: Higher-priority requests are scheduled before lower-priority requests; among requests of equal priority, the nearer eligible stop is selected first. Test: TC-RT-01 | Uses the agreed greedy heuristic and geographic distance calculations. |
| SCW-F-042 | The system shall ensure that a collection vehicle's load never exceeds its configured capacity and shall direct a full vehicle to the nearest suitable disposal facility that accepts the collected waste type and has sufficient remaining capacity. | Functional | High | Fleet Service / Facility Operator | AC-SCW-F-042: At every collection stop, the vehicle load is less than or equal to its configured capacity. When the vehicle cannot accept additional waste, the route includes the nearest eligible disposal facility. Test: TC-RT-02 | Depends on vehicle capacity, current load, waste type, facility acceptance rules, and remaining facility capacity. |
| SCW-F-043 | The system shall allow an authenticated driver to view the driver's assigned collection route as ordered stops on a map. | Functional | High | Collection Vehicle Driver | AC-SCW-F-043: The assigned route displays all assigned stops in their saved order, with each stop's location identifiable on the map. Test: TC-RT-03 | Depends on Route Service and Map Service (OpenStreetMap). |
| SCW-F-044 | The system shall allow an authenticated driver to mark each assigned collection stop as COLLECTED or MISSED and shall update the associated collection request status automatically. | Functional | High | Collection Vehicle Driver | AC-SCW-F-044: When a driver marks a stop as COLLECTED or MISSED, the corresponding request status changes to Collected or Missed respectively, and the updated status is available when the request is retrieved. Test: TC-RT-03 | Depends on Route Service and Request Service. Only authorized drivers may update their assigned stops. |

## Dependencies and Constraints

- Only approved collection requests for the selected date are eligible for route generation.
- Only available vehicles are eligible for route assignment.
- Route generation shall follow the priority-first, nearest-next-stop greedy heuristic agreed upon by the team.
- Vehicle capacity and disposal-facility compatibility and remaining capacity shall be checked during route generation.
- Drivers shall only access their assigned routes and update their assigned stops.
- Requirement IDs and test case references shall remain consistent with `docs/requirements-registry.md`.
## Worked Example: Route Generation

### Scenario

An administrator generates a collection route for one vehicle using three approved collection requests and one suitable facility.

**Vehicle and facility details**

| Item | Details |
|---|---|
| Vehicle | V1 |
| Vehicle maximum capacity | 1,000 kg |
| Initial vehicle load | 0 kg |
| Facility | F1 |
| Facility remaining capacity | 2,000 kg |

**Collection requests**

| Request | Priority | Location | Waste quantity |
|---|---|---|---:|
| R1 | High | Location A | 300 kg |
| R2 | Medium | Location B | 250 kg |
| R3 | Low | Location C | 200 kg |

The example assumes that all three requests are approved, eligible for assignment to V1, and can be collected without exceeding the vehicle's capacity.

### Route-generation steps

1. The system retrieves the three approved requests and sorts them by priority: R1, R2, then R3.
2. The system assigns R1 first. The vehicle load becomes 300 kg.
3. The system assigns R2 next. The vehicle load becomes 550 kg.
4. The system assigns R3 next. The vehicle load becomes 750 kg.
5. The system checks the resulting load against the vehicle's 1,000 kg maximum capacity. Since 750 kg is within capacity, no facility detour is required for capacity reasons.

### Expected result

The resulting collection order is R1 → R2 → R3, subject to the documented priority and distance-ordering rules. The vehicle's planned load is 750 kg, leaving 250 kg of unused capacity.

This example illustrates basic priority ordering and capacity validation. If requests have equal priority, nearest-next distance determines their order. If the vehicle needs a facility detour, the system must select the nearest suitable facility with sufficient remaining capacity. If no suitable facility is available, route planning must stop before the vehicle exceeds its capacity and the administrator must be alerted.