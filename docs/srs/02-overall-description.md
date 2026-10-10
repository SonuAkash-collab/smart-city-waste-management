## 2. Overall Description

### 2.1 Product Perspective

The Smart City Waste Management System is a new, self-contained web application. It replaces manual, phone- and paper-based handling of collection requests and fixed collection schedules with a single system in which requests, vehicles, facilities and routes share one database.

The system follows a layered (3-tier) architecture:

- **Presentation layer:** Web Frontend (React, mobile-responsive) used by all four roles; maps rendered with Leaflet and OpenStreetMap.
- **Application / service layer:** Python FastAPI REST services: Auth & User Service, Request Service, Fleet Service, Facility Service, Route Optimization Engine, and Notification & Reporting Service.
- **Data layer:** PostgreSQL database.

External systems the product depends on:

| External system | Used for |
|---|---|
| Map Service (OpenStreetMap) | Map tiles, geocoding of addresses, distance data (optionally OSRM road distance) |
| Email provider (SMTP) | Sending status-change notification emails to citizens |
| Web browser | Running the Web Frontend on desktop and mobile devices |

### 2.2 Major Product Functions

| Function area | Summary | Requirements |
|---|---|---|
| Authentication & roles | Register and log in with email and password; role-based access for four roles; Admin manages Driver and Operator accounts | SCW-F-001 – SCW-F-003 |
| Collection requests | Citizens submit, track and cancel requests; automatic priority assignment; Admin approves or rejects | SCW-F-010 – SCW-F-014 |
| Vehicle management | Admin manages vehicles, their status and driver assignment; system tracks vehicle load during a route | SCW-F-020 – SCW-F-023 |
| Facility management | Admin manages disposal facilities; Operators record incoming waste; full or unsuitable facilities are excluded | SCW-F-030 – SCW-F-032 |
| Route generation | Admin generates daily routes ordered by priority then distance within vehicle capacity; drivers view routes and mark stops | SCW-F-040 – SCW-F-044 |
| Notifications & reports | Citizens notified on every status change; Admin dashboard; daily CSV collection report | SCW-F-050 – SCW-F-052 |

### 2.3 User Roles and Characteristics

| Role | Description | Main tasks | Expected technical skill |
|---|---|---|---|
| Citizen | Resident of the city requesting waste collection | Submit requests, track status, cancel requests before they are Scheduled, receive notifications | Basic smartphone or web browser use; no training (see SCW-NF-004) |
| Collection Vehicle Driver | Municipal driver assigned to one vehicle | View the day's assigned route on a map, mark each stop Collected or Missed | Basic smartphone use; up to 30 minutes of onboarding |
| Admin / Municipal Officer | Municipal staff responsible for collection operations | Approve or reject requests, override priority, manage vehicles, facilities and accounts, generate routes, view the dashboard, export reports | Regular office computer use; up to 2 hours of onboarding |
| Disposal Facility Operator | Staff at a landfill, recycling or composting facility | Record incoming waste (vehicle, weight), monitor remaining capacity | Basic computer or tablet use; up to 30 minutes of onboarding |

Each user has exactly one role. Citizens self-register; Driver and Operator accounts are created only by an Admin (SCW-F-003).

### 2.4 Operating Environment

| Item | Requirement |
|---|---|
| Client | Current versions of Chrome, Firefox, Edge or Safari on desktop, Android or iOS; screen width ≥ 360 px |
| Server | Linux server or cloud VM running Python 3.11+ with FastAPI and an ASGI server (Uvicorn) |
| Database | PostgreSQL 15 or later |
| Network | Internet connection; all client-server traffic over HTTPS with TLS 1.2+ (SCW-SEC-003) |
| External services | OpenStreetMap tile and geocoding services; SMTP email provider |

### 2.5 Design and Implementation Constraints

- The backend shall be implemented in Python with FastAPI, the frontend in React, and persistent data stored in PostgreSQL.
- All APIs shall be REST/JSON under the base path `/api/v1` and authenticated with JWT bearer tokens in the `Authorization` header.
- Error responses shall use the body `{ "error": { "code": "STRING_CODE", "message": "Readable message" } }` with standard HTTP status codes (400, 401, 403, 404, 409, 422, 500).
- Passwords shall be stored only as bcrypt hashes (SCW-SEC-001); JWT access tokens shall expire after 30 minutes (SCW-SEC-002).
- Distances shall be computed with the Haversine formula, optionally replaced by OSRM road distance.
- Route generation shall use a greedy heuristic (priority first, then nearest-next stop, within vehicle capacity) rather than an exact optimisation solver, to meet SCW-NF-001.
- Maps shall use OpenStreetMap data, subject to its usage policy and attribution requirements.
- Only open-source tools and libraries shall be used; the project is developed by a 4-person student team within a fixed academic schedule.

#### Assumptions and Dependencies

- Citizens provide a valid email address and a location that can be pinned on the map.
- Vehicle capacities (kg) and facility daily capacities (kg) entered by the Admin are accurate.
- Drivers have a mobile device with internet access during their route.
- OpenStreetMap and the email provider are available; if they are unavailable, map display and email notifications are degraded but in-app status tracking continues.
