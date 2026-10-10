# Software Architecture & Design

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 4.1 Design Overview

The Smart City Waste Management System uses the layered (3-tier) architecture selected in Section 3.5. The **Web Frontend** forms the Presentation layer, the FastAPI services form the Application / Service layer, and **Database (PostgreSQL)** forms the Data layer. The Web Frontend communicates with the backend through REST APIs using JSON under `/api/v1`; the services access persistent application data through the Data layer. The browser does not connect directly to the database.

This design separates the user interface, application behavior and persistent storage. It uses the agreed technology stack and component boundaries, supports testing each layer, and is suitable for the four-person project team. Microservices were rejected because they would be too complex to deploy and operate at this scale. Further rationale for the selected pattern is in Section 3.5.

### Major Components

| Component | Design responsibility | Related requirements |
|---|---|---|
| **Web Frontend** | React web interface for all four roles; presents role-appropriate functions and maps using Leaflet/OpenStreetMap. | All functional requirements; SCW-NF-004; SCW-SEC-003 |
| **Auth & User Service** | Handles registration, login, JWTs, roles and account management. | SCW-F-001–SCW-F-003; SCW-SO-1; SCW-SEC-001, SCW-SEC-002, SCW-SEC-004–SCW-SEC-006 |
| **Request Service** | Creates, tracks, cancels and approves collection requests; assigns request priority. | SCW-F-010–SCW-F-014 |
| **Fleet Service** | Manages vehicles, drivers, vehicle status and vehicle load. | SCW-F-020–SCW-F-023 |
| **Facility Service** | Manages disposal facilities, incoming-waste intake and facility capacity. | SCW-F-030–SCW-F-032 |
| **Route Optimization Engine** | Generates collection routes and handles driver stop updates. | SCW-F-040–SCW-F-044; SCW-NF-001 |
| **Notification & Reporting Service** | Provides status notifications, the Admin dashboard and CSV export. | SCW-F-050–SCW-F-052 |
| **Database (PostgreSQL)** | Stores persistent application data used by the services. | Supports persistence across the functional requirements |
| **Map Service (OpenStreetMap)** | Supplies map tiles, geocoding and distance data used by map and routing functions. | SCW-F-010, SCW-F-043 |

### Component Interactions

1. **Authentication and role-based access:** A user interacts with the Web Frontend to register or log in. The Auth & User Service manages account credentials and JWT bearer tokens. Server-side role checks are enforced for every API call; role-specific presentation in the Web Frontend does not replace authorization. (SCW-F-001–SCW-F-003, SCW-SEC-001, SCW-SEC-002, SCW-SEC-004)
2. **Collection requests:** A Citizen submits request details through the Web Frontend. The Map Service (OpenStreetMap) supports location selection and geocoding; the Request Service validates and manages the request, assigns priority, and stores request data using Database (PostgreSQL). The Admin / Municipal Officer uses the same frontend to view, filter, approve or reject requests, and override priority. Citizens use it to track status and cancel requests when permitted. Status changes are made available to the Notification & Reporting Service. (SCW-F-010–SCW-F-014, SCW-F-050)
3. **Vehicles and facilities:** The Admin / Municipal Officer manages vehicles through the Fleet Service and disposal facilities through the Facility Service. The Disposal Facility Operator records incoming waste through the Facility Service, which updates facility capacity. The services persist their data using Database (PostgreSQL). (SCW-F-020–SCW-F-023, SCW-F-030–SCW-F-032)
4. **Route generation and collection:** On an Admin route-generation request, the Route Optimization Engine uses approved requests from the Request Service, available vehicles and load information from the Fleet Service, and facility eligibility and capacity from the Facility Service. It orders approved requests by priority first and then nearest-next stop, keeping vehicle load within capacity. When a vehicle is full, the route goes to the nearest facility that accepts the waste type and has capacity before continuing. Distance uses the Haversine formula, with OSRM road distance optional. Generated routes are saved, and the driver is notified. The Collection Vehicle Driver views the assigned route as ordered map stops and records Collected or Missed outcomes through the Web Frontend; stop outcomes update request status and support status notifications. (SCW-F-023, SCW-F-032, SCW-F-040–SCW-F-044, SCW-F-050, SCW-NF-001)
5. **Notifications and reporting:** The Notification & Reporting Service provides Citizens with in-app and email notifications on request status changes, supports the Admin dashboard using operational data, and exports daily collection reports as CSV. Email delivery uses the external SMTP provider. (SCW-F-050–SCW-F-052)

### Cross-Cutting Design Conventions

- Backend APIs use REST and JSON under `/api/v1`. Authenticated requests carry a JWT bearer token in the `Authorization` header. Request Service endpoint details are specified in Section 4.3.
- API errors use `{ "error": { "code": "STRING_CODE", "message": "Readable message" } }` with the agreed HTTP status codes.
- Passwords are stored as bcrypt hashes, JWT access tokens expire after 30 minutes, and server-side role checks apply to every API call. Administrative actions identified by the project security requirement are written to an audit log. (SCW-SEC-001–SCW-SEC-006)
- Client-server traffic uses HTTPS with TLS 1.2 or later (SCW-SEC-003). Whether this requirement applies to OpenStreetMap and SMTP connections, and the method for verifying transport security on those connections, remains an open specification item for project-team confirmation.

### Open Design Details

The project context does not specify the database schema at column level, deployment topology, or the internal communication mechanism between services in the Application / Service layer. These details are not assumed by this overview and require project-team confirmation if they are needed for implementation.

SAD Section 3.8 additionally maps the Map Service (OpenStreetMap) as supporting SCW-F-030, SCW-F-041 and SCW-NF-004. This broader mapping differs from the component mapping in the project context and requires project-team confirmation.
