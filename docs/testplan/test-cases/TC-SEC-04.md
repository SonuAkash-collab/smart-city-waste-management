# TC-SEC-04: Administrative Audit Logging

| Field | Content |
|---|---|
| TC ID | TC-SEC-04 |
| Title | Verify audit records for administrative actions |
| Requirement(s) | SCW-SEC-006 |
| Type | Security |
| Preconditions | 1. The system is available in the test environment. 2. An authorized Admin account exists. 3. Audit-log access is available to an authorized tester. 4. Test records are available for request approval/rejection, route generation and account changes. |
| Test data | Admin account ID; test request ID; test route ID; test user account ID; actions: approve request, reject request, generate route, change account details or status. |
| Steps | 1. Log in as Admin. 2. Approve a test request and inspect the corresponding audit record. 3. Reject another test request and inspect its audit record. 4. Generate a route and inspect its audit record. 5. Make an account change and inspect its audit record. 6. Verify each audit record contains the actor identifier, action performed, timestamp and affected record identifier where applicable. 7. Verify that audit records can be retrieved by an authorized tester. |
| Expected result | 1. Each specified administrative action creates an audit record. 2. Each record identifies the actor, action, timestamp and affected record identifier where applicable. 3. Records correspond to the correct actions and affected entities. 4. Audit records are available to authorized testers for verification. |
| Actual result | To be filled during testing. |
| Status | Not run |