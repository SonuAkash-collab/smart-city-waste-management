### 3.1 Goals and Constraints

#### Goals

| Goal | Description | Related requirements |
|---|---|---|
| Centralise waste-collection operations | Provide one system for Citizens to submit and track collection requests and for municipal staff to manage requests, vehicles, facilities and routes. | SCW-F-010–SCW-F-014, SCW-F-020–SCW-F-023, SCW-F-030–SCW-F-032 |
| Support capacity-aware collection routing | Generate daily routes from approved requests, order stops by priority and distance, respect vehicle capacity, and direct vehicles to suitable facilities when full. | SCW-F-040–SCW-F-044 |
| Support all four user roles | Provide role-appropriate functions for Citizen, Collection Vehicle Driver, Admin / Municipal Officer, and Disposal Facility Operator. | SCW-F-001–SCW-F-003, SCW-F-010–SCW-F-014, SCW-F-020–SCW-F-023, SCW-F-030–SCW-F-032, SCW-F-040–SCW-F-044 |
| Provide operational visibility and notifications | Notify Citizens about request status changes and provide the Admin dashboard and daily CSV collection report. | SCW-F-050–SCW-F-052 |
| Meet specified quality and security requirements | Meet the registered performance, availability, usability, modularity, and security targets and controls. | SCW-NF-001–SCW-NF-005, SCW-SO-1–SCW-SO-2, SCW-SEC-001–SCW-SEC-006 |

#### Constraints

**Technical constraints**

- The system uses the agreed layered (3-tier) architecture: React Presentation layer, Python FastAPI Application / Service layer, and PostgreSQL Data layer.
- The Web Frontend uses Leaflet with OpenStreetMap for map tiles and geocoding. Distance uses the Haversine formula, with OSRM road distance optional.
- APIs use REST and JSON under `/api/v1`; authenticated requests use JWT bearer tokens in the `Authorization` header. API errors use `{ "error": { "code": "STRING_CODE", "message": "Readable message" } }` and the agreed HTTP status codes.
- Passwords are stored only as bcrypt hashes; JWT access tokens expire after 30 minutes; client-server traffic uses HTTPS with TLS 1.2 or later; server-side role checks are enforced for every protected API request (SCW-SEC-001–SCW-SEC-004).
- Route generation uses the agreed greedy heuristic: approved requests are sorted by priority first and then nearest-next stop, vehicle load remains within capacity, and a full vehicle goes to the nearest facility that accepts the waste type and has capacity.

**Operational constraints**

- Clients require Internet access and a supported browser; drivers require a mobile device with Internet access while on route.
- The system depends on OpenStreetMap services for map tiles and geocoding and on an SMTP email provider for status-change email notifications. Working assumption: if either external service is unavailable, map display or email delivery may be degraded, while request status tracking and in-app notifications continue.
- The project is developed by a four-person student team within a fixed academic schedule.

**Business and scope constraints**

- The system addresses waste collection requests, vehicles, disposal facilities, and collection-route generation for Citizens and municipal operations; requirements and access are defined for the four project roles.
- Working assumption: Version 1.0 is limited to the capabilities defined in SRS Sections 4 and 5. Real-time GPS tracking of vehicles, payment or billing, native mobile applications, and integration with external municipal ERP systems are outside that defined scope.
- Route optimization is limited to the agreed greedy heuristic; an exact optimisation solver is not part of the selected approach.

**SCW-F-011 priority rule:** Hazardous / medical / e-waste → High; Mixed / general / recyclable → Medium; Garden / bulky → Low. Requests remaining in Submitted or Approved after 48 hours increase by one priority level, capped at High.

**Working assumption:** SCW-SEC-003 applies to browser-to-backend client-server communication, consistent with its detailed wording in SRS Section 5.1. This section does not assert an additional transport-security requirement or verification method for OpenStreetMap or SMTP connections.
