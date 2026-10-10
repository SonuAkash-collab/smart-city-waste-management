# 4.4 Facility Management Requirements

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC  
**Date:** 10-10-2026  
**Status:** Draft

## 4.4.1 Functional Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-F-030 | The system shall allow an authorized Admin to register a facility with its location, accepted waste types, and daily processing capacity. | Functional | High | Municipal Admin | AC-SCW-F-030: A facility is created successfully when a valid location, at least one accepted waste type, and a positive daily capacity are provided. Missing location, an empty accepted waste-type list, and zero or negative capacity are rejected with a suitable validation error. Test: TC-FAC-02. | Depends on Auth & User Service and Facility Service. |
| SCW-F-031 | The system shall allow an authorized Facility Operator to record incoming waste deliveries, including the vehicle and delivered weight, and update the facility's remaining daily capacity. | Functional | High | Facility Operator | AC-SCW-F-031: A valid delivery with a positive weight not exceeding the facility's remaining daily capacity is accepted. The remaining capacity is reduced by the accepted delivery weight. Invalid weights and deliveries exceeding the remaining capacity are rejected. Concurrent deliveries shall be processed atomically so the remaining capacity cannot become negative or exceed the daily limit. Test: TC-FAC-01. | Depends on Facility Service, Vehicle Service, and PostgreSQL. |
| SCW-F-032 | The system shall exclude facilities that cannot accept a planned waste delivery because they are full, do not accept the relevant waste type, or lack sufficient remaining daily capacity. | Functional | High | Route Optimization Engine / Facility Operator | AC-SCW-F-032: Route planning uses current facility capacity and accepted waste types. A facility is excluded if it is full, does not accept the relevant waste type, or has less remaining capacity than the expected delivery weight. Only suitable facilities with sufficient capacity are eligible for disposal routing. Test: TC-FAC-01. | Depends on Facility Service and Route Optimization Engine. |

## 4.4.2 Capacity Accounting Rules

- Each facility shall have a valid location, at least one accepted waste type, and a positive daily processing capacity.
- The remaining daily capacity shall be calculated as the configured daily capacity minus the total weight of accepted deliveries for the applicable operating day.
- Each incoming delivery shall identify the vehicle and provide a positive delivered weight.
- A delivery shall be rejected if its weight exceeds the facility's current remaining daily capacity.
- Capacity validation and capacity updates shall be performed atomically to prevent concurrent deliveries from exceeding the facility's daily capacity.
- Route planning shall check the facility's current remaining capacity and accepted waste types before selecting it as a disposal destination.
- A facility shall not be selected if it is full, incompatible with the collected waste type, or unable to accommodate the expected delivery weight.
- When a new operating day begins, the facility's daily capacity accounting shall follow the configured daily-capacity reset policy.

## 4.4.3 Dependencies

- **Auth & User Service:** Authenticates administrators and facility operators and enforces role-based authorization.
- **Facility Service:** Maintains facility location, accepted waste types, daily capacity, incoming delivery records, and remaining capacity.
- **Vehicle Service:** Provides vehicle identification and relevant vehicle information for incoming deliveries.
- **Route Optimization Engine:** Uses facility eligibility and current capacity information when selecting disposal destinations.
- **PostgreSQL:** Stores facility records, delivery history, and capacity updates with appropriate transaction handling.