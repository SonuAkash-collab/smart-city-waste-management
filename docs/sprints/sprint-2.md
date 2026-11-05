# Sprint 2 summary

| Item | Value |
|---|---|
| Sprint | 2 |
| Dates | Mon 2 Nov 2026 to Wed 4 Nov 2026 (planned 26 to 30 Oct; see `deviations.md`) |
| Goal | The full collection cycle: routes, drivers, tracking, notifications, dashboard, security |
| Result | All Sprint 2 stories merged; development frozen on 4 Nov |

## Stories completed

| Story | Owner | Points | Requirements |
|---|---|---|---|
| Generate routes API | Haritej | 5 | SCW-F-040 to SCW-F-042 |
| Routes list + driver marks stop, request status updates | Haritej | 3 | SCW-F-043, SCW-F-044 |
| Driver route page with map | Haritej | 4 | SCW-F-043 |
| Track status + cancel request API | Rishit | 3 | SCW-F-012, SCW-F-013 |
| Citizen "my requests" page | Rishit | 3 | SCW-F-012, SCW-NF-004 |
| Admin requests page | Rishit | 2 | SCW-F-014 |
| In-app notifications on status change (plus email) | Sonu | 3 | SCW-F-050 |
| Admin dashboard API + page | Sonu | 3 | SCW-F-051 |
| CSV daily collection report | Sonu | 3 | SCW-F-052 |
| Account lockout after 5 failed logins | Puru | 3 | SCW-SEC-005 |
| Audit log for admin actions | Puru | 3 | SCW-SEC-006 |
| Admin vehicle/facility pages + operator page | Puru | 5 | SCW-F-020 to SCW-F-031 |
| Deviations note + Sprint 2 docs | Puru | 1 | Part 2 item 2i |

Points completed: 41 of 41 planned. Haritej also added the Locust load test and the availability monitor for Part 3.

## What the demo shows

Citizen request → admin approval → route generation with a facility detour → driver marks stops on a map →
citizen notification and status → operator records a delivery → dashboard and CSV report. Script: `video-scripts.md`.

## Retrospective

| Went well | To improve |
|---|---|
| The pure route engine from Sprint 1 plugged straight into the API. | A browser check found two pages that crashed when you left them; we now walk through every page before merging. |
| Every page was checked at 360 px wide. | Load testing should start earlier; it found two defects only in Sprint 3. |
| CI kept `main` green through 30+ merges. | Agree on test data names (waste types) before writing test cases. |
