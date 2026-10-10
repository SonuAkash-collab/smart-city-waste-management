
# 4.6 Open Issues and Next Steps

## 4.6.1 Purpose

This section identifies implementation and deployment decisions that require further confirmation. The issues below are not changes to the agreed requirements or architecture; they are items to resolve during implementation and testing.

## 4.6.2 Open Issues

| Issue ID | Open Issue | Impact | Proposed Next Step | Responsible Role |
|---|---|---|---|---|
| OI-01 | The deployment environment and hosting provider have not been finalized. | Deployment configuration, HTTPS setup, and availability depend on the target environment. | Select the deployment environment and document its configuration before deployment. | Team Lead / Integrator |
| OI-02 | The production database backup frequency and recovery objectives have not been defined. | Data loss or prolonged service interruption may occur after a database failure. | Define backup frequency, retention, restoration steps, and recovery targets; test restoration. | Backend / Database Team |
| OI-03 | The routing implementation's distance source has not been finalized between Haversine distance and optional OSRM road distance. | Route ordering and estimated travel distances may differ depending on the selected method. | Confirm the distance calculation approach and evaluate it against representative routes. | Route Optimization Owner |
| OI-04 | Retry behavior and failure handling for SMTP email delivery require implementation-level decisions. | Email notifications may be delayed or fail when the external provider is unavailable. | Define retry limits, failure logging, and how notification failures are surfaced. | Notification Service Owner |
| OI-05 | Operational thresholds and alert delivery for application and database monitoring have not been specified. | Failures or performance degradation may not be detected promptly. | Define monitoring thresholds, alert recipients, and incident-response steps. | Team Lead / Operations |
| OI-06 | The final deployment and verification procedure for HTTPS and TLS 1.2 or later remains to be established. | Incorrect configuration could expose traffic or prevent secure connections. | Configure HTTPS in the deployment environment and verify that insecure HTTP is not used for protected traffic. | Security Owner |
| OI-07 | The retention period and access policy for administrative audit logs have not been finalized. | Audit records may be retained too briefly or exposed to unauthorized users. | Define retention, authorized access, and protection against unauthorized modification. | Security Owner / Team Lead |

## 4.6.3 Next Steps

The team should address these issues in the following order:

1. Confirm deployment and HTTPS configuration.
2. Finalize database backup and recovery procedures.
3. Confirm the route-distance calculation approach.
4. Define email retry behavior and notification-failure handling.
5. Establish monitoring thresholds and alert procedures.
6. Define audit-log retention and access policies.
7. Verify the resulting behavior through functional, integration, security, and performance testing.

## 4.6.4 Change Management

Any decision that changes an agreed requirement, component responsibility, API convention, or architecture pattern shall be reviewed with the team lead and reflected in the relevant project documentation. Requirement IDs in the requirements registry must not be changed without notifying the team lead.
