
# 3.9 Security Architecture and STRIDE Threat Model

## 3.9.1 Purpose

This section identifies security threats to the Smart City Waste Management System using the STRIDE threat-modelling framework and defines mitigations consistent with the project's security requirements.

## 3.9.2 Security Objectives

- **SCW-SO-1 — Confidentiality:** Protect user personal data and home locations from unauthorized access.
- **SCW-SO-2 — Integrity and accountability:** Protect request, route, and facility data from unauthorized modification and support accountability for administrative actions.

## 3.9.3 STRIDE Threat Analysis

| STRIDE Category | Threat Scenario | Potential Impact | Mitigation | Related Requirement |
|---|---|---|---|---|
| Spoofing | An attacker attempts to impersonate a citizen, driver, operator, or administrator using stolen credentials or a forged token. | Unauthorized access to role-specific operations and personal data. | Store passwords using bcrypt hashes, validate JWT access tokens, expire access tokens after 30 minutes, and enforce server-side role checks. | SCW-SEC-001, SCW-SEC-002, SCW-SEC-004 |
| Tampering | An unauthorized user modifies collection requests, route stops, vehicle loads, or facility capacity. | Incorrect collection operations, capacity violations, or inconsistent records. | Enforce authorization on protected APIs, validate input on the server, apply database constraints and transactions, and record relevant administrative actions in the audit log. | SCW-SEC-004, SCW-SEC-006 |
| Repudiation | An administrator denies having approved or rejected a request, generated a route, or changed an account. | Reduced accountability and difficulty investigating operational incidents. | Record relevant administrative actions in an audit log with the actor, action, target record, and timestamp. Restrict unauthorized modification of audit records. | SCW-SEC-006 |
| Information Disclosure | An unauthorized user obtains personal details, home locations, or information belonging to another role. | Privacy violations and exposure of sensitive operational information. | Enforce role-based access checks on the server, return only authorized data, use HTTPS with TLS 1.2 or later, and avoid exposing sensitive information in error messages or logs. | SCW-SO-1, SCW-SEC-003, SCW-SEC-004 |
| Denial of Service | Excessive or malformed requests consume API, database, or route-generation resources. | Delayed or unavailable request processing and route generation. | Validate incoming requests, apply appropriate request limits and timeouts, monitor service health, and test the defined performance workload. | SCW-NF-001, SCW-NF-002 |
| Elevation of Privilege | A citizen or driver attempts to access administrator-only endpoints or perform another role's operations. | Unauthorized account management, request decisions, or route generation. | Apply server-side role-based authorization to every protected API endpoint. Return HTTP 403 when an authenticated user lacks permission. | SCW-F-002, SCW-SEC-004 |

## 3.9.4 Security Controls by Architecture Layer

| Architecture Layer | Security Controls |
|---|---|
| Presentation Layer — Web Frontend | Present role-appropriate functions, use HTTPS, and avoid relying on client-side checks as the only authorization control. |
| Application Layer — FastAPI Services | Authenticate users, validate JWT expiry, enforce server-side role checks, validate inputs, handle errors safely, and record relevant administrative actions. |
| Data Layer — PostgreSQL | Store password hashes rather than plaintext passwords, apply database constraints and transactions, restrict database access, and protect audit records against unauthorized modification. |

## 3.9.5 Authentication and Access Control

The Auth & User Service authenticates users and issues JWT access tokens. Tokens expire after 30 minutes. Passwords are stored as bcrypt hashes, and accounts are locked for 15 minutes after five consecutive failed login attempts. Successful authentication resets the consecutive-failure count.

Authorization is enforced by FastAPI services on the server. The Web Frontend may hide unavailable functions for usability, but server-side checks remain mandatory.

## 3.9.6 Transport Security

All application traffic shall use HTTPS with TLS 1.2 or later. Deployment configuration must prevent credentials and access tokens from being transmitted over unencrypted HTTP.

## 3.9.7 Auditability and Monitoring

Relevant administrative actions, including request approvals and rejections, route generation, and account changes, shall be recorded in an audit log. Logs should include sufficient information to investigate actions without unnecessarily storing passwords, access tokens, or other sensitive secrets.

## 3.9.8 Verification

Security controls shall be verified using the project's security test cases and additional sprint testing where a dedicated test case is not yet defined. Verification shall include password hashing, token expiry, role-based access control, login lockout, transport security, and audit-log behavior.
