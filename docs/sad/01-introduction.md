# Software Architecture & Design

| Item | Value |
|---|---|
| Project | Smart City Waste Management System |
| Version | 1.0 |
| Authors | Team 04 – Sonu Akash, Rishit V N S, Rottela Haritej, Purushothama KC |
| Date | 10-10-2026 |
| Status | Draft |

## 1. Introduction

### 1.1 Purpose

This Software Architecture & Design (SAD) document describes the architecture and detailed design of the Smart City Waste Management System (SCW), version 1.0. It explains how the system is divided into components, which architecture pattern and technologies are used and why, how the design satisfies the requirements in the SRS, how the system is secured, and how the main components interact through their APIs. It is the reference for developers implementing the system and for testers verifying it.

### 1.2 Scope

This document covers:

- The overall architecture: components, the layered (3-tier) architecture pattern, the technology stack and data stores, risks, and the security architecture (STRIDE threat model).
- Traceability from every requirement ID in the SRS (`SCW-F-xxx`, `SCW-NF-xxx`, `SCW-SO-x`, `SCW-SEC-xxx`) to the component that implements it.
- The detailed design: UML sequence diagrams for submitting a collection request and generating routes, REST API design for the Request Service and the Route Optimization Engine, error handling, logging and monitoring, and UX design.

The requirements themselves are defined in the SRS and are not repeated here. Deployment scripts, the database schema at column level and source code are outside the scope of this document.

### 1.3 Intended Audience

| Audience | How they use this document |
|---|---|
| Developers (Team 04) | Implement each component and API according to the design |
| Testers | Understand component boundaries and APIs to design integration, system and security tests |
| Architects / reviewers | Check that the architecture meets the requirements and quality goals |
| Municipal officers (client) | Understand the system structure and its main technology choices |
| Course instructors / evaluators | Assess architecture quality, design completeness and traceability |

### 1.4 Definitions, Acronyms and Abbreviations

| Term | Definition |
|---|---|
| SCW | Smart City Waste Management System (prefix of all requirement IDs) |
| SAD | Software Architecture & Design document |
| SRS | Software Requirements Specification |
| RTM | Requirements Traceability Matrix |
| Component | An independently described part of the system with a defined responsibility and interface (see Section 3.4) |
| Layered (3-tier) architecture | Architecture with Presentation, Application/Service and Data layers, where each layer calls only the layer below it |
| Route Optimization Engine | Component that generates daily collection routes and handles driver stop updates |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token, used as a bearer token for authentication |
| RBAC | Role-Based Access Control |
| STRIDE | Threat model categories: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege |
| UML | Unified Modeling Language |
| ORM | Object-Relational Mapping |
| OSM / OSRM | OpenStreetMap / Open Source Routing Machine |
| Haversine | Formula for great-circle distance between two latitude/longitude points |
| HTTPS / TLS | HTTP over Transport Layer Security |
| CSV | Comma-Separated Values file format |

Role names (Citizen, Collection Vehicle Driver, Admin / Municipal Officer, Disposal Facility Operator) and domain terms (collection request, route, stop, priority, capacity) are defined in SRS Section 1.4.
