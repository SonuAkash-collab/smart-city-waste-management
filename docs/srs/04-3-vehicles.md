# 4.3 Vehicle Management

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04  
**Date:** 10-10-2026  
**Status:** Draft

## Description

The Vehicle Management feature allows an Admin / Municipal Officer to register and maintain waste collection vehicles, define their load capacities and supported waste types, assign drivers, and monitor vehicle availability. Only vehicles with status `Available` shall be eligible for route generation.

## Functional Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-020 | The system shall allow an Admin / Municipal Officer to add and edit a vehicle's registration number, capacity in kilograms, supported waste types, and depot location. | Functional | High | Admin / Municipal Officer | AC-SCW-F-020: A valid vehicle can be created and its saved details can be retrieved; invalid or missing mandatory fields shall be rejected. Test: TC-VEH-01 | Depends on Auth & User Service and Database (PostgreSQL). |
| SCW-F-021 | The system shall maintain each vehicle's status as `Available`, `On Route`, or `Maintenance`, and only `Available` vehicles shall be selected for route generation. | Functional | High | Admin / Municipal Officer | AC-SCW-F-021: When route generation runs, vehicles marked `On Route` or `Maintenance` are excluded from the eligible vehicle list. Test: TC-VEH-01 | Depends on Route Optimization Engine. |
| SCW-F-022 | The system shall allow an Admin / Municipal Officer to assign a registered driver to a vehicle. | Functional | Medium | Admin / Municipal Officer | AC-SCW-F-022: An authorised Admin can assign a valid driver account to a vehicle, and the saved assignment can be retrieved. Test: covered in sprint testing. | Depends on Auth & User Service. |
| SCW-F-023 | The system shall track the current collected waste load of each vehicle during a route and ensure that the load does not exceed its configured capacity. | Functional | High | Admin / Municipal Officer and Collection Vehicle Driver | AC-SCW-F-023: The recorded load shall remain less than or equal to the vehicle's configured capacity; an operation that would exceed capacity shall be prevented. Test: TC-RT-02 | Depends on Route Optimization Engine and Facility Service. |

## Dependencies

- Auth & User Service provides authentication, role checks, and driver accounts.
- Fleet Service manages vehicle information, driver assignments, status, and current load.
- Route Optimization Engine selects eligible vehicles and respects vehicle capacity.
- Database (PostgreSQL) stores vehicle records and assignments.