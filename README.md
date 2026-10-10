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

## Key Features (Planned)

- Citizen waste collection requests with priority levels
- Vehicle and capacity management
- Disposal facility management
- Optimized route generation based on location, capacity, priority and distance
- Admin dashboard
- Request status tracking

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
├── docs/            Project documentation (SRS, SAD, Test Plan)
│   └── diagrams/    UML and architecture diagrams
├── src/             Application source code
├── tests/           Automated tests
├── .gitignore       Files and folders excluded from version control
└── README.md        Project overview
```

## Project Deliverables

| Document                     | Status      |
|------------------------------|-------------|
| SRS                          | In progress |
| SAD (Architecture & Design)  | Not started |
| Test Plan                    | Not started |
| Implementation               | Not started |

## Contributing

1. Create a feature branch from the default branch: `feature/<name>`.
2. Commit your work with clear, descriptive commit messages.
3. Open a pull request to the default branch (`main`).
4. At least one teammate must review and approve the pull request before it is merged.
