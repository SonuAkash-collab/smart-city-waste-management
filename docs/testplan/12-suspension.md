
# 12. Test Suspension and Resumption Criteria

## 12.1 Purpose

This section defines the conditions under which testing of the Smart City Waste Management System may be suspended and the criteria required before testing resumes.

## 12.2 Suspension Criteria

Testing may be suspended when one or more of the following conditions occur:

| ID | Suspension Condition | Reason |
|---|---|---|
| TS-01 | The application cannot be started or a critical service is unavailable. | Planned tests cannot be executed reliably. |
| TS-02 | The test database is unavailable, corrupted, or contains inconsistent test data. | Results may be invalid or unreproducible. |
| TS-03 | A critical defect prevents execution of a major application workflow. | Continuing dependent tests would provide little useful evidence. |
| TS-04 | Authentication or authorization failures prevent safe access to the test environment. | Test execution may be unsafe or invalid. |
| TS-05 | Test data or environment configuration differs materially from the documented test setup. | Expected results may no longer be reliable. |
| TS-06 | An external dependency required by a test is unavailable and no approved alternative exists. | The affected test cannot be completed as designed. |
| TS-07 | Testing causes unexpected changes to shared or non-test data. | Further execution could cause additional unintended changes. |

## 12.3 Suspension Procedure

When a suspension condition is identified:

1. Stop the affected test and any dependent tests.
2. Preserve the current test results and relevant diagnostic evidence.
3. Record the affected test case IDs, observed condition, and reason for suspension.
4. Inform the test lead and the responsible team member.
5. Identify the corrective action required before resuming testing.
6. Continue unaffected tests only when they can be executed safely and independently.

## 12.4 Resumption Criteria

Testing may resume when all applicable conditions below have been satisfied:

- The application services and required test environment are available.
- Database connectivity and test-data integrity have been verified.
- The blocking defect has been corrected or an approved workaround is available.
- Authentication and authorization permit safe access to the test environment.
- The environment matches the documented test configuration.
- Required external dependencies or approved alternatives are available.
- The test lead or responsible team member has confirmed that the affected tests can continue.

## 12.5 Resumption Procedure

1. Verify that the suspension cause has been resolved.
2. Repeat relevant setup and readiness checks.
3. Re-run tests affected by the interruption when necessary.
4. Record the new execution results and link them to the original issue.
5. Resume the remaining planned tests.
6. Update the test status and report any unresolved limitations.

## 12.6 Documentation and Approval

Each suspension and resumption event shall be documented with the date, reason, affected test cases, corrective action, and final status. Unresolved issues that could affect acceptance must be reported to the team lead before final test-plan approval.
