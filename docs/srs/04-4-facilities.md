# 4.4 Facility Management

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04  
**Date:** 10-10-2026  
**Status:** Draft

## Description

The Facility Management feature allows an Admin / Municipal Officer to register disposal facilities and configure their locations, accepted waste types, and daily processing capacities. Disposal Facility Operators record incoming waste deliveries. The system updates the remaining facility capacity and excludes facilities that are full or do not accept the relevant waste type from route planning.

## Functional Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-030 | The system shall allow an Admin / Municipal Officer to add a disposal facility with its location, accepted waste types, and daily capacity. | Functional | High | Admin / Municipal Officer | AC-SCW-F-030: A facility with valid mandatory details can be saved and retrieved; invalid or missing mandatory fields shall be rejected. Test: covered in sprint testing. | Depends on Auth & User Service and Database (PostgreSQL). |
| SCW-F-031 | The system shall allow a Disposal Facility Operator to record incoming waste by vehicle and weight, and update the facility's remaining daily capacity. | Functional | High | Disposal Facility Operator | AC-SCW-F-031: Recording an accepted delivery reduces remaining capacity by the recorded weight; a delivery that exceeds remaining capacity is rejected. Test: TC-FAC-01. | Depends on Facility Service and Database (PostgreSQL). |
| SCW-F-032 | The system shall exclude facilities that have no remaining daily capacity or do not accept the waste type being transported. | Functional | High | Route Optimization Engine / Admin | AC-SCW-F-032: A full facility and a facility that does not accept the requested waste type are both excluded from eligible route destinations. Test: TC-FAC-01. | Depends on Facility Service and Route Optimization Engine. |

## Dependencies

- Auth & User Service authenticates administrators and facility operators and enforces role permissions.
- Facility Service maintains facility details, accepted waste types, intake records, and remaining capacity.
- Route Optimization Engine selects only suitable facilities with sufficient remaining capacity.
- Database (PostgreSQL) stores facility records and incoming waste transactions.