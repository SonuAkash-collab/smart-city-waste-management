
# 10. Test Risks and Mitigation

## 10.1 Purpose

This section identifies risks that may affect the planning, execution, accuracy, and completion of testing for the Smart City Waste Management System.

## 10.2 Test Risks

| Risk ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| TR-01 | Test environment or database is unavailable during scheduled testing. | Medium | High | Verify environment readiness before testing and maintain a record of setup requirements. |
| TR-02 | Test data does not adequately represent vehicle loads, facility capacities, and collection priorities. | Medium | High | Prepare valid, invalid, boundary, and capacity-limit test data before execution. |
| TR-03 | External map or geocoding services are unavailable or respond slowly. | Medium | Medium | Use controlled test data where possible and record external-service failures separately. |
| TR-04 | Concurrent facility intake operations cause incorrect remaining-capacity values. | Medium | High | Test concurrent updates and verify that facility capacity cannot become negative or exceed its configured limit. |
| TR-05 | Security tests use incomplete or incorrectly configured test accounts. | Low | High | Prepare dedicated accounts with documented roles and reset their state before relevant tests. |
| TR-06 | Changes to requirements or API behavior make existing test cases outdated. | Medium | Medium | Review the requirements registry and update affected test cases after approved changes. |
| TR-07 | Insufficient time prevents complete execution of planned tests. | Medium | High | Prioritize critical functional and security tests and report unexecuted tests explicitly. |
| TR-08 | Performance results vary because of hardware, network, or environment differences. | Medium | Medium | Record the test environment, workload, and configuration when reporting performance results. |
| TR-09 | Defects in test data or test procedures produce misleading results. | Low | High | Review test steps and expected results before execution and repeat unexpected results after investigating the cause. |

## 10.3 Risk Monitoring

The test lead shall review identified risks throughout test planning and execution. New risks, changes in probability or impact, and mitigation actions shall be documented.

High-impact risks should be addressed before final acceptance wherever possible. Any unresolved high-impact risk must be reported to the team lead.

## 10.4 Defect and Risk Reporting

When a test fails:

1. Record the test case ID and the observed behavior.
2. Compare the actual result with the documented expected result.
3. Capture relevant logs or screenshots without exposing passwords, access tokens, or other secrets.
4. Report the defect to the team for investigation.
5. Re-run the affected test after the correction is available.

## 10.5 Residual Risks

Some risks, including external-service outages and deployment-environment differences, may remain outside the team's direct control. Such risks must be documented, and their impact on test results and system acceptance must be communicated clearly.
