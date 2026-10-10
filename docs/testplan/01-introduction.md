# Test Plan

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 1. Introduction

### 1.1 Purpose

This Test Plan describes how the Smart City Waste Management System (SCW), version 1.0, will be tested. It defines the items and features to be tested, the test approach, environment, schedule, responsibilities and risks, and the test cases that verify the functional, non-functional and security requirements in the SRS. Every test case traces to at least one requirement ID, and every requirement is either covered by a test case in this plan or marked as covered in sprint testing (Section 13).

### 1.2 Scope

In scope:

- Functional testing of all six feature areas: authentication & roles, collection requests, vehicle management, facility management, route generation, and notifications & reports (SCW-F-001 – SCW-F-052).
- Performance testing of route generation and API response times (SCW-NF-001, SCW-NF-002).
- Security validation of password storage, token expiry, role-based access control, account lockout, TLS and input validation (SCW-SEC-001 – SCW-SEC-006).
- Unit, integration, system and acceptance test levels for the Web Frontend and the FastAPI services.

Out of scope (detailed in Section 4): internals of OpenStreetMap and the email provider, hardware GPS devices, and third-party browser behaviour.

### 1.3 References

| Document | Version |
|---|---|
| Software Requirements Specification (SRS) – Smart City Waste Management System | 1.0 |
| Software Architecture & Design (SAD) – Smart City Waste Management System | 1.0 |
| Requirements Registry (`docs/requirements-registry.md`) | 1.0 |
| IEEE 829-2008 – Standard for Software and System Test Documentation | – |
| OWASP Web Security Testing Guide | v4.2 |

### 1.4 Definitions, Acronyms and Abbreviations

| Term | Definition |
|---|---|
| SCW | Smart City Waste Management System (prefix of all requirement IDs) |
| TC | Test case; IDs have the form `TC-<AREA>-<NN>` (e.g. `TC-REQ-01`) |
| Test item | A software component or module that is tested |
| Unit test | Test of a single function or class in isolation |
| Integration test | Test of interaction between two or more components (e.g. Route Optimization Engine and Fleet Service) |
| System test | End-to-end test of the complete system through its user interface or API |
| Acceptance test | Test confirming that a requirement's acceptance criterion (`AC-SCW-…`) is met |
| Regression test | Re-run of existing tests after a change to confirm nothing broke |
| Sprint testing | Verification of a requirement during development sprints without a dedicated test case in this plan |
| Entry / exit criteria | Conditions that must hold before testing starts / before it is considered complete |
| RTM | Requirements Traceability Matrix |
| RBAC | Role-Based Access Control |
| JWT | JSON Web Token |
| Pytest | Python unit and integration testing framework |
| Locust / JMeter | Load and performance testing tools |
| Postman | API testing tool |
