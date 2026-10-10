# 5.1 Security Requirements

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04  
**Date:** 10-10-2026  
**Status:** Draft

## 5.1.1 Security Objectives

| ID | Security Objective | Description |
|---|---|---|
| SCW-SO-1 | Confidentiality | Protect users' personal information and home locations from unauthorised access or disclosure. |
| SCW-SO-2 | Integrity and accountability | Protect request, route, and facility data from unauthorised modification and maintain records of administrative actions. |

## 5.1.2 Security Requirements

| Req ID | Requirement | Priority | Acceptance Criteria / Test Case Ref | Comments / Dependencies |
|---|---|---|---|---|
| SCW-SEC-001 | The system shall store user passwords only as bcrypt hashes and shall never store plaintext passwords. | High | AC-SCW-SEC-001: Stored password values are bcrypt hashes and do not match the submitted plaintext passwords. Test: TC-SEC-01. | Depends on Auth & User Service. |
| SCW-SEC-002 | The system shall expire JWT access tokens after 30 minutes. | High | AC-SCW-SEC-002: An expired access token is rejected and the protected API returns HTTP 401. Test: TC-SEC-02. | Depends on Auth & User Service. |
| SCW-SEC-003 | The system shall transmit application traffic over HTTPS using TLS 1.2 or later. | High | AC-SCW-SEC-003: The deployed application accepts HTTPS connections using TLS 1.2 or later and does not permit insecure HTTP access to protected application endpoints. Test: covered in sprint testing. | Depends on deployment and server configuration. |
| SCW-SEC-004 | The system shall enforce server-side role-based access checks for every API call. | High | AC-SCW-SEC-004: A citizen attempting to access an admin-only endpoint receives HTTP 403, and unauthenticated requests receive HTTP 401. Test: TC-SEC-02, TC-AUTH-02. | Depends on Auth & User Service and all protected API services. |
| SCW-SEC-005 | The system shall lock an account for 15 minutes after five consecutive failed login attempts. | High | AC-SCW-SEC-005: After five consecutive failed login attempts, further login attempts are blocked for 15 minutes; login is permitted again after the lock period if valid credentials are supplied. Test: TC-SEC-01. | Depends on Auth & User Service. |
| SCW-SEC-006 | The system shall record all administrative approvals, rejections, route generation actions, and account changes in an audit log. | High | AC-SCW-SEC-006: Each listed administrative action produces an audit record containing the actor, action, timestamp, and affected record identifier. Test: covered in sprint testing. | Depends on audit logging and persistent storage. |

## Security Validation Notes

- Password hashing shall use bcrypt.
- JWT access tokens shall expire after 30 minutes.
- Server-side authorization shall be enforced for every protected API call.
- Account lockout shall follow the five-failure, 15-minute rule.
- Administrative actions shall be recorded for accountability.