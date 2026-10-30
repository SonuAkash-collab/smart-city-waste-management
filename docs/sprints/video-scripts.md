# Sprint demo video scripts

Record with the Windows Game Bar (Win + Alt + R) or OBS. Keep each file under 50 MB.
Before recording, start the app with fresh demo data (from the `backend` folder):

```
python scripts/seed_demo.py --reset
uvicorn app.main:app --reload
```

Open http://localhost:8000. Demo passwords: `Admin@1234` for the admin, `Demo@1234` for everyone else.

## Sprint 1 video (1 minute) — recorded by Rishit

| Time | Show | Say |
|---|---|---|
| 0:00–0:08 | Home page | "Team 04, Smart City Waste Management. This is Sprint 1." |
| 0:08–0:20 | Register a new citizen, land on "Request pickup" | "Citizens register and only see citizen pages." |
| 0:20–0:35 | Tap the map, choose Hazardous, 10 kg, submit | "The request is saved with a location, and gets High priority from its waste type." |
| 0:35–0:50 | Log out, log in as admin@scw.local, open Requests, approve the new request | "The admin filters requests and approves or rejects them, and can override priority." |
| 0:50–1:00 | Show `/docs` with the vehicles and facilities endpoints | "Vehicles, drivers and facilities are managed through the API. Sprint 2 adds routes." |

## Sprint 2 video (2 minutes) — recorded by Puru

| Time | Show | Say |
|---|---|---|
| 0:00–0:10 | Home page | "Sprint 2: the full collection cycle." |
| 0:10–0:30 | Citizen submits a request, then opens "My requests" | "The citizen can track status and cancel before it is scheduled." |
| 0:30–0:45 | Admin approves it; citizen opens Notifications | "Every status change creates an in-app notification and an email." |
| 0:45–1:10 | Admin opens Routes, picks today, generates routes; show stops and any facility stop | "Routes are planned by priority first, then nearest stop, without overloading any vehicle. Full vehicles detour to a suitable facility." |
| 1:10–1:35 | Log in as driver1, open My route, mark one stop Collected and one Missed | "Drivers see their stops on a map and mark each one; the request status updates automatically." |
| 1:35–1:50 | Operator records an intake; admin opens Facilities and sees remaining capacity drop | "Operators record deliveries and capacity updates at once." |
| 1:50–2:00 | Admin dashboard and CSV download | "The dashboard shows live counts, and the daily report downloads as CSV." |
