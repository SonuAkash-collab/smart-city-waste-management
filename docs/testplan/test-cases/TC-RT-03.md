\# TC-RT-03: Driver Route Viewing and Collection Status Updates



| Field | Details |

|---|---|

| \*\*Test Case ID\*\* | TC-RT-03 |

| \*\*Title\*\* | Verify driver route viewing and collection status updates |

| \*\*Requirement(s)\*\* | SCW-F-043, SCW-F-044 |

| \*\*Test Type\*\* | Functional |

| \*\*Priority\*\* | High |

| \*\*Preconditions\*\* | The system is available; a driver account is configured; the driver has an assigned route containing multiple collection stops; the associated waste requests have known initial statuses. |

| \*\*Test Data\*\* | One assigned route containing at least three ordered stops, with each stop linked to a waste collection request. Include valid collection and missed-stop scenarios. |

| \*\*Actual Result\*\* | To be recorded after execution. |

| \*\*Status\*\* | Not run |



\## Test Steps and Expected Results



| Step | Action | Expected Result |

|---|---|---|

| 1 | Sign in using the configured driver account. | The driver can access the driver's assigned route. |

| 2 | Open the assigned route. | The route displays its stops in the assigned order. |

| 3 | Inspect the route map and its stop markers. | The map presents the assigned route and its ordered stops in a manner that allows the driver to identify the stops. |

| 4 | Select the first stop and mark it as \*\*Collected\*\*. | The system records the collection status for that stop and updates the associated waste request status automatically. |

| 5 | Select another stop and mark it as \*\*Missed\*\*. | The system records the missed-stop status and updates the associated waste request status automatically according to the defined workflow. |

| 6 | Refresh or reopen the assigned route and inspect both requests. | The recorded statuses remain consistent with the updates made in Steps 4 and 5. |

| 7 | Inspect the remaining stops. | Updating one stop does not incorrectly change the status of unrelated requests. |

| 8 | Record the outcome and any observed defects. | Actual results and supporting evidence are documented; the status is updated only after execution. |



\## Pass/Fail Criteria



\*\*Pass:\*\* The driver can view the assigned route with ordered stops, mark stops as Collected or Missed, and observe the corresponding waste request status updates. Unrelated request statuses remain unchanged.



\*\*Fail:\*\* The assigned route or ordered stops cannot be viewed, a stop status cannot be recorded, the corresponding request status fails to update as specified, or an unrelated request is incorrectly modified.



\## Execution Notes



\- Record the test environment, driver account identifier (without passwords), assigned route, and request identifiers.

\- Capture evidence of the route map and the resulting request statuses.

\- Verify the exact request-status transitions against the requirements registry or approved workflow before execution.

\- Keep the status as \*\*Not run\*\* until the test has actually been executed.

\- Report any mismatch between expected and actual results as a defect.

