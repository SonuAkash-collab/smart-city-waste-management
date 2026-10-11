# TC-RT-04: Route Handling When No Facility Has Sufficient Capacity

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-RT-04 |
| Requirement ID | SCW-F-042 |
| Test Type | Functional / Route Generation Edge Case |
| Priority | High |
| Status | Not run |

## Objective

Verify that when no suitable facility has sufficient capacity to accept the vehicle's load, route generation prevents the vehicle from exceeding its capacity and alerts the administrator.

## Preconditions

- The application and test database are available.
- An administrator can generate routes and view alerts.
- A vehicle with a configured maximum capacity is available for testing.
- At least one approved collection request is assigned to the route.
- All candidate facilities are configured so that none can accept the vehicle's remaining load.
- The vehicle's current load, maximum capacity, and each facility's remaining capacity are known.

## Test Data

Prepare a controlled scenario in which:

- The vehicle has a defined maximum capacity and current load.
- A pending collection would bring the vehicle to its capacity limit or beyond it.
- Every candidate facility is either unsuitable or has insufficient remaining capacity to accept the required load.
- The expected route behavior and administrator alert can be observed.

Record the exact vehicle load, capacity, request quantity, and facility capacities before execution.

## Test Steps and Expected Results

| Step | Action | Expected Result |
|---|---|---|
| 1 | Configure the vehicle and candidate facilities with the test capacities. | The vehicle and facility capacity values match the prepared test data. |
| 2 | Attempt to generate a route that would require a facility detour, while ensuring no facility can accept the required load. | The system detects that no suitable facility is available. |
| 3 | Inspect the generated or updated route. | The route stops before the vehicle would exceed its configured capacity; no further collection is assigned if it would cause an overflow. |
| 4 | Inspect the vehicle load and route state. | The recorded or planned load does not exceed the vehicle's maximum capacity. |
| 5 | Check the administrator's alert or notification view. | An alert identifies that no suitable facility has sufficient capacity and that route progress requires attention. |
| 6 | Review application logs or the relevant API response. | The unavailable-facility condition is handled explicitly and is not silently treated as a successful facility detour. |

## Acceptance Criteria

- The system identifies that no suitable facility has sufficient remaining capacity.
- The route does not plan or execute a collection that would cause the vehicle to exceed its maximum capacity.
- The route stops or is safely suspended before an overflow would occur.
- An administrator alert is generated and can be observed.
- The outcome is recorded clearly so the administrator can take corrective action.
- The test passes only when all applicable criteria are satisfied.

## Actual Results

- Vehicle maximum capacity:
- Initial vehicle load:
- Request quantity:
- Candidate facility capacities:
- Route outcome:
- Administrator alert observed:
- Evidence location:

## Outcome

- Status: Not run
- Defects or observations: To be recorded after execution.