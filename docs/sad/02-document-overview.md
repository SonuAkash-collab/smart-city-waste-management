## 2. Document Overview

### 2.1 How to Use This Document

The document is organised in two main parts: **Architecture** (Section 3) describes the system at component level, and **Design** (Section 4) describes how the components behave and interact. Readers should use it as follows:

| Section | Content | Most useful for |
|---|---|---|
| 1. Introduction | Purpose, scope, audience, definitions | All readers |
| 2. Document Overview | Structure of this document and related documents | All readers |
| 3.1 – 3.2 | Architectural goals, constraints, stakeholders and their concerns | Architects, client, evaluators |
| 3.3 – 3.4 | Component (UML) diagram and description of each component | Developers, testers |
| 3.5 – 3.6 | Chosen architecture pattern with rationale, technology stack and data stores | Developers, architects |
| 3.7 | Architectural risks and mitigations | Architects, client |
| 3.8 | Traceability of every SRS requirement ID to a component | Testers, evaluators |
| 3.9 | Security architecture (STRIDE threats and mitigations) | Developers, testers, evaluators |
| 4.1 – 4.2 | Design overview and UML sequence diagrams | Developers |
| 4.3 | REST API design for the Request Service and Route Optimization Engine | Developers, testers |
| 4.4 – 4.6 | Error handling, logging and monitoring; UX design; open issues | Developers, testers |
| 5. Appendices | Glossary, references, tools | All readers |

Suggested reading paths:

- **Developers:** Sections 3.3 → 3.4 → 3.6 → 4 (all), then 3.9 for security controls to implement.
- **Testers:** Section 3.8 to find the component behind each requirement, then 4.3 for endpoints and error codes and 3.9 for security controls to validate.
- **Client and evaluators:** Sections 1, 3.1, 3.2, 3.3 and 3.5 for an overview, then 3.8 for traceability.

Conventions used throughout this document:

- Requirement IDs (`SCW-F-xxx`, `SCW-NF-xxx`, `SCW-SO-x`, `SCW-SEC-xxx`) and test case IDs (`TC-XXX-NN`) are the same as in the SRS and Test Plan.
- Component names are used exactly as listed in Section 3.4: Web Frontend, Auth & User Service, Request Service, Fleet Service, Facility Service, Route Optimization Engine, Notification & Reporting Service, Database (PostgreSQL), Map Service (OpenStreetMap).
- All API paths are relative to the base path `/api/v1`.
- Diagrams are written in PlantUML; source files (`.puml`) and exported images (`.png`) are kept in `docs/diagrams/`.

### 2.2 Related Documents

| Document | Version | Relationship to this document |
|---|---|---|
| Software Requirements Specification (SRS) – Smart City Waste Management System | 1.0 | Defines all functional, non-functional and security requirements that this architecture and design implement. Requirement IDs are traced to components in Section 3.8. |
| Test Plan – Smart City Waste Management System | 1.0 | Defines the test strategy and test cases (TC-AUTH, TC-REQ, TC-VEH, TC-FAC, TC-RT, TC-NOT, TC-PERF, TC-SEC) that verify the requirements implemented by the components described here. |
| Requirements Traceability Matrix (RTM) – SRS Section 8 | 1.0 | Links each requirement ID to its design component (from this document) and its test cases (from the Test Plan). |
| Requirements Registry (`docs/requirements-registry.md`) | 1.0 | Master list of all requirement, security and test case IDs used by the three documents. |
