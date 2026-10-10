# 4.3 Vehicle Management

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC  
**Date:** 10-10-2026  
**Status:** Draft

## Description

The Vehicle Management feature allows an Admin / Municipal Officer to register and maintain waste collection vehicles, define their load capacities and supported waste types, assign drivers, and monitor vehicle availability. Only vehicles with status `Available` shall be eligible for route generation. A vehicle assigned to an active route shall not be assigned to another active route.

## Functional Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-020 | The system shall allow an Admin / Municipal Officer to add and edit a vehicle's registration number, capacity in kilograms, supported waste types, and depot location. Registration numbers shall be unique and non-empty, and vehicle capacity shall be a positive number. | Functional | High | Admin / Municipal Officer | AC-SCW-F-020: A vehicle with a unique, non-empty registration number and capacity greater than zero can be saved and retrieved. Duplicate registration numbers, missing mandatory fields, and zero or negative capacities shall be rejected. Test: TC-VEH-01. | Depends on Auth & User Service and Database (PostgreSQL). |
| SCW-F-021 | The system shall maintain each vehicle's status as `Available`, `On Route`, or `Maintenance`. Newly registered vehicles shall be `Available` by default. Assigning a vehicle to an active route changes its status to `On Route`; when the active route ends, its status returns to `Available` unless it is placed in `Maintenance`. Only `Available` vehicles shall be eligible for route generation. | Functional | High | Admin / Municipal Officer | AC-SCW-F-021: Vehicles marked `On Route` or `Maintenance` are excluded from route generation. A vehicle assigned to an active route cannot be assigned to another active route. On route completion, the vehicle becomes `Available` unless its status is `Maintenance`. Test: TC-VEH-01. | Depends on Fleet Service and Route Optimization Engine. |
| SCW-F-022 | The system shall allow an authorized Admin / Municipal Officer to assign a registered, valid driver account to a vehicle. | Functional | Medium | Admin / Municipal Officer | AC-SCW-F-022: An authorized administrator can assign a valid driver account, and the saved assignment can be retrieved. Invalid or nonexistent driver accounts shall be rejected, and unauthorized assignment attempts shall return HTTP 403. Test: TC-VEH-02 (proposed; requires agreement and addition to the Test Plan). | Depends on Auth & User Service and Fleet Service. |
| SCW-F-023 | The system shall track the collected waste load of each vehicle during a route by recording collection weights and updating the current load. The system shall prevent the load from exceeding the configured vehicle capacity and direct a full vehicle to the nearest suitable disposal facility that accepts the waste type and has sufficient remaining capacity. | Functional | High | Admin / Municipal Officer and Collection Vehicle Driver | AC-SCW-F-023: Each recorded collection weight updates the vehicle's current load. The load shall never exceed vehicle capacity. When the vehicle reaches capacity, route handling shall direct it to the nearest eligible disposal facility before further collection. Test: TC-RT-02. | Depends on Fleet Service, Route Optimization Engine, and Facility Service. |

## Dependencies

- Auth & User Service provides authentication, role checks, and driver accounts.
- Fleet Service manages vehicle information, driver assignments, status, and current load.
- Route Optimization Engine selects eligible vehicles, respects vehicle capacity, and directs full vehicles to suitable disposal facilities.
- Facility Service provides accepted waste types and current remaining facility capacity.
- Database (PostgreSQL) stores vehicle records, assignments, status, and load information.