# 4.2 Sequence Diagram — Route Generation

## 1. Purpose

This document describes the interactions between system components when an administrator generates collection routes for a selected date. It explains authorization, data retrieval, route optimization, and persistence of generated routes.

## 2. Participating Components

- **Admin:** Initiates route generation for a selected date.
- **Web Frontend:** Sends the route-generation request and displays the result.
- **Auth & User Service:** Validates the user's identity and permissions.
- **Route Optimization Engine:** Generates routes using approved requests, vehicle information, facility information, and geographic data.
- **Request Service:** Retrieves approved collection requests.
- **Fleet Service:** Provides available vehicles and their capacities.
- **Facility Service:** Provides disposal facility information.
- **Map Service (OpenStreetMap):** Supports geographic information and map-related operations.
- **Database (PostgreSQL):** Stores and retrieves persistent system records.

## 3. Main Interaction Flow

### Step 1: Route Generation Request

The administrator selects a date and requests route generation through the Web Frontend. The frontend forwards the request for authorization and processing.

### Step 2: Authorization

The Auth & User Service validates the user's identity and role.

- If the user is authorized, the route-generation workflow continues.
- If the user is not authorized, the request is rejected and the frontend displays an access-denied message.

### Step 3: Retrieve Approved Requests

The Route Optimization Engine requests approved collection requests for the selected date from the Request Service. The Request Service retrieves the relevant records from PostgreSQL and returns request details, including locations and priorities.

### Step 4: Retrieve Vehicle Information

The Route Optimization Engine requests available vehicles and their capacities from the Fleet Service. The Fleet Service retrieves the required vehicle records from PostgreSQL and returns the available vehicle information.

### Step 5: Retrieve Disposal Facility Information

The Route Optimization Engine requests suitable disposal facility information from the Facility Service. The Facility Service retrieves facility records from PostgreSQL and returns facility locations and details.

### Step 6: Obtain Geographic Information

The Route Optimization Engine obtains geographic information from the Map Service where required for route planning and distance-related decisions.

### Step 7: Generate Routes

The Route Optimization Engine processes the retrieved information and generates collection routes according to the defined routing rules:

- Uses approved collection requests for the selected date.
- Orders stops by priority and then shortest distance.
- Respects vehicle capacity limits.
- Directs a full vehicle to the nearest suitable disposal facility.

### Step 8: Save Generated Routes

The Route Optimization Engine saves the generated routes and ordered stop information in PostgreSQL. The database returns the persistence result.

### Step 9: Return the Result

The Route Optimization Engine returns the generated routes and ordered stops to the Web Frontend. The frontend displays the route-generation result to the administrator.

## 4. Alternative Flow — Unauthorized User

If authorization fails:

1. The Auth & User Service returns an access-denied result.
2. The Web Frontend receives the authorization failure.
3. The frontend displays an authorization error to the administrator.
4. Route generation does not proceed.

## 5. Preconditions and Postconditions

**Preconditions**
- The administrator is authenticated and authorized to generate routes.
- A route-generation date has been selected.
- Approved collection requests and relevant vehicle and facility information are available in the system.

**Postconditions**
- On success, generated routes and ordered stops are persisted and returned for display.
- On authorization failure, route generation is rejected.
- Generated routes must respect the defined priority, distance, and vehicle-capacity rules.

## 6. Requirements Traceability

- **SCW-F-040:** Generate routes for a date from approved collection requests.
- **SCW-F-041:** Order stops by priority and then shortest distance.
- **SCW-F-042:** Respect vehicle capacity and direct a full vehicle to a suitable disposal facility.
- **SCW-F-043:** Make generated routes available for driver route viewing.
- **SCW-F-044:** Support collection-status updates through the driver workflow.
- **SCW-NF-001:** Meet the specified route-generation performance target.
- **SCW-SEC-003:** Support HTTPS for frontend and service communication.
- **SCW-SEC-006:** Support audit logging through the Auth & User Service.

## 7. Diagram Reference

The corresponding PlantUML source is located at `docs/diagrams/seq-route-generation.puml`.

The rendered sequence diagram is located at `docs/diagrams/seq-route-generation.png`.

## 8. Conclusion

The sequence diagram describes the main route-generation workflow, from the administrator's request and authorization through data retrieval, route optimization, persistence, and presentation of the result. It also represents the alternative flow for an unauthorized user.
## Route Algorithm (Pseudocode)

The route-generation service creates routes from approved collection requests while respecting request priority, travel distance, and vehicle capacity.

```text
INPUT:
    approved_requests
    available_vehicles
    suitable_facilities

FOR each available vehicle:
    remaining_capacity = vehicle.capacity - vehicle.current_load
    current_location = vehicle.start_location
    pending_requests = approved requests eligible for assignment

    SORT pending_requests by priority (highest first)

    WHILE pending_requests is not empty:
        next_request = nearest eligible request
                      among the highest-priority pending requests

        IF next_request would exceed remaining_capacity:
            facility = nearest suitable facility
                       with sufficient remaining capacity

            IF facility exists:
                ADD facility to route
                UPDATE current_location to facility.location
                UPDATE vehicle load and remaining capacity
                CONTINUE route planning
            ELSE:
                STOP route planning before vehicle capacity is exceeded
                ALERT administrator that no suitable facility is available
                BREAK

        ADD next_request to route
        UPDATE current_location to next_request.location
        UPDATE remaining_capacity
        REMOVE next_request from pending_requests

    SAVE the valid route and its ordered stops

OUTPUT:
    generated routes and any required administrator alerts
```

**Algorithm notes:**
- Request priority is considered before distance; nearest-next selection is applied among eligible requests at the highest priority.
- Vehicle capacity is checked before assigning a collection that could exceed the limit.
- A facility detour is permitted only when a suitable facility has sufficient remaining capacity.
- If no suitable facility is available, route planning stops safely and the administrator is alerted.