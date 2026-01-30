## Plan: Refactor AI Logic to excuse_agent Utility

This plan extracts PydanticAI Agent logic from ExcuseRepository into a new `excuse_agent` utility following the **Type A Infrastructure (Stateful)** pattern. The repository currently violates separation of concerns by directly managing AI client state - this refactoring will establish proper boundaries where repositories handle data access and utilities wrap infrastructure concerns.

**Phases: 4**

1. **Phase 1: Create excuse_agent Utility Infrastructure**
   - **Objective:** Establish the utility module structure with interfaces and base implementation following Type A pattern
   - **Files/Functions to Create:**
     - app/utilities/excuse_agent/interface.py - `ExcuseAgentABC`, `ExcuseAgentOperationABC[TParams, TReturn]`
     - app/utilities/excuse_agent/__init__.py - `ExcuseAgent` class
     - app/utilities/excuse_agent/operations/interface.py - Re-export `ExcuseAgentOperationABC`
     - app/utilities/excuse_agent/operations/__init__.py - Operations export file
   - **Tests to Write:**
     - `test_excuse_agent_interface` - Verify ABC structure
     - `test_excuse_agent_initialization` - Verify agent is created with correct system prompt and model
     - `test_excuse_agent_execute_delegates_to_operation` - Verify execute() passes agent to operation
     - `test_excuse_agent_initialization_with_missing_api_key` - Verify ConfigurationError raised
   - **Steps:**
     1. Write failing tests for ExcuseAgentABC interface (abstract methods, Generic types)
     2. Write failing tests for ExcuseAgent concrete class initialization
     3. Create interface.py with abstract base classes
     4. Implement ExcuseAgent with Agent initialization in __init__, execute() delegation pattern
     5. Run tests to verify they pass
     6. Lint and format code

2. **Phase 2: Implement GenerateExcuse Operation**
   - **Objective:** Create the operation that generates excuses using the PydanticAI Agent, extracting logic from GetVague.execute()
   - **Files/Functions to Create:**
     - app/utilities/excuse_agent/operations/generate_excuse.py - `GenerateExcuse` class with `execute()` method
   - **Tests to Write:**
     - `test_generate_excuse_with_valid_prompt` - Verify excuse is generated successfully
     - `test_generate_excuse_with_empty_prompt` - Verify InvalidRequestError raised
     - `test_generate_excuse_when_agent_fails` - Verify AIServiceError raised
     - `test_generate_excuse_uses_agent_from_utility` - Verify operation accesses `self.utility.agent`
   - **Steps:**
     1. Write failing tests for GenerateExcuse operation with various scenarios
     2. Create generate_excuse.py implementing `ExcuseAgentOperationABC`
     3. Extract agent.run() logic from GetVague lines 46-62
     4. Implement execute() with prompt validation and error handling
     5. Run tests to verify they pass
     6. Lint and format code

3. **Phase 3: Refactor Repository to Use excuse_agent**
   - **Objective:** Update ExcuseRepository to depend on excuse_agent instead of directly managing PydanticAI Agent
   - **Files/Functions to Modify:**
     - app/repositories/excuse_generator/excuse_repository.py - Remove Agent initialization, add `excuse_agent` dependency
     - app/repositories/excuse_generator/operations/get_vague.py - Delegate to `excuse_agent.execute()`
   - **Tests to Write:**
     - `test_excuse_repository_accepts_excuse_agent` - Verify repository can be initialized with excuse_agent
     - `test_get_vague_delegates_to_excuse_agent` - Verify GetVague calls excuse_agent.execute()
     - `test_get_vague_passes_prompt_correctly` - Verify prompt is passed through correctly
   - **Steps:**
     1. Write failing tests for updated ExcuseRepository interface
     2. Update ExcuseRepository.__init__() to accept `excuse_agent: Optional[ExcuseAgentABC]` parameter
     3. Remove Agent initialization code (lines 32-53)
     4. Update GetVague.execute() to call `self.repository.excuse_agent.execute()`
     5. Update existing repository tests to mock excuse_agent instead of Agent
     6. Run all tests to verify they pass
     7. Lint and format code

4. **Phase 4: Update Service Layer and Create Comprehensive Tests**
   - **Objective:** Ensure GenerateVague service works with refactored repository and create comprehensive test suite for excuse_agent utility
   - **Files/Functions to Modify:**
     - app/services/excuse_generator/operations/generate_vague.py - Verify no changes needed (should work transparently)
   - **Files/Functions to Create:**
     - tests/utilities/__init__.py - Test directory initialization
     - tests/utilities/excuse_agent/__init__.py - Test module init
     - tests/utilities/excuse_agent/test_excuse_agent.py - Complete utility tests
     - tests/utilities/excuse_agent/operations/__init__.py - Operations test init
     - tests/utilities/excuse_agent/operations/test_generate_excuse.py - Operation tests
   - **Tests to Write:**
     - Comprehensive test coverage for excuse_agent utility (≥80%)
     - Integration tests verifying end-to-end flow through service → repository → excuse_agent
   - **Steps:**
     1. Create comprehensive test suite for excuse_agent utility
     2. Create comprehensive test suite for GenerateExcuse operation
     3. Run all tests across the codebase to verify nothing breaks
     4. Verify test coverage meets ≥80% threshold
     5. Run linters and formatters on all files
     6. Final verification that all tests pass
