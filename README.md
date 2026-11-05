# Smart City Waste Management System

A platform for coordinating waste collection requests, vehicles and disposal facilities through optimized collection routes.

## About

This repository contains the Software Engineering Mini Project of Team 04, PES University.

## Problem Statement

Manage waste collection requests, vehicles and disposal facilities. Generate efficient collection routes using location, capacity, priority and distance.

## Team

| Name            | SRN           |
|-----------------|---------------|
| Sonu Akash      | PES1UG24AM908 |
| Rishit V N S    | PES1UG24AM225 |
| Rottela Haritej | PES1UG24AM231 |
| Purushothama KC | PES1UG25AM810 |

## Features

- Citizens request pickups on a map and follow each request until it is collected
- Priority from waste type, raised after 48 hours, with Admin override
- Route generation: priority first, then nearest stop, within vehicle capacity, with detours to suitable facilities
- Drivers see their route on a map and mark stops Collected or Missed
- Operators record deliveries; facility capacity updates at once
- In-app and email notifications, Admin dashboard and daily CSV report
- JWT login, roles checked on the server, account lockout, audit log

## Users and Roles

- **Citizen**: submits waste collection requests and tracks their status
- **Collection Vehicle Driver**: views assigned routes and updates collection progress
- **Admin / Municipal Officer**: manages requests, vehicles and facilities, and oversees route generation
- **Disposal Facility Operator**: manages facility capacity and records incoming waste

## Tech Stack

| Layer             | Choice                                                                 |
|-------------------|------------------------------------------------------------------------|
| Frontend          | React (web, mobile-responsive) + Leaflet/OpenStreetMap for maps        |
| Backend           | Python FastAPI (REST, JSON)                                            |
| Database          | PostgreSQL                                                             |
| Auth              | JWT bearer tokens, bcrypt password hashing                             |
| Distance          | Haversine distance (optionally OSRM road distance)                     |
| Routing algorithm | Greedy heuristic: approved requests sorted by priority first, then nearest-next stop, while vehicle load ≤ capacity. When full, go to the nearest facility that accepts that waste type and has capacity, then continue. |
| Tools             | GitHub, PlantUML/draw.io, Swagger (FastAPI auto-docs), Postman, Pytest, JMeter/Locust |

## Architecture

**Layered (3-tier) architecture:** Presentation (React) → Application/Service layer (FastAPI services) → Data layer (PostgreSQL).

- **Rationale:** clear separation of concerns, easy for a 4-person team, easy to test each layer.
- **Rejected alternative:** microservices, because they are too complex to deploy and operate at this scale.

## Repository Structure

```
.
├── backend/            FastAPI app (app/), tests (tests/), scripts (scripts/)
├── frontend/           Web app (React + Leaflet browser builds, no build step)
├── docs/               SRS, SAD, Test Plan, test cases, sprint notes, reports, user guide
└── .github/workflows/  CI: tests with coverage on every pull request
```

## How to run

Python 3.11 or newer. From the repository folder:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_demo.py --reset  # demo data (optional)
uvicorn app.main:app --reload
```

Open http://localhost:8000 for the web app and http://localhost:8000/docs for the API.
Demo accounts: `admin@scw.local` / `Admin@1234`; `citizen1@scw.local`, `driver1@scw.local`, `operator1@scw.local` / `Demo@1234`.
Without demo data, create the first Admin with `python scripts/create_admin.py --email you@example.com --password <password>`.
After pulling model changes, run `python scripts/seed_demo.py --reset` again (it rebuilds the tables).

## Tests and reports

```bash
cd backend
python -m pytest --cov=app --cov-branch          # all tests with coverage
python scripts/generate_reports.py               # writes docs/reports/*.md
pip install -r requirements-perf.txt && python scripts/run_perf.py   # load test (TC-PERF-01/02)
```

Reports: `docs/reports/`. Sprint notes and deviations: `docs/sprints/`. User guide: `docs/user-guide.md`.
