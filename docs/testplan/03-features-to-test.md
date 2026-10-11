# 3. Features to Be Tested

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04  
**Date:** 11-10-2026  
**Status:** Draft

## 3.1 Overview

This section identifies the features to be tested for the Smart City Waste Management System. The test scope covers route generation and ordering, vehicle capacity handling, driver route viewing, collection-status updates, reporting, availability, usability, maintainability, and performance. The test cases are mapped to the corresponding requirement IDs in the project's requirements registry.

## 3.2 Functional Features

| Feature | Description | Requirement IDs | Test Case |
|---|---|---|---|
| Route generation | Verify that an administrator can generate collection routes for a selected date using approved requests. | SCW-F-040 | TC-RT-01 |
| Route stop ordering | Verify that stops are ordered by priority first and then by shortest distance. | SCW-F-041 | TC-RT-01 |
| Vehicle capacity handling | Verify that vehicle load never exceeds capacity and that a full vehicle is directed to the nearest suitable disposal facility. | SCW-F-042 | TC-RT-02 |
| No suitable facility available | Verify that the route stops before vehicle capacity is exceeded and an administrator is alerted when no suitable facility has sufficient capacity. | SCW-F-042 | TC-RT-04 |
| Driver route viewing | Verify that a driver can view an assigned route as ordered stops on a map. | SCW-F-043 | TC-RT-03 |
| Collection-status updates | Verify that a driver can mark a stop as Collected or Missed and that the associated request status updates automatically. | SCW-F-044 | TC-RT-03 |
| Dashboard counts | Verify that dashboard counts match the corresponding underlying records. | SCW-F-051 | TC-RPT-01 |
| Daily collection CSV export | Verify that the daily CSV export contains one row per collection for the selected day, with correct columns and values. | SCW-F-052 | TC-RPT-01 |

## 3.3 Non-Functional Features

| Feature | Description | Requirement ID | Test Case |
|---|---|---|---|
| Route-generation performance | Verify that route generation completes within 10 seconds for 200 approved requests and 20 vehicles. | SCW-NF-001 | TC-PERF-01 |
| API response performance | Verify that at least 95% of API calls complete within 2 seconds under 100 concurrent users using Locust. | SCW-NF-002 | TC-PERF-02 |
| System availability | Verify at least 99% uptime over a continuous 24-hour window, with health checks every minute. | SCW-NF-003 | TC-AVL-01 |
| First-time user usability | Verify that five first-time users can each submit a request within 3 minutes on desktop and a mobile viewport 360 CSS pixels wide. | SCW-NF-004 | TC-USE-01 |
| Service-layer test coverage | Verify that pytest with coverage reporting achieves at least 70% statement coverage for the service layer. | SCW-NF-005 | TC-MNT-01 |

## 3.4 Test Scope

Testing covers the functional behavior and measurable non-functional targets listed above. Each test case defines its preconditions, test data, execution steps, expected results, actual results, and execution status.

Tests will remain **Not run** until execution evidence is available. Results will be updated based on actual observations rather than assumed outcomes.

The availability, usability, maintainability, reporting, route edge-case, and API load tests will be executed according to their documented procedures and acceptance criteria.

## 3.5 Traceability

The requirement IDs and test case IDs in this section follow the project's requirements registry and assigned test plan. Any change to requirement IDs, acceptance criteria, or business rules must be coordinated with the project lead so that the requirements registry and traceability documentation remain consistent.

