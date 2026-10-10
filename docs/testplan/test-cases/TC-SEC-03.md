# TC-SEC-03: HTTPS and TLS Security Validation

| Field | Content |
|---|---|
| TC ID | TC-SEC-03 |
| Title | Verify HTTPS enforcement and TLS version |
| Requirement(s) | SCW-SEC-003 |
| Type | Security |
| Preconditions | 1. The system is deployed in a test environment. 2. The deployment hostname and HTTPS endpoint are known. 3. An authorized test account exists. |
| Test data | HTTPS base URL; protected API endpoint such as `/api/v1/vehicles`; HTTP version of the same endpoint; TLS 1.2 and TLS 1.3 client configurations where supported. |
| Steps | 1. Connect to the application using HTTPS with a supported TLS 1.2-or-later client. 2. Verify the negotiated TLS version. 3. Call a protected API endpoint over HTTPS without a token. 4. Attempt to access the same protected endpoint using plain HTTP. 5. Inspect the HTTP response and verify that protected response data is not disclosed. |
| Expected result | 1. HTTPS connections negotiate TLS 1.2 or later. 2. The protected endpoint enforces authentication even over HTTPS. 3. Plain HTTP is rejected or redirected to HTTPS without disclosing protected data. 4. The test results record the negotiated TLS version and the behavior of the HTTP endpoint. |
| Actual result | To be filled during testing. |
| Status | Not run |