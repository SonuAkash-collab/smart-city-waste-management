### TC-NOT-01: Notification on status change

| Field | Content |
|---|---|
| TC ID | TC-NOT-01 |
| Title | Citizen receives a notification on every request status change |
| Requirement(s) | SCW-F-050 |
| Type | Functional |
| Preconditions | 1. System is deployed in the test environment with the email provider replaced by a test SMTP inbox (e.g. MailHog). 2. An active Citizen account and an active Admin account exist. 3. The Citizen has no existing notifications. |
| Test data | Citizen: `citizen1@test.local` / `Citizen@123`; Admin: `admin1@test.local` / `Admin@123`; new request: waste type `Household`, estimated quantity `20 kg`, location pinned on the map |
| Steps | 1. Log in as the Citizen and submit a new collection request with the test data; note the request ID. 2. Log in as the Admin and approve the request (`PATCH /api/v1/requests/{id}/status` with `{ "status": "APPROVED" }`). 3. As the Citizen, submit a second request with the same test data; then, as the Admin, reject it (`{ "status": "REJECTED" }`). 4. Wait 5 minutes. 5. As the Citizen, open the in-app notification list. 6. Open the test SMTP inbox for `citizen1@test.local`. |
| Expected result | Step 5: exactly 4 in-app notifications are shown (request 1: Submitted, Approved; request 2: Submitted, Rejected), each created within 1 minute of the status change and each showing the request ID, the new status and the time of the change. Step 6: exactly 4 emails are received, with the same request ID, status and time as the in-app notifications. No notification is sent to any other user. |
| Actual result | See the execution record below. |
| Status | Pass |

## Execution record (Part 3, November 2026)

| Field | Details |
|---|---|
| Changes after the sprints | Each notification states the request id, the new status and the UTC time. Emails go through SMTP when configured, otherwise to `email-outbox.log`. |
| Automated tests | `test_notifications.py`, `test_requests_admin.py::test_every_status_change_notifies_owner` |
| Actual result | Submit, approve, submit, reject produced exactly 4 in-app notifications for the citizen with request id, status and time, and 4 matching emails; no other user was notified. |
| Status | Pass |

Emails were checked through the outbox. To check with a real inbox, run MailHog and set SMTP_HOST=localhost, SMTP_PORT=1025.
