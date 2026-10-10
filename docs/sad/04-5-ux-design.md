# Software Architecture & Design

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 4.5 UX Design

The user experience is provided through the React-based, mobile-responsive Web Frontend. It is used on supported desktop and mobile browsers, supports screens at least 360 px wide, and presents functions according to the signed-in user's role. Role-specific menus shall not expose functions assigned to other roles; server-side authorization remains authoritative (SCW-F-002, SCW-SEC-004).

The interface uses Leaflet with OpenStreetMap for maps. Users interact through standard keyboard, pointer and touch input. Forms identify required inputs and display validation or operation errors returned by the system in readable form. No additional visual theme, navigation layout, or accessibility conformance target is specified.

### Role-Based User Interactions

| Role | Supported interface tasks |
|---|---|
| Citizen | Register and log in; submit a collection request; track its status; cancel it before it becomes Scheduled; receive in-app and email status notifications. |
| Collection Vehicle Driver | View an assigned route as ordered stops on a map and mark each stop Collected or Missed. |
| Admin / Municipal Officer | View, filter, approve and reject collection requests; override request priority; manage vehicles, facilities, and Driver and Operator accounts; generate routes; view the dashboard; export daily collection reports as CSV. |
| Disposal Facility Operator | Record incoming waste by vehicle and weight and manage facility capacity. |

The precise arrangement of these functions in menus, pages, or navigation is not specified and requires project-team confirmation.

### Citizen Collection-Request Submission

The request form collects the required location (map pin or address), waste type, and estimated quantity. A photo is optional. It is selected through the browser's standard file-selection interface; a device camera may be available through that interface, but is not required. The project documents do not define photo formats, size limits, or how the photo is transferred or stored.

The Web Frontend identifies required inputs and presents validation errors returned by the Request Service. In particular, a submission missing its required location is rejected with HTTP 422 (SCW-F-010). On successful submission, the Request Service accepts and stores the request and returns HTTP 201; when supplied, the photo is associated with the stored request.

The Request Service assigns priority from waste type and request age (SCW-F-011):

| Waste type | Priority |
|---|---|
| Hazardous / medical / e-waste | High |
| Mixed / general / recyclable | Medium |
| Garden / bulky | Low |

A request remaining in Submitted or Approved after 48 hours increases by one priority level, capped at High. An Admin / Municipal Officer may override the assigned level. The Admin dashboard lists pending (Submitted) requests by priority (SCW-F-051). The project documents do not specify whether or how priority is displayed to a Citizen; that presentation decision requires team confirmation.

### Request Status, Cancellation, and Notifications

Citizens can track their request through the supported statuses: Submitted, Approved, Scheduled, Collected, Rejected, Missed, and Cancelled (SCW-F-012). The SRS describes the progression as Submitted → Approved → Scheduled → Collected / Rejected / Missed / Cancelled. Cancellation is allowed only before Scheduled; a successful cancellation changes the status to Cancelled, while an attempt at Scheduled or later is rejected with HTTP 409 and leaves the status unchanged (SCW-F-013).

The system notifies the Citizen in-app and by email on every request status change (SCW-F-050). Notifications include the request ID, new status, and time of change. If the email provider is unavailable, the in-app notification is still created and the email is retried. Request status tracking and in-app notifications continue if the map service or email provider is unavailable. The project documents do not prescribe how status history or notifications are visually arranged in the Web Frontend.

### Other Role-Specific Views

- The Collection Vehicle Driver sees the assigned route as ordered stops on a map and can record Collected or Missed for each stop. Stop updates change request status.
- The Admin / Municipal Officer can filter requests by status, priority, waste type, and date; view pending requests listed by priority on the dashboard; generate routes; and access vehicle, facility, dashboard, and CSV-report functions.
- The Disposal Facility Operator can record incoming waste by vehicle and weight; the Facility Service updates remaining facility capacity.

The project context does not define detailed screen layouts, page transitions, route-map controls, dashboard visualizations, or the presentation of operation errors beyond readable messages. These UX details require project-team confirmation before implementation.
