# Test Plan

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 6. Test Environment

### 6.1 Hardware

Client testing uses desktop, tablet and mobile devices with Internet connectivity and a supported web browser. The Web Frontend supports screens at least 360 px wide and standard keyboard, pointer and touch input. No dedicated peripherals or vehicle GPS hardware are required for testing.

The server hardware profile, including CPU, memory and storage, is not specified. The operating environment allows a Linux server or cloud VM; the exact host and resource allocation require team confirmation.

### 6.2 Software

| Environment component | Documented configuration |
|---|---|
| Web Frontend | React, accessed through current versions of Chrome, Firefox, Edge or Safari on desktop, Android or iOS. |
| Backend | Python 3.11 or later with FastAPI and the Uvicorn ASGI server, on a Linux server or cloud VM. |
| Database | PostgreSQL 15 or later for persistent application data. |
| Client-server communications | REST/JSON under `/api/v1`, over HTTPS with TLS 1.2 or later. Authenticated requests use a JWT bearer token in the `Authorization` header. |
| Request Service API | The endpoints and examples in SAD §4.3 are used for Request Service API checks, including the documented request fields, filters, roles, responses and status codes. |

Exact framework, library and browser release versions beyond the minimum or "current versions" stated above are not specified.

### 6.3 Test Tools

The project identifies the following tools for test execution and management:

- **Pytest** for Python unit and integration tests.
- **Postman** and **Swagger** (FastAPI auto-docs) for REST API inspection and testing.
- **Selenium or Playwright** for browser-based checks.
- **Locust or JMeter** for load and performance testing.
- **GitHub Issues** for recording failed test cases and tracking defects.

The specific browser automation and load-testing tools to be used for a test cycle have not been selected.

### 6.4 Database and Test Data

The test environment uses PostgreSQL 15 or later. Test data shall support the scenarios in the registered test cases and SRS acceptance criteria. The performance test workload is defined as 200 requests and 20 vehicles for route generation, and 100 concurrent users for API response-time testing.

The test-data dataset, account setup, database initialization and reset procedure, and whether test databases are isolated between test runs are not specified; the team must confirm them before execution.

### 6.5 Interfaces and External Services

- The Web Frontend runs in the browser and communicates with the FastAPI services using the documented REST/JSON API.
- Backend services use PostgreSQL for persistent application data; the browser does not connect directly to the database.
- The map interface uses Leaflet with OpenStreetMap map tiles and geocoding services. Distance calculations use Haversine distance and may optionally use OSRM road distance.
- The Notification & Reporting Service uses an external SMTP email provider for status-change emails. In-app notifications are handled through the system.

OpenStreetMap and the email provider are external systems; their internals are not tested. The Test Plan permits replacing them with stubs or using them as-is. The choice for each test cycle, along with required service endpoints and configuration, requires team confirmation.

### 6.6 Environment Setup

For each test cycle, the version under test is a build of the `main` branch tagged for that cycle. Record the commit hash in the test run report. Run the application with the documented client, backend and database software, and configure the client-server connection to use HTTPS and the `/api/v1` API conventions.

Deployment instructions, environment-specific API base URLs, TLS certificate setup, service credentials, secrets handling, and exact external-service configuration are not defined in the project documents. The team must confirm and provision these settings without placing credentials in the test plan.
