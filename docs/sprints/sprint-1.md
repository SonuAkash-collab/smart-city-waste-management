# Sprint 1 summary

| Item | Value |
|---|---|
| Sprint | 1 |
| Dates | Thu 29 Oct 2026 to Sun 1 Nov 2026 (planned 19 to 23 Oct; started late, see note) |
| Goal | A working core: log in, submit a request on a map, approve it, manage vehicles and facilities, plan routes |
| Board | GitHub Project "Team 04 Sprint Board" (Story Points and Sprint fields) |

**Note on dates.** The course plan put Sprint 1 in 19 to 23 Oct. The team only received the Part 2 instructions late, so the backlog was created on 29 Oct and Sprint 1 ran from 29 Oct to 1 Nov. This is recorded as a deviation in `deviations.md`.

## Stories completed

| Story | Owner | Points | Requirements |
|---|---|---|---|
| Backend skeleton + DB models | Sonu | 5 | SAD 3.3, 3.6 |
| Register/login with JWT + bcrypt | Sonu | 5 | SCW-F-001, SCW-SEC-001, SCW-SEC-002 |
| Role guard + admin creates driver/operator accounts | Sonu | 3 | SCW-F-002, SCW-F-003, SCW-SEC-004 |
| Login/register pages + role-based menu | Sonu | 3 | SCW-F-001, SCW-F-002 |
| Frontend skeleton | Rishit | 3 | SAD 4.5 |
| Submit request API with validation | Rishit | 3 | SCW-F-010 |
| Priority auto-assign + admin override | Rishit | 3 | SCW-F-011 |
| Citizen submit page with map pin | Rishit | 5 | SCW-F-010, SCW-NF-004 |
| Admin approve/reject API with filters | Rishit | 3 | SCW-F-014 |
| Haversine distance helper | Haritej | 2 | SCW-F-041 |
| Greedy route engine | Haritej | 5 | SCW-F-040, SCW-F-041, SCW-NF-001 |
| Facility detour when vehicle full + admin alert | Haritej | 3 | SCW-F-042 |
| GitHub Actions CI: pytest on every PR | Haritej | 3 | Part 2 item 2b |
| Vehicle add/edit + status API | Puru | 3 | SCW-F-020, SCW-F-021 |
| Assign driver to vehicle | Puru | 2 | SCW-F-022 |
| Facility add/edit API | Puru | 3 | SCW-F-030 |
| Operator records intake, capacity updates | Puru | 3 | SCW-F-031, SCW-F-032 |
| Vehicle load tracking | Puru | 2 | SCW-F-023 |

Points completed: 59 of 59 planned for Sprint 1.

## What the demo shows

1. A citizen registers, logs in and sees only the citizen menu.
2. The citizen drops a pin on the map, picks a waste type and submits; the request gets a priority from its waste type.
3. The admin filters the request list and approves or rejects requests.
4. Vehicles, drivers and facilities are managed through the API (Swagger at `/docs`); their pages follow in Sprint 2.

## How we worked

* Every story was built on its own branch, opened as a pull request, reviewed by the partner (Sonu and Rishit, Haritej and Puru) and merged with **Rebase and merge**.
* GitHub Actions runs the full test suite with coverage on every pull request; `main` requires the check to pass.
* Commits were kept small (one logical change each) so each member's work is visible.

## Retrospective

| Went well | To improve |
|---|---|
| Shared error format, camelCase JSON and role guard were agreed first, so later work fitted together. | Start earlier: the late start squeezed Sprint 1 into four days. |
| The route engine is pure Python, so it was tested without a database. | Review pull requests within a few hours so nobody waits. |
| Tests run in under 10 seconds, so CI feedback is quick. | Write the sprint notes during the sprint, not after. |

## Carried into Sprint 2

Route generation API and driver page, citizen tracking pages, notifications (in-app and email), dashboard and CSV report, account lockout, audit log, fleet and facility pages.
