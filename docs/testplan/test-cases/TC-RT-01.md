\# TC-RT-01: Route Generation and Stop Ordering



| Field | Details |

|---|---|

| \*\*Test Case ID\*\* | TC-RT-01 |

| \*\*Title\*\* | Verify route generation and stop ordering |

| \*\*Requirement(s)\*\* | SCW-F-040, SCW-F-041 |

| \*\*Test Type\*\* | Functional |

| \*\*Priority\*\* | High |

| \*\*Preconditions\*\* | The system is available; an administrator can generate routes; approved waste collection requests, their priorities and locations, and available vehicles are configured for the selected date. |

| \*\*Test Data\*\* | Use at least four approved requests with known locations and priorities, including two requests with equal priority but different distances. Include one unapproved request to verify that it is excluded from route generation. Ensure the selected vehicle has sufficient capacity for this test. |

| \*\*Actual Result\*\* | To be recorded after execution. |

| \*\*Status\*\* | Pass |



\## Test Steps and Expected Results



| Step | Action | Expected Result |

|---|---|---|

| 1 | Sign in as an administrator and open the route-generation workflow. | The route-generation workflow is accessible to the authorized administrator. |

| 2 | Select a date containing the configured approved and unapproved requests. | Requests for the selected date are available for route generation. |

| 3 | Generate routes for the selected date using the available vehicle configuration. | The system generates routes from eligible approved requests without including the unapproved request. |

| 4 | Inspect the generated route and its ordered stops. | Stops are ordered by priority first. Among requests with equal priority, the shorter-distance request is ordered before the longer-distance request. |

| 5 | Compare the generated route with the configured request data. | Each included stop corresponds to an eligible approved request, and the displayed ordering follows the specified priority and distance rules. |

| 6 | Record the outcome and any observed defects. | Actual results and evidence are documented; the status is updated only after execution. |



\## Pass/Fail Criteria



\*\*Pass:\*\* Route generation completes for the selected date, only eligible approved requests are included, and stop ordering follows priority first and shortest distance among requests with equal priority.



\*\*Fail:\*\* Route generation fails unexpectedly, an unapproved request is included, an eligible request is incorrectly omitted, or the generated stop ordering violates the specified priority and distance rules.



\## Execution Notes



\- Record the test date, test environment, selected requests, vehicle configuration, and generated route.

\- Use controlled test data so that request priorities and distances can be compared reliably.

\- Record \*\*Not run\*\* until the test has actually been executed.

\- Report any mismatch between the expected and actual results as a defect.

## Execution record (Part 3, November 2026)

| Field | Details |
|---|---|
| Changes after the sprints | Routes are generated with `POST /api/v1/routes/generate {"date": ...}` from every Approved request; only Available vehicles with an assigned driver are used. Equal-priority stops are chosen nearest-next from the vehicle's current position. |
| Automated tests | `test_routes_api.py::test_generate_orders_by_priority_then_distance`, `test_route_engine.py` (ordering tests) |
| Actual result | Four approved requests and one Submitted request: the Submitted one was left out; the High request came first, then the two Medium requests nearest-next, then Low. Route saved with date and driver. |
| Status | Pass |
