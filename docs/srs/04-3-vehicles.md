# 4.3 Vehicle Management Requirements

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC  
**Date:** 10-10-2026  
**Status:** Draft

## 4.3.1 Functional Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-020 | The system shall allow an authorized Admin to add and edit vehicles with a registration number, capacity in kilograms, accepted waste types, and depot location. Registration numbers shall be unique, and capacity shall be positive. | Functional | High | Municipal Admin | AC-SCW-F-020: A vehicle with a unique, non-empty registration number and positive capacity is created successfully. Duplicate registration numbers, missing required fields, and zero or negative capacity are rejected with a suitable validation error. Valid vehicle details can be edited and saved. Test: TC-VEH-01. | Depends on Auth & User Service and Vehicle Service. |
| SCW-F-021 | The system shall maintain each vehicle's status as `Available`, `On Route`, or `Maintenance`. Only `Available` vehicles shall be eligible for route assignment. | Functional | High | Municipal Admin / Route Optimization Engine | AC-SCW-F-021: A newly registered vehicle is `Available`. Assigning a vehicle to an active route changes its status to `On Route`. A vehicle assigned to an active route cannot be assigned to another active route. When the route ends, the vehicle returns to `Available` unless it is placed in `Maintenance`. Vehicles in `Maintenance` are excluded from routing. Test: TC-VEH-01. | Depends on Vehicle Service and Route Optimization Engine. |
| SCW-F-022 | The system shall allow an authorized Admin to assign a valid driver account to a registered vehicle. A driver shall not be assigned to two vehicles simultaneously. | Functional | High | Municipal Admin | AC-SCW-F-022: An authorized Admin can assign a valid driver to a vehicle. Invalid or nonexistent driver accounts are rejected. An unauthorized assignment attempt is rejected with HTTP 403, and assigning a driver who is already assigned to another vehicle is rejected with HTTP 409. Test: TC-VEH-02. | Depends on Auth & User Service and Vehicle Service. |
| SCW-F-023 | The system shall track the current collected waste load of each vehicle during a route and compare it with the vehicle's capacity. | Functional | High | Driver / Route Optimization Engine | AC-SCW-F-023: The system records the weight collected at each stop and updates the vehicle's current load. The current load shall never exceed the vehicle's capacity. When the vehicle reaches capacity, the system directs it to the nearest suitable disposal facility that accepts the collected waste type and has sufficient remaining capacity, consistent with SCW-F-042. After disposal is recorded, the vehicle's current load is updated before collection continues. Test: TC-RT-02. | Depends on Route Optimization Engine, Vehicle Service, and Facility Service. |

## 4.3.2 Vehicle Status and Capacity Rules

- A vehicle must have a unique registration number and a positive capacity before it can be registered.
- Only vehicles with `Available` status are eligible for a new route assignment.
- A vehicle on an active route must have `On Route` status and cannot be assigned to another active route.
- A vehicle in `Maintenance` status is not eligible for route assignment.
- Collected waste weights must be recorded and added to the vehicle's current load.
- The current load must never exceed the vehicle's configured capacity.
- When the vehicle reaches capacity, route handling shall direct it to a suitable disposal facility in accordance with SCW-F-042.
- After waste disposal is recorded, the vehicle's current load must be updated before further collection proceeds.

## 4.3.3 Dependencies

- **Auth & User Service:** Authenticates administrators and validates authorization for vehicle and driver assignment operations.
- **Vehicle Service:** Stores vehicle registration details, capacity, accepted waste types, depot location, assigned driver, status, and current load.
- **Route Optimization Engine:** Assigns eligible vehicles, prevents conflicting active-route assignments, and handles capacity-related facility detours.
- **Facility Service:** Supplies facility waste-type compatibility and current remaining-capacity information for disposal decisions.
- **PostgreSQL:** Persists vehicle records, driver assignments, status changes, and current load information.