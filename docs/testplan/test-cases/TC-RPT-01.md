# TC-RPT-01: Dashboard Counts and Daily Collection CSV Export

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-RPT-01 |
| Requirement IDs | SCW-F-051, SCW-F-052 |
| Test Type | Functional / Reporting |
| Priority | High |
| Status | Not run |

## Objective

Verify that dashboard counts match the underlying application records and that the daily collection CSV export contains exactly one row per collection recorded for the selected day, with the correct columns and values.

## Preconditions

- The application and test database are available.
- A user with permission to access the dashboard and export reports is available.
- The expected dashboard count definitions and CSV column names are documented.
- Test data can be identified by collection date.

## Test Data

Prepare controlled records for a selected test date, including:

- Multiple collections recorded on that date.
- At least one collection recorded on a different date.
- Requests or records in different statuses relevant to the dashboard.
- Known expected counts for each dashboard metric.
- Known expected values for the fields included in the CSV export.

Record the test dataset and expected counts before execution.

## Test Steps and Expected Results

| Step | Action | Expected Result |
|---|---|---|
| 1 | Prepare the test records and calculate the expected dashboard counts from the underlying records. | Expected counts are recorded independently before checking the dashboard. |
| 2 | Open the dashboard using an authorized account. | The dashboard loads successfully. |
| 3 | Compare each displayed dashboard count with the independently calculated expected count. | Every displayed count matches the corresponding underlying records and defined status/date filters. |
| 4 | Select the test date and export the daily collection report as CSV. | A CSV file is generated for the selected date. |
| 5 | Open and parse the exported CSV, checking its header row against the documented export column names. | The CSV contains the expected columns with the correct names and order, as defined by the application specification. |
| 6 | Count the data rows and compare them with the collections recorded for the selected date. | The CSV contains exactly one data row per collection for that day, with no missing or duplicate collection rows. |
| 7 | Compare exported values against the underlying records. | Each row contains the correct values for its corresponding collection. |
| 8 | Verify that records outside the selected date are not included. | Collections from other dates are excluded from the daily export. |

## Acceptance Criteria

- All dashboard counts match the corresponding underlying records and documented counting rules.
- The CSV header matches the documented export schema.
- The CSV contains exactly one data row per collection recorded on the selected day.
- No collection is missing or duplicated.
- Exported values match the source records.
- Collections outside the selected day are excluded.
- The test passes only when all applicable criteria are satisfied.

## Actual Results

- Test date:
- Expected dashboard counts:
- Actual dashboard counts:
- Expected number of daily collections:
- Actual CSV data-row count:
- CSV column names/order:
- Missing or duplicate rows:
- Evidence location:

## Outcome

- Status: Not run
- Defects or observations: To be recorded after execution.