\# TC-PERF-01: Route Generation and API Performance



| Field | Details |

|---|---|

| \*\*Test Case ID\*\* | TC-PERF-01 |

| \*\*Title\*\* | Verify route generation time and API response performance |

| \*\*Requirement(s)\*\* | SCW-NF-001, SCW-NF-002 |

| \*\*Test Type\*\* | Performance |

| \*\*Priority\*\* | High |

| \*\*Preconditions\*\* | The application and its required services are available in a documented test environment. Representative test data is prepared, and a performance-testing tool is configured. |

| \*\*Test Data\*\* | For route generation, prepare 200 collection requests and 20 vehicles. For API performance, prepare a representative workload of 100 concurrent users and identify the API operations to be measured. |

| \*\*Actual Result\*\* | To be recorded after execution. |

| \*\*Status\*\* | Not run |



\## Test Steps and Expected Results



| Step | Action | Expected Result |

|---|---|---|

| 1 | Configure the test environment and record the application version, hardware or deployment resources, database state, and test tool. | The test environment and measurement conditions are documented so that the results can be interpreted and reproduced. |

| 2 | Prepare 200 eligible collection requests and 20 vehicles for the selected date. | The test data contains the required number of requests and vehicles. |

| 3 | Measure the time taken by the route-generation operation from invocation until a complete result is returned. | Route generation completes within 10 seconds. |

| 4 | Repeat the route-generation measurement under the same documented conditions and record each result. | Each run has a recorded duration, and any variation or failure is documented. |

| 5 | Configure the performance-testing tool to simulate 100 concurrent users against the selected API operations. | The tool generates the intended concurrent workload, and the workload configuration is recorded. |

| 6 | Execute the API load test and record response times and errors for all measured requests. | At least 95% of measured API responses complete within 2 seconds. |

| 7 | Calculate the percentage of API responses completed within 2 seconds and review errors and timeouts. | The measured percentage can be compared directly with the 95% requirement; errors and timeouts are reported separately. |

| 8 | Record the measurements, test environment, evidence, and final outcome. | Actual results and supporting evidence are documented, and the status reflects the observed outcome. |



\## Pass/Fail Criteria



\*\*SCW-NF-001 — Route generation:\*\* Pass if route generation for 200 requests and 20 vehicles completes within 10 seconds under the documented test conditions. Otherwise, fail.



\*\*SCW-NF-002 — API response performance:\*\* Pass if at least 95% of measured API responses complete within 2 seconds under a workload of 100 concurrent users. Otherwise, fail.



The overall test case passes only when both requirements pass. If either requirement fails, the overall test case fails.



\## Execution Notes



\- Record the actual route-generation duration for each run.

\- Record the number of API requests, concurrency settings, response-time distribution, errors, and timeouts.

\- Identify which API operations were measured and how concurrent users were simulated.

\- Do not report performance measurements unless they were obtained by executing the test.

\- Keep the status as \*\*Not run\*\* until execution is complete.

\- Report performance failures as defects and attach the relevant test evidence.

