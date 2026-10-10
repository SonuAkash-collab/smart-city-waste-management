# Software Requirements Specification

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional, non-functional and security requirements of the Smart City Waste Management System (SCW), version 1.0. It is the agreed baseline for the Software Architecture & Design (SAD) document and the Test Plan: every requirement here has a unique ID (prefix `SCW-`) that the SAD maps to a design component and the Test Plan maps to one or more test cases.

### 1.2 Scope

The Smart City Waste Management System is a web application that lets a municipality manage waste collection requests, collection vehicles and disposal facilities, and generate collection routes for each day.

The system will:

- Allow citizens to submit waste collection requests with a location, waste type and estimated quantity, and track each request until it is collected, rejected or missed.
- Assign each request a priority (High, Medium or Low) based on waste type and request age.
- Allow the Admin / Municipal Officer to approve or reject requests and to manage vehicles, drivers, disposal facilities and user accounts.
- Generate daily collection routes from approved requests, ordering stops by priority first and then by shortest distance, without exceeding any vehicle's capacity.
- Allow drivers to view their assigned route on a map and mark each stop as Collected or Missed.
- Allow disposal facility operators to record incoming waste and keep remaining facility capacity up to date.
- Notify citizens of every status change and give the Admin a dashboard and a daily CSV collection report.

Out of scope for version 1.0: real-time GPS tracking of vehicles, payment or billing, native mobile apps, and integration with external municipal ERP systems.

### 1.3 Intended Audience

| Audience | How they use this document |
|---|---|
| Municipal officers (client / product owner) | Confirm that the requirements match the municipality's needs |
| Developers (Team 04) | Implement each requirement against its ID and acceptance criterion |
| Architects / designers | Derive components and interfaces in the SAD |
| Testers | Derive test cases in the Test Plan and trace them back to requirement IDs |
| Course instructors / evaluators | Assess completeness, clarity and traceability |

Readers new to the project should start with Sections 1 and 2; developers and testers should focus on Sections 4, 5 and 8.

### 1.4 Definitions, Acronyms and Abbreviations

| Term | Definition |
|---|---|
| SCW | Smart City Waste Management System (prefix of all requirement IDs) |
| SRS | Software Requirements Specification |
| SAD | Software Architecture & Design document |
| RTM | Requirements Traceability Matrix |
| FR | Functional Requirement (IDs `SCW-F-xxx`) |
| NFR | Non-Functional Requirement (IDs `SCW-NF-xxx`) |
| SO / SEC | Security Objective (`SCW-SO-x`) / Security Requirement (`SCW-SEC-xxx`) |
| AC | Acceptance Criterion (IDs `AC-SCW-F-xxx`) |
| TC | Test Case (e.g. `TC-REQ-01`) |
| Citizen | Resident who submits and tracks waste collection requests |
| Driver | Collection vehicle driver who follows an assigned route |
| Admin | Admin / Municipal Officer who manages requests, vehicles, facilities, users and routes |
| Operator | Disposal facility operator who records incoming waste and manages facility capacity |
| Collection request | A citizen's request to collect a given waste type and quantity from a location |
| Route | Ordered list of stops (collection points and facility visits) assigned to one vehicle for one date |
| Stop | One collection point or facility visit within a route |
| Priority | High, Medium or Low ranking of a request, used to order route stops |
| Capacity | Maximum load of a vehicle (kg) or daily intake of a facility (kg) |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| JWT | JSON Web Token, used for authentication |
| RBAC | Role-Based Access Control |
| HTTPS / TLS | HTTP over Transport Layer Security |
| CSV | Comma-Separated Values file format |
| OSM | OpenStreetMap |
| UML | Unified Modeling Language |
