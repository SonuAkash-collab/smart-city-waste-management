
# 4.4 Error Handling, Logging and Monitoring

## 4.4.1 Purpose

This section defines how the Smart City Waste Management System handles application errors, records operational events, and monitors service health. The design uses consistent JSON error responses so that the Web Frontend can present understandable messages to users.

## 4.4.2 Error Response Format

All API errors shall use the following JSON structure:

```json
{
  "error": {
    "code": "STRING_CODE",
    "message": "Readable message"
  }
}
```

The `code` field identifies the error category, while `message` provides a readable explanation without exposing internal implementation details, credentials, tokens, or database information.

## 4.4.3 HTTP Status Codes

| HTTP Status | Meaning | Example |
|---|---|---|
| 200 OK | The request completed successfully. | Request details retrieved or a route updated. |
| 201 Created | A resource was created successfully. | A new collection request was submitted. |
| 400 Bad Request | The request is malformed or cannot be processed. | An invalid request format is received. |
| 401 Unauthorized | Authentication is missing or invalid. | A missing, expired, or invalid JWT is supplied. |
| 403 Forbidden | The authenticated user lacks permission. | A citizen attempts to use an administrator-only endpoint. |
| 404 Not Found | The requested resource does not exist or is not accessible. | A nonexistent request or route is requested. |
| 409 Conflict | The operation conflicts with the resource's current state. | A citizen attempts to cancel a request after it becomes Scheduled. |
| 422 Unprocessable Entity | Input validation fails. | A vehicle capacity is non-positive or a required field is missing. |
| 500 Internal Server Error | An unexpected server-side failure occurs. | An unhandled application error prevents the operation from completing. |

## 4.4.4 Validation and Exception Handling

- The Web Frontend shall provide immediate feedback for basic input errors, but server-side validation remains authoritative.
- FastAPI services shall validate request data, resource state, and user permissions before performing protected operations.
- Invalid inputs shall return the appropriate 400 or 422 response according to the API convention.
- Authentication failures shall return 401, while authorization failures shall return 403.
- State conflicts shall return 409 without applying the conflicting operation.
- Unexpected exceptions shall be handled centrally and return a generic 500 response.
- Error responses shall not expose stack traces, database credentials, passwords, JWTs, or other sensitive information.

## 4.4.5 Transaction Safety

Database operations that modify related records shall use PostgreSQL transactions where consistency requires them. If an operation fails, the transaction shall be rolled back so that partially applied changes are not retained.

Vehicle-load and facility-capacity updates shall be validated against current capacity. Concurrent intake operations must not allow recorded incoming waste to exceed the facility's remaining daily capacity.

## 4.4.6 Logging

Application logs shall record operational events needed for debugging and incident investigation, including:

- Request processing failures and unexpected exceptions.
- Authentication failures and account-lockout events.
- Route-generation failures and validation errors.
- Database-operation failures and external-service failures.
- Relevant administrative actions required by SCW-SEC-006.

Audit records for administrative actions shall identify the actor, action, affected record, and timestamp where applicable. Logs shall not contain plaintext passwords, access tokens, or unnecessary personal information.

## 4.4.7 Monitoring and Recovery

The team shall monitor application availability, API response times, route-generation duration, database health, and external-service failures.

The following performance targets shall be used for validation:

- Route generation shall complete within 10 seconds for 200 requests and 20 vehicles.
- At least 95% of API responses shall complete within 2 seconds with 100 concurrent users.

If OpenStreetMap or the SMTP email provider becomes unavailable, the system shall report the relevant failure and preserve unrelated functions where possible. In-app request-status tracking shall remain the primary way for citizens to check their request status.

Database backups and restoration procedures shall be documented and tested before production deployment.

## 4.4.8 Verification

Error handling and monitoring shall be verified through functional and integration testing. Tests shall cover invalid input, expired tokens, forbidden operations, missing resources, state conflicts, unexpected server errors, transaction rollback, and logging of relevant administrative actions.
