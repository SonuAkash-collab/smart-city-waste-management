
# 5. Appendices

## 5.1 Glossary

| Term | Definition |
|---|---|
| API | Application Programming Interface; defines how software components communicate. |
| FastAPI | Python web framework used to develop the backend API. |
| JWT | JSON Web Token; a token format used to represent authenticated user claims. |
| RBAC | Role-Based Access Control; restricts actions according to a user's assigned role. |
| REST | Representational State Transfer; an architectural style commonly used for web APIs. |
| HTTPS | HTTP secured using Transport Layer Security (TLS). |
| TLS | Transport Layer Security; a protocol that protects data transmitted over a network. |
| PostgreSQL | Relational database management system used to store application data. |
| OpenStreetMap (OSM) | Collaborative geographic data source that may support map display and location-related features. |
| SMTP | Simple Mail Transfer Protocol; a protocol used to send email. |
| STRIDE | Security threat-modeling framework covering Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. |
| UML | Unified Modeling Language; a standard notation for representing software structures and behavior. |
| bcrypt | Password-hashing algorithm used to store passwords without keeping them in plaintext. |
| Audit Log | A record of selected security-sensitive or administrative events. |
| Route Optimization | The process of ordering vehicle stops while considering priorities, distance, vehicle capacity, and facility constraints. |

## 5.2 Architecture and Design References

The following references provide background for the architecture and design practices used in this project:

1. **ISO/IEC/IEEE 42010** — Architecture description for systems and software engineering.
2. **ISO/IEC/IEEE 29148** — Requirements engineering for systems and software.
3. **OWASP Application Security Verification Standard (ASVS)** — Guidance for assessing web application security controls.
4. **OWASP JSON Web Token for Java Cheat Sheet** — Security guidance for JWT-based authentication concepts.
5. **FastAPI Documentation** — Reference for API implementation, request validation, and OpenAPI documentation.
6. **PostgreSQL Documentation** — Reference for relational database design, transactions, and data integrity.
7. **OpenStreetMap Documentation** — Reference for geographic data and map usage.

These references provide design guidance. Their inclusion does not imply that the project has been formally certified or independently audited against them.

## 5.3 Development and Verification Tools

| Tool | Intended Use |
|---|---|
| Visual Studio Code | Source-code editing and project documentation. |
| Git | Version control and individual file commits. |
| GitHub | Repository hosting, pull requests, code review, and collaboration. |
| PlantUML | Creating and maintaining UML diagrams. |
| React | Frontend user interface development. |
| Leaflet | Interactive map presentation in the frontend. |
| FastAPI | Backend API development and API documentation. |
| PostgreSQL | Persistent relational data storage. |
| Postman | Manual API request and response verification. |
| Pytest | Automated backend testing. |
| JMeter or Locust | Optional load and performance testing, depending on the team's final selection. |

## 5.4 Related Project Documents

The following documents provide additional detail about the system:

- Software Requirements Specification (SRS): functional requirements, non-functional requirements, and use cases.
- Software Architecture Document (SAD): system components, architecture decisions, security architecture, risks, and error handling.
- Software Test Plan: test strategy, test cases, security validation, assumptions, and risks.
- Requirements Registry: authoritative requirement IDs and requirement-to-test traceability.
- UML Use-Case Diagram: visual representation of the system actors and their interactions.

## 5.5 Document Maintenance

The project team shall update these appendices when the selected tools, architecture references, or related project documents change. The requirements registry remains the authoritative source for requirement IDs. Any changes to agreed requirements or architecture conventions should be reviewed with the team lead before being reflected in project documentation.
