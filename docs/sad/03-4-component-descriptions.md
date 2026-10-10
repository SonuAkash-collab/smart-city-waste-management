# 3.4 Component Descriptions

## 1. Purpose

This section describes the responsibilities, interfaces, inputs, outputs, and interactions of the major components in the Smart City Waste Management System. The descriptions follow the component diagram and the system's three-tier architecture.

## 2. Web Frontend

**Layer:** Presentation Layer

**Responsibilities:**
- Provides user interfaces for citizens, drivers, administrators, municipal officers, and disposal facility operators.
- Allows citizens to submit and track waste collection requests.
- Allows administrators to manage requests, vehicles, facilities, and route generation.
- Allows drivers to view assigned routes and update collection status.
- Displays route information on a map.

**Inputs:** User actions, form data, route information, and API responses.

**Outputs:** API requests to backend services and information displayed to users.

**Interactions:** Communicates with the backend services through HTTPS.

## 3. Auth & User Service

**Layer:** Application / Service Layer

**Responsibilities:**
- Handles user authentication and authorization.
- Manages user accounts and role-based access.
- Restricts operations according to user roles and permissions.
- Maintains audit records of relevant security-sensitive activities.

**Inputs:** Login credentials, user information, access requests, and audit events.

**Outputs:** Authentication results, authorization decisions, user information, and audit records.

**Interactions:** Supports the Web Frontend and other services that require authenticated user identity and permissions.

**Traceability:** SCW-SEC-006 identifies this service as the primary component for audit logging. HTTPS support is covered by SCW-SEC-003.

## 4. Request Service

**Layer:** Application / Service Layer

**Responsibilities:**
- Creates and manages waste collection requests.
- Maintains request details, including location, waste information, and status.
- Supports the request approval workflow.
- Provides approved requests to the Route Optimization Engine.
- Updates request status when collection results are recorded.

**Inputs:** Citizen submissions, administrator approval actions, and driver collection updates.

**Outputs:** Request records, approval status, and updated collection status.

**Interactions:** Communicates with the Web Frontend, Auth & User Service, Route Optimization Engine, and Database.

## 5. Fleet Service

**Layer:** Application / Service Layer

**Responsibilities:**
- Maintains vehicle information and availability.
- Provides vehicle capacity and related details for route generation.
- Supports the assignment of vehicles to collection routes.

**Inputs:** Vehicle details, availability information, and route assignment requests.

**Outputs:** Vehicle records, capacity information, and vehicle assignment data.

**Interactions:** Communicates with the Web Frontend, Route Optimization Engine, and Database.

## 6. Facility Service

**Layer:** Application / Service Layer

**Responsibilities:**
- Maintains disposal facility information and locations.
- Provides facility details needed when a vehicle reaches its load capacity.
- Supports the selection of a suitable facility for disposal.

**Inputs:** Facility information, locations, and facility-selection requests.

**Outputs:** Facility records and suitable facility details.

**Interactions:** Communicates with the Web Frontend, Route Optimization Engine, and Database.

## 7. Route Optimization Engine

**Layer:** Application / Service Layer

**Responsibilities:**
- Generates collection routes for a selected date using approved requests.
- Orders stops according to priority and then shortest distance.
- Considers vehicle capacity when assigning stops.
- Directs a full vehicle to the nearest suitable disposal facility.
- Produces ordered stops for drivers to follow.

**Inputs:** Approved collection requests, request priorities, locations, vehicle availability and capacity, and disposal facility information.

**Outputs:** Generated routes, ordered stops, vehicle assignments, and facility destinations when required.

**Interactions:** Communicates with the Request Service, Fleet Service, Facility Service, Map Service, Database, and Web Frontend.

**Traceability:** Implements SCW-F-040, SCW-F-041, SCW-F-042, SCW-F-043, and SCW-F-044 as applicable to route generation and its integration with driver operations. Its performance requirement is SCW-NF-001.

## 8. Notification & Reporting Service

**Layer:** Application / Service Layer

**Responsibilities:**
- Supports notifications related to request and collection status changes.
- Provides reporting information for authorized users.
- Helps communicate relevant system updates to users.

**Inputs:** Request status changes, collection outcomes, and reporting queries.

**Outputs:** Notifications and report data.

**Interactions:** Communicates with the Request Service, Web Frontend, and Database as required.

## 9. Map Service (OpenStreetMap)

**Type:** External Map Service

**Responsibilities:**
- Supplies map information for displaying collection locations and routes.
- Supports the visualization of ordered route stops.
- Provides map-related geographic information used by the application.

**Inputs:** Geographic locations and map requests.

**Outputs:** Map data and geographic visualization resources.

**Interactions:** Used by the Web Frontend and Route Optimization Engine where map-related information is required.

**Dependency:** Uses OpenStreetMap as the external mapping service.

## 10. Database (PostgreSQL)

**Layer:** Data Layer

**Responsibilities:**
- Stores persistent application data.
- Maintains user, request, vehicle, facility, route, and collection-status records.
- Supports data retrieval and updates initiated by backend services.

**Inputs:** Data creation, update, and retrieval operations from application services.

**Outputs:** Stored records and query results.

**Interactions:** Provides persistent storage for the application and service layer.

## 11. Cross-Cutting Quality Requirements

The following requirements apply across the relevant system components:

- **SCW-SEC-003 — HTTPS:** The Web Frontend is the primary component, with support required across all services.
- **SCW-SEC-006 — Audit logging:** Auth & User Service is the primary component for audit logging.
- **SCW-NF-002 — API performance:** Applies to all services.
- **SCW-NF-003 — Availability:** Applies to all services.
- **SCW-NF-005 — Modularity and test coverage:** Applies to all services.
- **SCW-SO-2:** Applies to all services, as specified in the system architecture traceability document.

## 12. Summary

The Smart City Waste Management System follows a three-tier architecture consisting of the Presentation Layer, Application / Service Layer, and Data Layer, with OpenStreetMap as an external service. The separation of responsibilities supports maintainability, testing, and independent development of system components.