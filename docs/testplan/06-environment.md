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

Working assumption: use an available test host capable of running the Web Frontend, FastAPI services, and PostgreSQL. No particular server hardware profile, operating system, or hosting platform is required by the project documents.

### 6.2 Software

| Environment component | Documented configuration |
|---|---|
| Web Frontend | React, accessed through current versions of Chrome, Firefox, Edge or Safari on desktop, Android or iOS; test screens include widths of at least 360 px. |
| Backend | Python FastAPI services. |
| Database | PostgreSQL for persistent application data. |
| Client-server communications | REST/JSON under `/api/v1`, over HTTPS with TLS 1.2 or later. Authenticated requests use a JWT bearer token in the `Authorization` header. |
| Request Service API | Use the endpoints and contract in SAD §4.3 for Request Service checks, including documented request fields, filters, roles, responses and status codes. Configure the test client with the API base URL for the test environment; no specific host or URL is prescribed here. |

The project does not prescribe language-runtime, framework, database, or browser release numbers beyond the browser scope stated above; do not treat particular version numbers as test-environment requirements.

### 6.3 Test Tools

The project identifies the following tools for test execution and management:

- **Pytest** for Python unit and integration tests.
- **Postman** and **Swagger** (FastAPI auto-docs) for REST API inspection and testing.
- **Selenium or Playwright** for browser-based checks.
- **Locust or JMeter** for load and performance testing.
- **GitHub Issues** for recording failed test cases and tracking defects.

Working assumption: use the listed tool appropriate to each test activity; where alternatives are listed, select one that is available for the test cycle and record it in the test results. The project does not mandate a particular browser automation or load-testing tool.

### 6.4 Database and Test Data

The test environment uses PostgreSQL. Test data shall support the registered test cases and SRS acceptance criteria. The performance test workload is 200 approved requests and 20 vehicles for route generation (SCW-NF-001), and 100 concurrent users for API response-time testing (SCW-NF-002). Test accounts shall have only the roles needed for the scenarios under test; account identities and credentials are supplied through the test setup and are not specified in this plan.

Working assumption: use test data in a test database separate from production data, and initialize or reset records when required to establish a test case's documented preconditions. No specific dataset, account credentials, database initialization command, or reset procedure is prescribed.

### 6.5 Interfaces and External Services

- The Web Frontend runs in the browser and communicates with the FastAPI services using the documented REST/JSON API.
- Backend services use PostgreSQL for persistent application data; the browser does not connect directly to the database.
- The map interface uses Leaflet with OpenStreetMap map tiles and geocoding services. Distance calculations use Haversine distance and may optionally use OSRM road distance.
- The Notification & Reporting Service uses an external SMTP email provider for status-change emails. In-app notifications are handled through the system.

OpenStreetMap and the email provider are external dependencies; their internal services are outside the system test scope. Working assumption: use controlled substitutes for isolated tests when external integration is not under test; use the configured external service for integration checks when it is available. The test setup supplies any required service configuration without recording endpoint values or credentials in this plan. If the map service or email provider is unavailable, record the resulting degradation separately from application behavior; request status tracking and in-app notifications shall continue.

### 6.6 Environment Setup

For each test cycle, run the selected application build with the documented Web Frontend, FastAPI services, and PostgreSQL. Configure client-server communication for HTTPS with TLS 1.2 or later and the `/api/v1` REST/JSON conventions. Working assumption: record the source revision or commit hash for each tested build in the test run report.

The project documents do not prescribe deployment instructions, an environment-specific API base URL, TLS certificate provisioning, or external-service configuration. Supply these through the selected test environment; keep credentials and other secrets out of this plan and test results.
