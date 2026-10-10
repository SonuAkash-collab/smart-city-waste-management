
# 11. Test Assumptions and Dependencies

## 11.1 Purpose

This section documents the assumptions and dependencies used when planning and executing tests for the Smart City Waste Management System.

## 11.2 Test Assumptions

| ID | Assumption | Impact if Incorrect |
|---|---|---|
| TA-01 | The approved SRS and requirements registry provide the authoritative requirement IDs and expected system behavior. | Test cases may need revision if requirements change. |
| TA-02 | A test environment with the required frontend, backend, and database configuration will be made available before execution. | Environment-related failures may prevent planned tests from running. |
| TA-03 | Test accounts can be created for the roles required by the application. | Authentication and authorization tests may be delayed. |
| TA-04 | Test data can be prepared for valid and invalid vehicle details, vehicle capacities, facility capacities, and waste types. | Functional and boundary tests may not provide sufficient coverage. |
| TA-05 | Vehicle and facility capacity values are maintained consistently by the application and database. | Capacity-related test results may be unreliable if data is inconsistent. |
| TA-06 | The configured authentication mechanism supports password hashing, JWT validation, token expiration, and account lockout according to the SRS. | Security test cases may require adjustment if the implementation differs from the specification. |
| TA-07 | External map and email services may be unavailable or restricted in the test environment. | Tests depending on those services may require controlled test data or documented limitations. |
| TA-08 | The test team has access to the application interfaces and logs needed to observe test results. | Some defects may be harder to diagnose. |
| TA-09 | Test execution is performed using approved test accounts and non-production test data. | Testing may affect real data or expose sensitive information if this assumption is violated. |

## 11.3 Dependencies

The following dependencies may affect test execution:

- Availability of the application build and required backend services.
- Availability and correct configuration of the PostgreSQL database.
- Availability of the test accounts, roles, and representative test data.
- Access to the relevant application logs and audit records.
- HTTPS and TLS configuration for deployment-level security validation.
- Availability of external map, geocoding, and email services for tests that depend on them.
- Availability of the team members responsible for reviewing defects and verifying corrections.

## 11.4 Handling Invalid Assumptions

If an assumption is found to be incorrect:

1. Record the assumption ID and the observed condition.
2. Assess which test cases and requirements are affected.
3. Inform the test lead and relevant team member.
4. Update the test procedure or environment where appropriate.
5. Document tests that cannot be executed and the reason for the limitation.

## 11.5 Limitations

A test result is valid only for the configuration, test data, and environment in which the test was executed. Passing tests do not establish that every possible input, deployment configuration, or external-service failure has been covered.
