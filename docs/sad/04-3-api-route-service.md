# 4.3 API — Route Service

## 1. Purpose

This document defines the proposed API contract for route generation and route retrieval in the Smart City Waste Management System. The API enables authorized administrators to generate collection routes and allows drivers to retrieve their assigned routes.

The API is exposed through the backend and communicates with the application services and PostgreSQL database.

## 2. Base URL

The API base URL depends on the deployment environment.

```text
/api
```

All endpoints must be served over HTTPS in deployed environments.

## 3. Route Generation API

### 3.1 Generate Routes

**Endpoint:** `POST /api/routes/generate`

**Purpose:** Generates collection routes for a selected date using approved collection requests, available vehicles, vehicle capacities, and suitable disposal facilities.

**Authorized role:** Administrator or another explicitly authorized municipal role.

**Request headers:**

```http
Content-Type: application/json
Authorization: Bearer <access_token>
```

**Example request body:**

```json
{
  "date": "2026-10-10"
}
```

**Processing:**
1. Authenticate the user and verify route-generation permission.
2. Retrieve approved collection requests for the selected date.
3. Retrieve available vehicles and their capacities.
4. Retrieve suitable disposal facility information.
5. Obtain geographic information as required.
6. Generate routes using the defined priority, distance, and capacity rules.
7. Persist generated routes and ordered stops.
8. Return the result to the frontend.

**Example successful response:**

```json
{
  "success": true,
  "date": "2026-10-10",
  "routes": [
    {
      "route_id": "route-example-001",
      "vehicle_id": "vehicle-example-001",
      "stops": [
        {
          "sequence": 1,
          "request_id": "request-example-001",
          "location": {
            "latitude": 12.9716,
            "longitude": 77.5946
          },
          "status": "Pending"
        }
      ]
    }
  ],
  "message": "Routes generated successfully"
}
```

The identifiers and location values above are illustrative examples. Actual response fields and identifier formats must match the implementation.

## 4. Driver Route Retrieval API

### 4.1 Retrieve Assigned Routes

**Endpoint:** `GET /api/routes/assigned`

**Purpose:** Retrieves routes assigned to the authenticated driver.

**Authorized role:** Driver.

**Request headers:**

```http
Authorization: Bearer <access_token>
```

**Example successful response:**

```json
{
  "success": true,
  "routes": [
    {
      "route_id": "route-example-001",
      "date": "2026-10-10",
      "stops": [
        {
          "sequence": 1,
          "request_id": "request-example-001",
          "status": "Pending"
        }
      ]
    }
  ]
}
```

The backend must restrict results to routes the authenticated driver is permitted to access.

## 5. Route Stop Status API

### 5.1 Update Collection Outcome

**Endpoint:** `PATCH /api/routes/{route_id}/stops/{request_id}/status`

**Purpose:** Records whether a collection stop was completed or missed.

**Authorized role:** Driver assigned to the relevant route, subject to the system's authorization rules.

**Example request body:**

```json
{
  "status": "Collected"
}
```

The accepted status values are `Collected` and `Missed`.

**Expected behavior:**
- Verify that the driver is authorized to update the stop.
- Validate the requested status.
- Persist the collection outcome.
- Update the associated request status according to the defined business rules.
- Return the updated status.

**Example successful response:**

```json
{
  "success": true,
  "route_id": "route-example-001",
  "request_id": "request-example-001",
  "status": "Collected"
}
```

## 6. Validation and Error Handling

The API should handle the following conditions consistently:

| HTTP status | Condition |
|---|---|
| `200 OK` | A retrieval or update operation succeeds. |
| `201 Created` | A new resource is created, if the implementation uses this response. |
| `400 Bad Request` | The request contains invalid data. |
| `401 Unauthorized` | Authentication is missing or invalid. |
| `403 Forbidden` | The user lacks the required permission. |
| `404 Not Found` | The requested route, stop, or resource does not exist. |
| `409 Conflict` | A request conflicts with the current resource state. |
| `422 Unprocessable Entity` | Request validation fails, where used by the framework. |
| `500 Internal Server Error` | An unexpected server error occurs. |

Error responses should provide a consistent, useful message without exposing credentials, sensitive data, or internal implementation details.

## 7. Security Considerations

- Require authentication for protected endpoints.
- Enforce role-based authorization for route generation and driver operations.
- Use HTTPS in deployed environments.
- Validate and constrain all client-supplied data.
- Prevent drivers from viewing or modifying routes assigned to other drivers.
- Record relevant security-sensitive actions in the audit log.
- Avoid returning unnecessary personal or sensitive information in API responses.

## 8. Performance Considerations

Route generation must satisfy **SCW-NF-001**, which specifies a maximum target of 10 seconds for 200 requests and 20 vehicles.

API response performance must satisfy **SCW-NF-002**, which specifies that 95% of API responses complete within 2 seconds under 100 concurrent users.

These targets must be verified through performance testing; defining the API alone does not establish compliance.

## 9. Requirements Traceability

- **SCW-F-040:** Generate routes for a date from approved requests.
- **SCW-F-041:** Order stops by priority and then shortest distance.
- **SCW-F-042:** Respect vehicle capacity and route full vehicles to a suitable facility.
- **SCW-F-043:** Make assigned routes available to drivers as ordered stops on a map.
- **SCW-F-044:** Allow drivers to mark stops as Collected or Missed and update request status.
- **SCW-NF-001:** Meet the route-generation performance target.
- **SCW-NF-002:** Meet the API response-time target.
- **SCW-SEC-003:** Support HTTPS.
- **SCW-SEC-006:** Support audit logging through the Auth & User Service.

## 10. Implementation Note

The endpoint paths, payload schemas, response fields, and HTTP status codes in this document are proposed interface contracts. Before implementation or final submission, verify them against the actual backend routes and the team's agreed API conventions. Update this document if the implementation differs.