# Software Architecture & Design

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 4.3 API Design — Request Service

The Request Service exposes REST endpoints under `/api/v1`. Requests and responses use JSON. Authenticated API requests use a JWT bearer token in the `Authorization` header. Server-side role checks apply to every API call (SCW-SEC-004); the SRS identifies Citizen and Admin / Municipal Officer access for the operations below but does not define a complete endpoint-by-endpoint permission matrix.

API errors use the documented body shape:

```json
{
  "error": {
    "code": "STRING_CODE",
    "message": "Readable message"
  }
}
```

The documented HTTP status conventions are 200 and 201 for success, 400 for bad input, 401 for unauthenticated requests, 403 for role or permission failures, 404 for missing resources, 409 for conflicts, 422 for validation errors, and 500 for server errors. The SRS specifies particular outcomes below; it does not assign every listed error status to every endpoint.

### Request Service Endpoints

#### Submit a Collection Request

| Field | Definition |
|---|---|
| Endpoint | `/api/v1/requests` |
| Method | `POST` |
| Request | JSON request containing location (map pin or address), waste type and estimated quantity; an optional photo may also be supplied. The photo's representation and transfer mechanism are unspecified. Authenticated access follows the JWT bearer convention. |
| Response | HTTP 201 when the request is accepted and stored. When supplied, the optional photo is associated with the stored request. The response body schema is not specified. |
| Errors | If location is missing, HTTP 422. Other applicable API errors follow the documented common conventions; endpoint-specific error bodies beyond the common shape are unspecified. |

On successful submission, the Request Service assigns priority under SCW-F-011 and the request enters the Submitted status. Status-change notification behavior is specified by SCW-F-050; notification delivery is handled by the Notification & Reporting Service.

#### List Collection Requests

| Field | Definition |
|---|---|
| Endpoint | `/api/v1/requests` |
| Method | `GET` |
| Request | Optional filtering by status, priority, waste type and date. Exact query parameter names and value formats are unspecified. Admin / Municipal Officer access is specified for viewing and filtering requests. |
| Response | HTTP 200 on success. Returns requests matching the selected filter criteria. The response body schema and pagination behavior are unspecified. |
| Errors | Applicable API errors follow the documented common conventions. Endpoint-specific error conditions and response bodies are unspecified. |

#### Retrieve a Collection Request

| Field | Definition |
|---|---|
| Endpoint | `/api/v1/requests/{id}` |
| Method | `GET` |
| Request | The request identifier in the path. A Citizen may retrieve their request; authenticated access follows the JWT bearer convention. |
| Response | HTTP 200 on success. The returned request includes its current stored status; for SCW-F-011, an Admin priority override is saved and returned by this endpoint. The complete response body schema is unspecified. |
| Errors | Applicable API errors follow the documented common conventions. A missing-resource response uses HTTP 404 under those conventions. |

The supported request statuses are Submitted, Approved, Scheduled, Collected, Rejected, Missed and Cancelled (SCW-F-012). The SRS specifies status tracking through this endpoint but does not define a complete status-update response schema.

#### Update Request Status

| Field | Definition |
|---|---|
| Endpoint | `/api/v1/requests/{id}/status` |
| Method | `PATCH` |
| Request | The request identifier in the path and a status update. The request body property names and schema are unspecified. Admin / Municipal Officer uses this endpoint to approve or reject requests. |
| Response | HTTP 200 on success, following the general success convention. The updated status is returned by subsequent request retrieval. A response body schema for this endpoint is unspecified. |
| Errors | Applicable API errors follow the documented common conventions, including HTTP 404 for a missing resource and HTTP 409 for a documented status conflict. Exact endpoint-specific conflict conditions beyond cancellation are unspecified. |

This endpoint participates in status updates covered by SCW-F-012. Approval and rejection depend on SCW-F-014; Scheduled, Collected and Missed updates also depend on route generation and stop updates (SCW-F-040 and SCW-F-044). Administrative approval and rejection are written to the audit log (SCW-SEC-006). Any status change triggers the notification behavior specified by SCW-F-050.

#### Cancel a Collection Request

| Field | Definition |
|---|---|
| Endpoint | `/api/v1/requests/{id}` |
| Method | `DELETE` |
| Request | The request identifier in the path. The Citizen may cancel the request only before its status becomes Scheduled (SCW-F-013). |
| Response | HTTP 200 when cancellation succeeds; the request status becomes Cancelled. |
| Errors | HTTP 409 when the request is Scheduled or later; its status remains unchanged. Other applicable API errors follow the documented common conventions. |

Successful cancellation is a status change and is covered by SCW-F-050 notification behavior.

### Priority Assignment

The Request Service assigns priority from the request's waste type and age (SCW-F-011):

| Waste type | Assigned priority |
|---|---|
| Hazardous / medical / e-waste | High |
| Mixed / general / recyclable | Medium |
| Garden / bulky | Low |

A request remaining in Submitted or Approved after 48 hours increases by one priority level, capped at High. An Admin / Municipal Officer may override the priority. The overridden value is returned by `GET /api/v1/requests/{id}`. The SRS does not specify a dedicated priority-update endpoint or the exact request body for an override.

### Open API Specifications

The project documents do not define complete JSON request or response schemas, the optional photo's representation and transfer mechanism, the `GET /requests` filter parameter names and value formats, pagination, or the request body for status updates and priority overrides. They also do not define a complete endpoint-by-endpoint role permission matrix or all status-conflict conditions for `PATCH /requests/{id}/status`. These details require project-team confirmation; this section does not assume them.
