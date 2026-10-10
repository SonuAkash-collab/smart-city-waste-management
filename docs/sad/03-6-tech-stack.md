# 3.6 Technology Stack

## 1. Overview

The Smart City Waste Management System uses a technology stack consisting of a web frontend, backend API, relational database, mapping libraries, and a route-optimization algorithm. These technologies support citizen requests, administrative operations, vehicle routing, and driver collection workflows.

## 2. Frontend Technologies

### 2.1 React

**Purpose:** Web user interface development.

React is used to build a component-based web interface for citizens, drivers, administrators, municipal officers, and disposal facility operators.

**Responsibilities:**
- Displays pages, forms, dashboards, and request information.
- Supports waste collection request submission and tracking.
- Displays assigned routes and collection status.
- Communicates with backend APIs.

**Selection rationale:** React supports reusable UI components and helps keep presentation logic separate from backend business logic.

### 2.2 Leaflet

**Purpose:** Interactive maps in the web interface.

Leaflet is used to display geographic locations and collection routes.

**Responsibilities:**
- Displays collection points and route stops.
- Supports map interactions and geographic visualization.
- Helps drivers understand the sequence and locations of assigned stops.

**Selection rationale:** Leaflet provides a lightweight way to integrate interactive maps into a web application.

## 3. Backend Technologies

### 3.1 Python

**Purpose:** Backend implementation and route-optimization logic.

Python is used to implement application services and the route-generation algorithm.

**Responsibilities:**
- Implements business rules and application workflows.
- Processes approved collection requests and vehicle information.
- Supports route generation and related validation.
- Provides integration between backend services and the database.

**Selection rationale:** Python supports readable application code and provides libraries suitable for data processing and algorithm implementation.

### 3.2 FastAPI

**Purpose:** Backend API development.

FastAPI exposes endpoints through which the frontend communicates with backend services.

**Responsibilities:**
- Receives and validates API requests.
- Exposes operations for request management and route generation.
- Returns structured responses to the frontend.
- Supports integration between application components.

**Selection rationale:** FastAPI supports structured API development, request validation, and automatic API documentation.

## 4. Database Technology

### 4.1 PostgreSQL

**Purpose:** Persistent relational data storage.

PostgreSQL stores the system's operational records.

**Responsibilities:**
- Stores user and request information.
- Maintains vehicle and disposal facility records.
- Stores route assignments and collection-status information.
- Supports querying and updating application data.

**Selection rationale:** PostgreSQL provides relational data management, transaction support, and constraints that help maintain data consistency.

## 5. Mapping Data Source

### 5.1 OpenStreetMap

**Purpose:** Geographic map data.

OpenStreetMap provides map data used to display locations and collection routes.

**Responsibilities:**
- Supplies geographic map information.
- Supports the visualization of collection locations.
- Provides a mapping data source for the Leaflet-based interface.

**Selection rationale:** OpenStreetMap provides openly available geographic data. The application must comply with applicable attribution requirements and the usage policies of its selected map-data provider.

## 6. Route-Optimization Approach

### 6.1 Greedy Heuristic

**Purpose:** Generate practical collection routes.

The system uses a greedy route-optimization heuristic to select and order collection stops based on the requirements and available information.

**Responsibilities:**
- Considers approved collection requests.
- Prioritizes stops according to the defined priority and distance rules.
- Considers vehicle capacity.
- Selects a suitable disposal facility when a vehicle reaches its capacity.

**Selection rationale:** A greedy heuristic is comparatively straightforward to implement and evaluate. Its performance must be measured against the route-generation requirements.

**Limitation:** A greedy heuristic does not guarantee a globally optimal route. Its results depend on the selection rules, input data, and implementation.

## 7. Technology Integration

The technologies work together as follows:

1. React provides the user interface.
2. Leaflet and OpenStreetMap support map visualization.
3. The frontend communicates with backend endpoints exposed by FastAPI.
4. Python implements the application logic and route-generation heuristic.
5. PostgreSQL stores and retrieves persistent application data.
6. The backend returns request and route information for presentation in the frontend.

## 8. Requirements and Quality Considerations

The selected stack supports the architecture and the following quality objectives:

- **SCW-F-040 to SCW-F-044:** Supports route generation, stop ordering, vehicle capacity handling, driver route viewing, and collection-status updates.
- **SCW-NF-001:** Route generation must meet the specified performance target.
- **SCW-NF-002:** APIs must meet the specified response-time target.
- **SCW-NF-003:** The system must meet the specified availability target.
- **SCW-NF-005:** Services must remain modular and meet the specified service-layer test-coverage target.
- **SCW-SEC-003:** HTTPS must be supported.
- **SCW-SEC-006:** Audit logging must be supported by the designated component.

The technology choices alone do not guarantee these targets. Implementation, testing, configuration, and deployment must demonstrate compliance.

## 9. Conclusion

React, FastAPI, Python, PostgreSQL, Leaflet, OpenStreetMap, and a greedy route-optimization heuristic form the proposed technology stack for the Smart City Waste Management System. Together, they support the web interface, backend operations, persistent storage, map visualization, and waste collection route generation.