# TC-MNT-01: Service-Layer Unit Test Coverage

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-MNT-01 |
| Requirement ID | SCW-NF-005 |
| Test Type | Maintainability / Unit Test Coverage |
| Priority | High |
| Status | Not run |

## Objective

Verify that the backend service layer achieves at least 70% statement coverage using pytest and pytest-cov.

## Preconditions

- The backend source code and test suite are available.
- The project's Python dependencies, including pytest and pytest-cov, are installed.
- The service-layer source directory or package is identified in the project configuration.
- Tests can run in an isolated test environment with required test configuration and data.

## Test Configuration

- Test runner: pytest
- Coverage tool: pytest-cov
- Coverage target: backend service layer
- Minimum required statement coverage: 70%

## Test Steps and Expected Results

| Step | Action | Expected Result |
|---|---|---|
| 1 | Verify that the service-layer coverage target is correctly configured. | Coverage includes the intended service-layer source files and excludes unrelated modules from the service-layer measurement. |
| 2 | Run the project's test suite with pytest-cov configured for the service layer. | Tests execute and a coverage report is generated. |
| 3 | Review the report for total statements, covered statements, missed statements, and percentage coverage. | The report provides enough information to reproduce the coverage result. |
| 4 | Calculate or verify the reported statement-coverage percentage. | Coverage is calculated as covered statements divided by total measured statements, multiplied by 100. |
| 5 | Compare the result against the 70% threshold. | Pass if service-layer statement coverage is at least 70%; otherwise, fail. |
| 6 | Record test failures and coverage gaps. | Failures and uncovered service-layer code are documented for follow-up. |

## Example Command

Use the actual service-layer package or directory configured in the repository:

`pytest --cov=<service_layer_package_or_directory> --cov-report=term-missing`

Replace `<service_layer_package_or_directory>` with the repository's real service-layer path before executing the test. Do not treat the placeholder command as an executed test.

## Acceptance Criteria

- The service-layer test suite completes and produces a coverage report.
- Coverage measures the intended backend service layer.
- Statement coverage is **at least 70%**.
- The test result and report are recorded.
- A command failure or missing coverage report does not count as a pass.

## Actual Results

- Command executed:
- Test result:
- Total statements:
- Covered statements:
- Missed statements:
- Coverage percentage:
- Report/evidence location:

## Outcome

- Status: Not run
- Coverage gaps or defects: To be recorded after execution.