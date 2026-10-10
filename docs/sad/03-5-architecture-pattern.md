# 3.5 Architecture Pattern

## 1. Selected Architecture Pattern

The Smart City Waste Management System follows a **Layered Architecture (Three-Tier Architecture)**. The system separates presentation, application logic, and data storage into distinct layers. This separation improves modularity, maintainability, testing, and the ability to develop components independently.

## 2. Architecture Layers

### 2.1 Presentation Layer

**Component:** Web Frontend

The Presentation Layer provides the user interface for citizens, drivers, administrators, municipal officers, and disposal facility operators.

Responsibilities:
- Accepts user input and displays system information.
- Allows citizens to submit and track waste collection requests.
- Enables administrators to manage requests and generate routes.
- Allows drivers to view assigned routes and update collection outcomes.
- Displays collection routes and locations on a map.

The frontend communicates with backend services through APIs and does not directly access the database.

### 2.2 Application / Service Layer

**Components:** Auth & User Service, Request Service, Fleet Service, Facility Service, Route Optimization Engine, and Notification & Reporting Service.

This layer implements the system's business rules and application workflows.

Responsibilities:
- Authenticates users and enforces authorization.
- Manages collection requests and approval workflows.
- Maintains vehicle and facility information.
- Generates routes using approved requests, priorities, vehicle capacities, and geographic information.
- Supports driver collection updates and related status changes.
- Provides notifications and reporting functionality.

Separating these responsibilities into components makes the application easier to maintain, test, and extend.

### 2.3 Data Layer

**Component:** Database (PostgreSQL)

The Data Layer provides persistent storage for system information.

Responsibilities:
- Stores user, request, vehicle, facility, route, and collection-status records.
- Supports data retrieval and updates requested by application services.
- Maintains consistent information for the system's operations.

Application services access persistent data through controlled database operations. The Web Frontend does not directly access PostgreSQL.

### 2.4 External Map Service

**Component:** Map Service (OpenStreetMap)

The system integrates with OpenStreetMap for geographic visualization and map-related information.

Responsibilities:
- Displays collection locations and ordered route stops.
- Provides map resources for the frontend.
- Supports route-related geographic information where required.

The Map Service is an external dependency rather than an internal business layer.

## 3. Architectural Interaction

The typical interaction flow is:

1. A user performs an action through the Web Frontend.
2. The frontend sends a request to the relevant backend service.
3. The service validates the request, applies business rules, and accesses the database when necessary.
4. The service returns a response to the frontend.
5. The frontend displays the result to the user.

For route generation, the Route Optimization Engine receives approved collection requests, vehicle information, and facility information. It generates ordered stops while considering priority and vehicle capacity. The generated route is then made available for driver use.

## 4. Rationale for Selecting Layered Architecture

The layered architecture is suitable for the Smart City Waste Management System for the following reasons:

- **Separation of concerns:** User interfaces, business logic, and persistent storage have distinct responsibilities.
- **Maintainability:** Changes to one layer can often be made without requiring major changes to the other layers, provided their interfaces remain stable.
- **Testability:** Backend services can be tested independently using unit tests and suitable test doubles.
- **Modularity:** Authentication, request management, fleet management, facility management, and route generation have separate responsibilities.
- **Security:** Backend services can enforce authentication, authorization, and validation before performing operations.
- **Extensibility:** New features can be added by extending the relevant service or frontend component.
- **Data management:** PostgreSQL provides a centralized persistent data layer for system records.

## 5. Limitations and Design Considerations

- Communication between the frontend and backend services introduces API and network overhead.
- The system must define clear interfaces between services to reduce tight coupling.
- Database availability and performance can affect multiple application functions.
- Route generation depends on accurate request locations, vehicle capacities, facility information, and suitable routing logic.
- External map service availability and usage constraints must be considered.

These limitations can be addressed through service-layer testing, input validation, error handling, performance testing, and clear interface contracts.

## 6. Requirements Traceability

The architecture supports the following requirements:

- **SCW-F-040:** Generating routes from approved collection requests.
- **SCW-F-041:** Ordering stops by priority and shortest distance.
- **SCW-F-042:** Respecting vehicle capacity and selecting a suitable facility when a vehicle is full.
- **SCW-F-043:** Displaying assigned routes and ordered stops for drivers.
- **SCW-F-044:** Updating request status based on collection outcomes.
- **SCW-NF-001:** Meeting the route-generation performance target.
- **SCW-NF-002:** Meeting the API response-time target.
- **SCW-NF-003:** Meeting the system availability target.
- **SCW-NF-005:** Supporting modular services and the required service-layer test coverage.
- **SCW-SEC-003:** Supporting HTTPS.
- **SCW-SEC-006:** Supporting audit logging through the Auth & User Service.

The detailed requirement definitions and component mappings remain governed by the project's requirements registry and SAD traceability document.

## 7. Conclusion

The Three-Tier Layered Architecture provides a clear separation between presentation, application services, and data storage. Combined with modular backend components and an external map integration, it provides a maintainable foundation for the Smart City Waste Management System.