## Plan: Complete Ghost-as-a-Service Implementation

The project has a fully implemented repository layer with PydanticAI integration but is missing the service layer entirely. We'll implement the service layer following the Command pattern and TDD principles, integrate it with the Lambda handler, and add comprehensive error handling.

**Phases: 4**

1. **Phase 1: Service Layer Interfaces and Base Classes**
   - **Objective:** Create abstract base classes for the service layer following Command pattern
   - **Files/Functions to Create:**
     - app/services/excuse_generator/interface.py - `ExcuseGeneratorABC` and `ExcuseGeneratorOperationABC`
     - app/services/excuse_generator/operations/interface.py - `ExcuseGeneratorOperationABC`
   - **Tests to Write:** Already exist in tests/services/excuse_generator/operations/test_generate_vague.py
   - **Steps:**
     1. Run existing tests to see them fail (imports won't resolve)
     2. Create `ExcuseGeneratorOperationABC` in app/services/excuse_generator/operations/interface.py as abstract base class with `execute(service: ExcuseGeneratorABC) -> str` method
     3. Create `ExcuseGeneratorABC` in app/services/excuse_generator/interface.py with `excuse_repository` attribute
     4. Update app/services/excuse_generator/operations/__init__.py to export `ExcuseGeneratorOperationABC`
     5. Run tests again - should still fail but imports should resolve

2. **Phase 2: Service Layer Implementation**
   - **Objective:** Implement the concrete service class and GenerateVague operation
   - **Files/Functions to Create:**
     - app/services/excuse_generator/__init__.py - `ExcuseGenerator` class
     - app/services/excuse_generator/operations/generate_vague.py - `GenerateVague` operation
   - **Tests to Write:** Already exist in tests/services/excuse_generator/operations/test_generate_vague.py
   - **Steps:**
     1. Run tests to see them fail (classes don't exist yet)
     2. Create `GenerateVague` operation in app/services/excuse_generator/operations/generate_vague.py with input validation and GetVague call
     3. Update app/services/excuse_generator/operations/__init__.py to export `GenerateVague`
     4. Create `ExcuseGenerator` class in app/services/excuse_generator/__init__.py with dependency injection
     5. Run tests - all service tests should now pass
     6. Run linter/formatter (ruff)

3. **Phase 3: Lambda Handler Integration**
   - **Objective:** Connect the service layer to the Lambda handler entry point
   - **Files/Functions to Modify:**
     - app/__init__.py - `lambda_handler` and `_handle_event` functions
   - **Tests to Write:** Manual validation or create integration test
   - **Steps:**
     1. Read current Lambda handler implementation
     2. Import `ExcuseGenerator` and `GenerateVague` in app/__init__.py
     3. Replace TODO comment with actual implementation: instantiate service, create operation, execute, return response
     4. Add basic error handling with try-except for custom exceptions
     5. Map exceptions to appropriate HTTP status codes (400 for validation, 500 for others)
     6. Run all tests to ensure no regressions

4. **Phase 4: Error Handling and Observability**
   - **Objective:** Add comprehensive error handling, structured logging, and proper HTTP responses
   - **Files/Functions to Modify:**
     - app/__init__.py - Enhanced error handling in `_handle_event`
   - **Tests to Write:** Add tests for error scenarios if needed
   - **Steps:**
     1. Add detailed exception handling for each custom exception type
     2. Use Lambda Powertools logger for structured error logging with context
     3. Create proper error response structure with status code, message, and details
     4. Add metrics using Lambda Powertools for tracking errors and latency
     5. Test with various error scenarios (empty request, API failures, etc.)
     6. Run all tests and verify 80%+ coverage

**Open Questions**

1. Should we add integration tests for the Lambda handler, or rely on manual testing for now? - Relying on manual testing
2. Do you want metrics/tracing enabled in the Lambda handler, or just logging? - Logging priority, metrics if time permits
3. Should error responses follow a specific format (e.g., RFC 7807 Problem Details)? - Simple dict format with statusCode, error, message
