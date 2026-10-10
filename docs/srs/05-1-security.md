# 5.1 Security Objectives and Requirements

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC  
**Date:** 10-10-2026  
**Status:** Draft

## Security Objectives

| Objective ID | Objective | Description |
|---|---|---|
| SCW-SO-1 | Confidentiality | The system shall protect user credentials and sensitive operational data from unauthorized access or disclosure. |
| SCW-SO-2 | Integrity and Accountability | The system shall protect operational records against unauthorized modification and maintain audit records for administrative actions. |

## Security Requirements

| Req ID | Requirement (The system shall…) | Type | Priority | Source/Stakeholder | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|---|---|
| SCW-SEC-001 | The system shall store passwords using bcrypt hashing and shall not store plaintext passwords. | Security | Critical | All users / Security requirements | AC-SCW-SEC-001: Stored passwords are bcrypt hashes, and authentication does not require plaintext passwords to be stored. Test: TC-SEC-01. | Depends on Auth & User Service. |
| SCW-SEC-002 | The system shall expire JWT access tokens after 30 minutes. | Security | High | All users / Security requirements | AC-SCW-SEC-002: An expired token is rejected when accessing a protected endpoint. Test: TC-SEC-02. | Depends on Auth & User Service. |
| SCW-SEC-003 | The system shall use HTTPS with TLS 1.2 or higher for client-server communication and shall not expose protected endpoints over unencrypted HTTP. | Security | Critical | All users / Security requirements | AC-SCW-SEC-003: HTTPS connections negotiate TLS 1.2 or higher. Attempts to access protected endpoints over plain HTTP are rejected or redirected to HTTPS without exposing protected data. Test: TC-SEC-03. | Depends on deployment configuration and web server. |
| SCW-SEC-004 | The system shall enforce role-based access control on every protected API request. Public or explicitly unauthenticated endpoints shall be limited to documented operations; all other endpoints shall require authentication and the appropriate role. | Security | Critical | Admin / Municipal Officer / Security requirements | AC-SCW-SEC-004: Unauthenticated requests to protected endpoints are rejected with HTTP 401. Authenticated users without the required role are rejected with HTTP 403. Public endpoints are explicitly documented and limited to their intended operations. Test: TC-SEC-02 and TC-AUTH-02. | Depends on Auth & User Service and API middleware. |
| SCW-SEC-005 | The system shall temporarily lock an account for 15 minutes after five consecutive failed login attempts. A successful login shall reset the consecutive-failure counter. | Security | High | All users / Security requirements | AC-SCW-SEC-005: The first four consecutive failed attempts do not trigger lockout. The fifth consecutive failure triggers a 15-minute lockout. Further login attempts are blocked during the lockout, and login is permitted after the lockout expires if the credentials are valid. A successful login resets the failure counter. Test: TC-SEC-01. | Depends on Auth & User Service and account-state storage. |
| SCW-SEC-006 | The system shall maintain audit logs for administrative approvals and rejections, route generation, and account changes. | Security | High | Admin / Municipal Officer / Security requirements | AC-SCW-SEC-006: Each tested administrative action creates an audit record containing the actor identifier, action performed, timestamp, and affected record identifier where applicable. Test: TC-SEC-04. | Depends on audit logging and persistent storage. |

## Security Implementation Notes

- Passwords shall be hashed with bcrypt before storage.
- JWT access tokens shall expire after 30 minutes.
- Protected client-server communication shall use HTTPS with TLS 1.2 or higher.
- Protected API endpoints shall enforce server-side authentication and role-based authorization.
- Public or unauthenticated endpoints shall be explicitly documented and limited to necessary operations.
- Failed login attempts shall be counted consecutively. Five consecutive failed attempts shall trigger a 15-minute account lockout.
- Successful authentication shall reset the consecutive-failure counter.
- Administrative approvals, rejections, route generation, and account changes shall be recorded in audit logs to support accountability and investigation.

## Dependencies

- Auth & User Service manages password hashing, JWT validation, account lockout, and role-based authorization.
- API middleware enforces authentication and authorization for protected endpoints.
- Deployment configuration enables HTTPS and TLS 1.2 or higher.
- Audit logging records administrative activity and stores audit events.