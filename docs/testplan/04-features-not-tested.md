# 4. Features Not Tested

**Project:** Smart City Waste Management System
**Version:** 1.0
**Authors:** Team 04
**Date:** 10-10-2026
**Status:** Draft

## 4.1 Purpose

This section identifies features that are outside the scope of the current Test Plan. Exclusion from this plan does not mean that a feature is unnecessary or permanently excluded from project testing.

## 4.2 Excluded Features

| Feature | Reason for Exclusion | Risk / Notes |
|---|---|---|
| Third-party map service internal implementation | The internal implementation of OpenStreetMap and its underlying infrastructure is outside the team's control. Testing will focus on the application's integration with the map service and its handling of map data. | External service outages or unavailable map data may affect route visualization. |
| Production infrastructure and hosting operations | Production infrastructure configuration and operational procedures are outside the scope of the current feature-focused test cases. | Deployment and infrastructure testing may be required before production release. |
| Real-world vehicle hardware and weighing equipment | Physical vehicle behavior and calibration of weighing equipment are not covered by the software test cases in this plan. | The application will be tested using controlled test data for vehicle load and facility delivery scenarios. |

## 4.3 Scope Clarification

The exclusions listed above apply only to the current Test Plan. They do not exclude testing of application behavior that depends on these external systems or inputs.

The following remain in scope:

- Route generation and stop ordering.
- Vehicle capacity enforcement and suitable disposal-facility selection.
- Driver route viewing and collection-status updates.
- Route-generation and API response performance targets.

## 4.4 Review and Approval

Any change to the testing scope or addition of exclusions must be reviewed and agreed upon by the project team. Exclusions and their associated risks should be documented before the final Test Plan is approved.
