\# TC-RT-02: Vehicle Capacity and Facility Detours



| Field | Details |

|---|---|

| \*\*Test Case ID\*\* | TC-RT-02 |

| \*\*Title\*\* | Verify vehicle capacity limits and facility detours |

| \*\*Requirement(s)\*\* | SCW-F-042, SCW-F-023 |

| \*\*Test Type\*\* | Functional |

| \*\*Priority\*\* | High |

| \*\*Preconditions\*\* | The system is available; an authorized user can generate routes; vehicle capacities, collection requests, waste quantities, and suitable waste facilities are configured. |

| \*\*Test Data\*\* | Configure a vehicle with a known capacity and approved collection requests whose combined waste quantity exceeds that capacity. Configure at least one suitable facility and provide the locations needed to determine the nearest suitable facility. |

| \*\*Actual Result\*\* | To be recorded after execution. |

| \*\*Status\*\* | Not run |



\## Test Steps and Expected Results



| Step | Action | Expected Result |

|---|---|---|

| 1 | Open the route-generation workflow and select the configured vehicle and collection requests. | The system recognizes the vehicle's configured capacity and the eligible collection requests. |

| 2 | Generate a route using requests whose combined waste quantity exceeds the vehicle's capacity. | The generated route respects the vehicle's capacity limit; the planned collection load never exceeds the configured capacity. |

| 3 | Inspect the route when the vehicle reaches its capacity limit. | The route directs the vehicle to the nearest suitable configured facility before additional collection would exceed its capacity. |

| 4 | Inspect the route after the facility stop. | The route follows the system's configured facility and collection workflow, without planning an over-capacity collection load. |

| 5 | Compare the route's planned load with the vehicle capacity at each collection step. | At every step, the planned load is less than or equal to the configured vehicle capacity. |

| 6 | Record the outcome and any observed defects. | Actual results and supporting evidence are documented; the status is updated only after execution. |



\## Pass/Fail Criteria



\*\*Pass:\*\* The generated route never exceeds the configured vehicle capacity and directs a full vehicle to the nearest suitable configured facility before any further collection would exceed capacity.



\*\*Fail:\*\* Any planned collection step exceeds vehicle capacity, the system continues collecting when doing so would exceed capacity, or the route fails to direct a full vehicle to the nearest suitable configured facility.



\## Execution Notes



\- Record the vehicle capacity, collection quantities, facility locations, generated route, and calculated load at each step.

\- Ensure that the test data makes the nearest suitable facility unambiguous.

\- Verify the requirement for SCW-F-023 against its authoritative registry definition before finalizing execution evidence; do not assume additional behavior beyond that definition.

\- Keep the status as \*\*Not run\*\* until the test has actually been executed.

\- Report any mismatch between expected and actual results as a defect.

