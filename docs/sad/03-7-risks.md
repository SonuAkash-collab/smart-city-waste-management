
# 3.7 Architecture Risks and Mitigations

## 3.7.1 Purpose

This section identifies risks that may affect the architecture, reliability, security, and operation of the Smart City Waste Management System. Each risk includes its potential impact and a mitigation strategy.

## 3.7.2 Risk Assessment

| Risk ID | Architecture Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-01 | OpenStreetMap or geocoding services become unavailable or return inaccurate location data. | Medium | High | Handle map-service failures gracefully, validate submitted locations, and display a clear error when location services are unavailable. |
| RISK-02 | Incorrect vehicle-load calculations cause a route to exceed vehicle capacity. | Medium | High | Validate load and capacity in the Route Optimization Engine and Fleet Service. Reject invalid load updates and verify that generated routes respect vehicle capacity. |
| RISK-03 | Concurrent waste intake operations cause facility capacity values to become inconsistent. | Medium | High | Use database transactions and atomic capacity updates in PostgreSQL. Reject intake operations that exceed the facility's remaining daily capacity. |
| RISK-04 | Unauthorized users access protected operations or another role's functions. | Medium | High | Enforce server-side role checks on every protected API endpoint. Use JWT authentication, token-expiry validation, and bcrypt password hashing. |
| RISK-05 | A large number of requests or concurrent users slows route generation and API responses. | Medium | High | Measure performance with the defined workload, optimize database queries, and test route generation against the project's performance targets. |
| RISK-06 | Database failure or loss of persistent data interrupts collection operations. | Low | High | Configure database backups, monitor database health, and document restoration procedures. Validate recovery procedures before deployment. |
| RISK-07 | Email-provider failure prevents some status-change emails from being delivered. | Medium | Medium | Keep request status available through the application, record notification failures, and retry failed email delivery where supported. |
| RISK-08 | Incorrect or incomplete request data produces unsuitable collection routes. | Medium | High | Validate request location, waste type, estimated quantity, and status before route generation. Include only approved requests and eligible vehicles and facilities. |

## 3.7.3 Risk Monitoring

The team should review these risks during implementation and testing. Mitigations should be verified through functional tests, security validation, performance tests, and integration tests as applicable.

Performance validation should use the targets in the SRS:

- Route generation completes within 10 seconds for 200 requests and 20 vehicles.
- At least 95% of API responses complete within 2 seconds with 100 concurrent users.

## 3.7.4 Dependencies

The architecture depends on PostgreSQL for persistent storage, OpenStreetMap for mapping and geocoding, and an SMTP email provider for email notifications. Failure of an external service should be handled without unnecessarily preventing unrelated application functions.
