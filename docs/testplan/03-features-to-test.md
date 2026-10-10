# 3. Features to Be Tested

**Project:** Smart City Waste Management System  
**Version:** 1.0  
**Authors:** Team 04  
**Date:** 10-10-2026  
**Status:** Draft

## 3.1 Overview

This section identifies the features to be tested for the Smart City Waste Management System. The test scope is based on the requirements registry and focuses on route generation, route ordering, vehicle capacity handling, driver route viewing, collection-status updates, and performance.

## 3.2 Functional Features

| Feature | Description | Requirement IDs | Test Case |
|---|---|---|---|
| Route generation | Verify that an administrator can generate collection routes for a selected date using approved requests. | SCW-F-040 | TC-RT-01 |
| Route stop ordering | Verify that stops are ordered by priority first and then by shortest distance. | SCW-F-041 | TC-RT-01 |
| Vehicle capacity handling | Verify that vehicle load never exceeds capacity and that a full vehicle is directed to the nearest suitable disposal facility. | SCW-F-042 | TC-RT-02 |
| Driver route viewing | Verify that a driver can view an assigned route as ordered stops on a map. | SCW-F-043 | TC-RT-03 |
| Collection-status updates | Verify that a driver can mark a stop as Collected or Missed and that the associated request status updates automatically. | SCW-F-044 | TC-RT-03 |

## 3.3 Non-Functional Features

| Feature | Description | Requirement ID | Test Case |
|---|---|---|---|
| Route-generation performance | Verify that route generation completes within 10 seconds for 200 approved requests and 20 vehicles. | SCW-NF-001 | TC-PERF-01 |
| API response performance | Verify that at least 95% of API responses complete within 2 seconds under 100 concurrent users. | SCW-NF-002 | TC-PERF-01 |

## 3.4 Test Scope

Testing will cover the functional behavior and measurable performance targets listed above. Test cases will use defined preconditions, test data, execution steps, expected results, actual results, and execution status.

Tests will be recorded as Not run until they are executed. Results will be updated based on actual observations rather than assumed outcomes.

## 3.5 Traceability

The requirement IDs and test case IDs in this section follow the project's requirements registry. Any change to these IDs must be coordinated with the project lead so that the requirements traceability matrix remains consistent.