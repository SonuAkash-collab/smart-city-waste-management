# 3.3 Component Diagram

## Purpose

The component diagram presents the high-level structure of the Smart City Waste Management System. It shows the system's main components, their responsibilities at a structural level, the external actors that interact with the system, and the dependencies between components.

The diagram is maintained in PlantUML format at `docs/diagrams/component-diagram.puml`. Its rendered image is available at `docs/diagrams/component-diagram.png`.

## Architecture Overview

The system is organized into a presentation layer, an application/service layer, and a data layer. An external map service supports location-related operations and map display.

### 1. Presentation Layer

The **Web Frontend** provides the user interface for Citizens, Drivers, Admin / Municipal Officers, and Disposal Facility Operators. It allows users to access the functions permitted by their roles, including submitting collection requests, managing vehicles and facilities, generating routes, viewing assigned routes, and accessing reports.

### 2. Application / Service Layer

The application/service layer contains the following components:

- **Auth & User Service:** Manages authentication, user roles, access control, and audit logging.
- **Request Service:** Manages waste collection requests, their priorities, and request status changes.
- **Fleet Service:** Manages collection vehicles, driver assignments, vehicle availability, and capacity information.
- **Facility Service:** Manages disposal facilities, accepted waste types, and remaining facility capacity.
- **Route Optimization Engine:** Generates collection routes, orders stops, considers vehicle capacity, and selects suitable disposal facilities.
- **Notification & Reporting Service:** Supports status-change notifications, administrative dashboards, and daily collection reports.

These components collaborate to implement the functional requirements assigned to them in the requirements traceability document.

### 3. Data Layer

**Database (PostgreSQL)** provides persistent storage for user information, collection requests, vehicle records, facility information, routes, stop statuses, and audit records.

The application services access the database to retrieve and update the information required for their operations.

### 4. External Map Service

**Map Service (OpenStreetMap)** supports location lookup, geographic distance calculations, and map display. It assists the Request Service, Facility Service, Route Optimization Engine, and Web Frontend where geographic information is required.

## Main Component Interactions

1. Users interact with the Web Frontend to access authorized system functions.
2. The Web Frontend communicates with the appropriate application services to process requests.
3. The Route Optimization Engine obtains approved requests, vehicle information, and facility information from the relevant services to generate routes.
4. The Route Optimization Engine uses geographic information to order collection stops and identify suitable disposal facilities.
5. The Request Service and Route Optimization Engine communicate status changes to the Notification & Reporting Service.
6. Application services use PostgreSQL to persist and retrieve system data.
7. Drivers use the Web Frontend to view assigned routes and update collection-stop statuses.

## Security and Quality Considerations

- **SCW-SEC-003:** HTTPS using TLS 1.2 or higher protects traffic between the Web Frontend and the services.
- **SCW-SEC-006:** The Auth & User Service is the primary component responsible for recording administrative actions in the audit log, with supporting services providing relevant action details.
- **SCW-NF-002:** The API response-time target applies across all services.
- **SCW-NF-003:** The monthly availability target applies across all services.
- **SCW-NF-005:** The modularity and service-layer unit-test coverage requirement applies across all services.
- **SCW-SO-2:** Integrity and accountability of request, route, and facility data apply across all services.

## Traceability

The component diagram follows the component names and responsibility mappings defined in `docs/sad/03-8-traceability.md`. Requirement IDs are not redefined in this section; the requirements registry and traceability document remain the authoritative references.