# 4.4 Facility Management

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC  
**Date:** 10-10-2026  
**Status:** Draft

## Description

The Facility Management feature allows an Admin / Municipal Officer to register disposal facilities and configure their locations, accepted waste types, and daily processing capacities. Disposal Facility Operators record incoming waste deliveries. The system updates remaining daily capacity and excludes facilities that are full, incompatible with the waste type, or unable to accept the expected delivery from route planning.

## Functional Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-030 | The system shall allow an Admin / Municipal Officer to add a disposal facility with a valid location, one or more accepted waste types, and a positive daily processing capacity. | Functional | High | Admin / Municipal Officer | AC-SCW-F-030: A facility can be saved and retrieved when its location is valid, at least one accepted waste type is specified, and daily capacity is greater than zero. Missing or invalid mandatory fields and zero or negative capacity shall be rejected. Test: TC-FAC-02. | Depends on Auth & User Service and Database (PostgreSQL). |
| SCW-F-031 | The system shall allow a Disposal Facility Operator to record an incoming waste delivery with a valid vehicle and a positive weight, and update the facility's remaining daily capacity. | Functional | High | Disposal Facility Operator | AC-SCW-F-031: For each accepted delivery, remaining daily capacity shall equal the previous remaining capacity minus the recorded delivery weight. Zero or negative weights and deliveries exceeding remaining capacity shall be rejected. Capacity updates shall be atomic so concurrent deliveries cannot exceed the facility's daily limit. Test: TC-FAC-01. | Depends on Facility Service and Database (PostgreSQL). |
| SCW-F-032 | The system shall exclude a disposal facility from route planning when it is full, does not accept the relevant waste type, or has insufficient remaining daily capacity for the expected delivery. Eligibility shall be determined using current capacity information. | Functional | High | Route Optimization Engine / Admin | AC-SCW-F-032: Route planning excludes a facility if its remaining capacity is zero, its accepted waste types do not include the collected waste type, or its remaining capacity is less than the expected delivery weight. Eligibility is checked using the latest available facility capacity. Test: TC-FAC-01. | Depends on Facility Service and Route Optimization Engine. |

## Capacity Accounting Rules

- Remaining daily capacity shall be calculated as daily processing capacity minus the total accepted delivery weight recorded for the current operating day.
- An incoming delivery shall be accepted only if its weight is positive and does not exceed the facility's remaining daily capacity.
- Capacity updates shall be performed atomically to prevent concurrent deliveries from exceeding the daily limit.
- The system shall use the current remaining capacity and accepted waste types when determining facility eligibility for route generation.

## Dependencies

- Auth & User Service authenticates administrators and facility operators and enforces role permissions.
- Facility Service maintains facility details, accepted waste types, incoming delivery records, and remaining capacity.
- Route Optimization Engine selects suitable facilities based on waste compatibility and available capacity.
- Database (PostgreSQL) stores facility records and incoming waste transactions.