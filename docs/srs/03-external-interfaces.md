## 3. External Interface Requirements

### 3.1 User Interfaces

The system shall provide a responsive web interface implemented in React and usable in current versions of Chrome, Firefox, Edge and Safari on desktop, Android and iOS devices. The interface shall support screens at least 360 px wide.

The Web Frontend shall present functions according to the signed-in user's role: Citizen, Collection Vehicle Driver, Admin / Municipal Officer, or Disposal Facility Operator. It shall provide:

- **Citizen:** registration and login; a collection-request form for location (map pin or address), waste type, estimated quantity and an optional photo; request status tracking; cancellation while the request is not Scheduled; and in-app status notifications.
- **Collection Vehicle Driver:** an assigned route shown as ordered stops on a map, with controls to mark each stop Collected or Missed.
- **Admin / Municipal Officer:** interfaces to view, filter, approve and reject collection requests; manage vehicles, facilities and Driver and Operator accounts; generate routes; override request priority; view the dashboard; and export daily collection reports as CSV.
- **Disposal Facility Operator:** an interface to record incoming waste by vehicle and weight and manage facility capacity.

The interface shall use Leaflet with OpenStreetMap for maps. A location may be supplied as an address or selected as a map pin. Forms shall identify required inputs and display validation or operation errors returned by the system in readable form. Role-specific menus shall not expose functions assigned to other roles; server-side authorization remains authoritative.

### 3.2 Hardware Interfaces

The system has no dedicated hardware interfaces, specialized peripherals, or direct control interfaces. Users access the Web Frontend using a desktop, tablet or mobile device with a supported web browser and Internet connectivity. The interface shall accept standard keyboard, pointer and touch input and render on the device display.

The optional request photo shall be selected through the browser's standard file-selection interface, including a device camera when the browser and device make it available. A camera is not required to submit a request. The system does not require or interface directly with vehicle GPS hardware; drivers view assigned routes and update stop status through the Web Frontend.

### 3.3 Software Interfaces

| Software interface | Interaction and data |
|---|---|
| Web browser | Runs the React Web Frontend on supported desktop and mobile browsers. |
| FastAPI REST API | The Web Frontend communicates with the backend over JSON REST endpoints under `/api/v1`. Authenticated requests use a JWT bearer token in the `Authorization` header. |
| PostgreSQL | The backend services store and retrieve persistent application data in PostgreSQL. The browser does not connect directly to the database. |
| Map Service (OpenStreetMap) | The Web Frontend uses OpenStreetMap map tiles through Leaflet. Address geocoding and distance data are provided by the Map Service; distance uses the Haversine formula and may optionally use OSRM road distance. |
| Email provider (SMTP) | The Notification & Reporting Service uses the email provider to send citizens email notifications on request status changes. In-app notifications are presented in the Web Frontend. |

API errors shall use the body `{ "error": { "code": "STRING_CODE", "message": "Readable message" } }`. The API shall use HTTP status codes 200 and 201 for success, 400 for bad input, 401 for unauthenticated requests, 403 for role or permission failures, 404 for missing resources, 409 for conflicts, 422 for validation errors, and 500 for server errors.

### 3.4 Communications

The Web Frontend and backend shall communicate over the Internet using HTTPS with TLS 1.2 or later. REST request and response bodies shall use JSON, and API paths shall use the `/api/v1` base path. Authenticated API requests shall include the JWT bearer token in the `Authorization` header.

The Notification & Reporting Service shall communicate with the external email provider using SMTP to deliver status-change email notifications. The Web Frontend shall display in-app notifications and retrieve application data from the backend API. Map tiles and geocoding data shall be retrieved from OpenStreetMap services via the map interface.

If the map service or email provider is unavailable, map display or email delivery may be degraded; request status tracking and in-app notifications shall continue through the system.
