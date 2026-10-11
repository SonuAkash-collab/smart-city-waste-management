# TC-USE-01: First-Time User Request Submission

## Test Case Information

| Field | Details |
|---|---|
| Test Case ID | TC-USE-01 |
| Requirement ID | SCW-NF-004 |
| Test Type | Usability |
| Priority | High |
| Status | Not run |

## Objective

Verify that first-time users can submit a request within 3 minutes on both a desktop layout and a mobile layout with a viewport width of 360 CSS pixels.

## Preconditions

- The application is available in the test environment.
- Five participants who have not previously used the application are recruited.
- Participants receive no task-specific training or assistance.
- A separate test account and required test data are available for each participant.
- The mobile viewport is configured to 360 CSS pixels wide.
- A timer and results-recording sheet are prepared.

## Test Data

- Participants: 5 first-time users.
- Layouts: Desktop and mobile at 360 CSS pixels wide.
- Time limit: 3 minutes per submission attempt.
- Total planned attempts: 10 (one desktop and one mobile attempt per participant).

## Test Steps and Expected Results

| Step | Action | Expected Result |
|---|---|---|
| 1 | Prepare the desktop layout and provide the participant with the request-submission task. | The participant can access the request form without task-specific training. |
| 2 | Start the timer when the participant begins the task. | The start time is recorded consistently. |
| 3 | Allow the participant to complete and submit the request without assistance. | The request is successfully submitted and a confirmation is displayed within 3 minutes. |
| 4 | Record the elapsed time and whether submission succeeded. | The participant's result is recorded accurately. |
| 5 | Repeat steps 1–4 for the mobile layout at 360 CSS pixels wide. | The form remains usable at the specified viewport width, and the request is successfully submitted within 3 minutes. |
| 6 | Repeat the desktop and mobile attempts for all five participants. | Results are recorded for all 10 planned attempts. |
| 7 | Compare each attempt with the acceptance criteria. | Each attempt is classified as pass or fail; failed and incomplete attempts are documented. |

## Acceptance Criteria

- All five participants must complete a request submission on desktop in 3 minutes or less.
- All five participants must complete a request submission on mobile at 360 CSS pixels wide in 3 minutes or less.
- A submission counts as successful only when the application accepts the request and displays confirmation.
- No participant may receive task-specific assistance during a measured attempt.
- The test passes only when all 10 attempts meet the time limit and succeed.

## Actual Results

| Participant | Desktop time/result | Mobile time/result |
|---|---|---|
| P1 | Not run | Not run |
| P2 | Not run | Not run |
| P3 | Not run | Not run |
| P4 | Not run | Not run |
| P5 | Not run | Not run |

## Outcome

- Status: Not run
- Usability issues observed: To be recorded after execution.
- Evidence location: To be recorded after execution.