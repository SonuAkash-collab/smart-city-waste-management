# Software Architecture & Design

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 4.3 API Design — Request Service

The Request Service provides REST endpoints under `/api/v1`. Requests and responses use JSON. Authenticated requests use a JWT bearer token in the `Authorization` header. API errors use `{"error":{"code":"STRING_CODE","message":"Readable message"}}`.

### POST `/api/v1/requests`

**Role:** Citizen, for their own requests.

**Request:**

```json
{"latitude":12.97,"longitude":77.59,"address":"...","wasteType":"HAZARDOUS|MEDICAL|E_WASTE|MIXED|RECYCLABLE|GARDEN|BULKY","estimatedQuantityKg":25,"photo":"<base64, optional>"}
```

**Response — HTTP 201:**

```json
{"id":101,"status":"SUBMITTED","priority":"HIGH","createdAt":"2026-10-10T10:00:00Z"}
```

**Errors:** HTTP 401 and HTTP 422, using:

```json
{"error":{"code":"LOCATION_REQUIRED","message":"..."}}
```

Location is required; the photo is optional (SCW-F-010). The Request Service assigns priority from waste type and request age (SCW-F-011).

### GET `/api/v1/requests?status=APPROVED&priority=HIGH&wasteType=MIXED&date=2026-10-10&page=1&size=20`

**Role:** Admin.

**Response — HTTP 200:**

```json
{"items":[...],"page":1,"size":20,"total":57}
```

The list supports filtering by status, priority, waste type, and date (SCW-F-014).

### GET `/api/v1/requests/{id}`

**Role:** Request owner or Admin.

**Response — HTTP 200:** Returns the full request object.

**Errors:** HTTP 403 or HTTP 404, using the common API error body.

Citizens use this endpoint to retrieve their request status (SCW-F-012) and to read an Admin priority override (SCW-F-011).

### PATCH `/api/v1/requests/{id}/status`

**Role:** Admin.

**Request:**

```json
{"status":"APPROVED|REJECTED","priority":"HIGH|MEDIUM|LOW (optional override)","reason":"optional"}
```

**Response — HTTP 200:**

```json
{"id":101,"status":"APPROVED","priority":"HIGH","updatedAt":"..."}
```

**Errors:** HTTP 403 (not admin), HTTP 404, or HTTP 409 with code `INVALID_STATUS_TRANSITION`.

This endpoint supports Admin approval or rejection and priority override (SCW-F-011, SCW-F-014). Administrative approval and rejection are recorded in the audit log (SCW-SEC-006).

### DELETE `/api/v1/requests/{id}`

**Role:** Citizen, for their own requests.

**Response — HTTP 200:**

```json
{"id":101,"status":"CANCELLED"}
```

**Errors:** HTTP 409 if the request is SCHEDULED or later.

Cancellation is permitted only before Scheduled; successful cancellation changes the status to Cancelled (SCW-F-013).

### Status Values

`SUBMITTED`, `APPROVED`, `SCHEDULED`, `COLLECTED`, `REJECTED`, `MISSED`, `CANCELLED` (SCW-F-012).
