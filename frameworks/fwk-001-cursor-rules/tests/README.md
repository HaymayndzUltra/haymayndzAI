# Test Implementation — T-08 (Test Strategy)

## Overview

This directory contains the complete test implementation for **T-08: Test Strategy (Unit/Contract/E2E/Gates)** of the fwk-001-cursor-rules framework.

## Test Strategy

### Test Pyramid
```
    E2E Tests (10%)
   /           \
  /             \
Contract Tests (20%)
  \             /
   \           /
  Unit Tests (70%)
```

### Test Categories

1. **Unit Tests (70%)** - Fast, isolated tests for individual functions
2. **Contract Tests (20%)** - Interface and schema validation tests  
3. **E2E Tests (10%)** - Complete workflow and integration tests

## Directory Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_schema_validation.py
│   ├── test_routing.py
│   ├── test_hydration.py
│   ├── test_contracts.py
│   └── test_sync.py
├── contract/                # Contract validation tests
│   ├── test_schemas.py
│   └── test_contracts.py
├── e2e/                     # End-to-end workflow tests
│   ├── test_workflows.py
│   └── test_integration.py
├── fixtures/                # Test data and artifacts
│   ├── test_artifacts/
│   └── test_data/
└── README.md               # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd frameworks/fwk-001-cursor-rules
pip install -r requirements-test.txt
```

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -v

# Contract tests only  
pytest tests/contract/ -v

# E2E tests only
pytest tests/e2e/ -v
```

### 4. Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html --cov-fail-under=80
```

## Test Markers

Use pytest markers to run specific test types:

```bash
# Run unit tests
pytest -m unit

# Run contract tests
pytest -m contract

# Run E2E tests
pytest -m e2e

# Run performance tests
pytest -m performance

# Run schema tests
pytest -m schema

# Run slow tests
pytest -m slow
```

## Test Fixtures

Common fixtures available in `conftest.py`:

- `framework_root` - Framework root directory
- `temp_dir` - Temporary directory for test isolation
- `mock_artifact` - Sample artifact data
- `mock_schema` - Sample JSON schema
- `mock_contract` - Sample framework contract
- `sample_md_file` - Sample Markdown file
- `sample_sidecar_file` - Sample sidecar JSON
- `mock_file_system` - Mock file system structure
- `performance_timer` - Performance measurement utility

## Writing Tests

### Unit Test Example

```python
import pytest

class TestExample:
    @pytest.mark.unit
    def test_function_behavior(self, mock_artifact):
        # Arrange
        input_data = mock_artifact
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result is not None
        assert result["status"] == "success"
```

### Contract Test Example

```python
import pytest
import jsonschema

class TestContractValidation:
    @pytest.mark.contract
    def test_schema_compliance(self, mock_artifact, mock_schema):
        # Act & Assert
        jsonschema.validate(instance=mock_artifact, schema=mock_schema)
```

### E2E Test Example

```python
import pytest
import subprocess

class TestEndToEndWorkflow:
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_complete_workflow(self, temp_dir):
        # Arrange
        setup_test_environment(temp_dir)
        
        # Act
        result = subprocess.run([
            "python3", "main_script.py",
            "--input", str(temp_dir / "input"),
            "--output", str(temp_dir / "output")
        ], capture_output=True, text=True)
        
        # Assert
        assert result.returncode == 0
        assert "success" in result.stdout
```

## Performance Testing

### Performance Targets

- **Unit Tests:** <100ms per test
- **Contract Tests:** <500ms per test  
- **E2E Tests:** <5s per workflow
- **Full Suite:** <2 minutes total

### Performance Test Example

```python
@pytest.mark.performance
def test_function_performance(self, performance_timer):
    timer = performance_timer
    
    timer.start()
    result = function_under_test()
    timer.stop()
    
    assert timer.elapsed() < 100, "Function should complete within 100ms"
```

## Coverage Requirements

### Coverage Targets

- **Minimum:** 80%
- **Target:** 85%
- **Critical:** 75%

### Coverage Commands

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Check coverage threshold
pytest --cov=. --cov-fail-under=80

# Generate multiple report formats
pytest --cov=. --cov-report=html --cov-report=json --cov-report=xml
```

## CI Integration

### Pre-commit Hooks

The test suite integrates with pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### CI Pipeline

Tests run automatically in CI with these gates:

1. **Pre-commit:** Unit tests on changed files
2. **Pull Request:** All tests + coverage check
3. **Release:** Full test suite + performance benchmarks

## Test Data Management

### Fixtures Directory

```
fixtures/
├── test_artifacts/         # Sample artifacts for testing
│   ├── sample.md
│   ├── sample.mdc
│   └── sample.json
└── test_data/              # Test data sets
    ├── valid_artifacts.json
    ├── invalid_artifacts.json
    └── edge_cases.json
```

### Creating Test Data

```python
@pytest.fixture
def custom_test_data():
    return {
        "valid_cases": [...],
        "invalid_cases": [...],
        "edge_cases": [...]
    }
```

## Troubleshooting

### Common Issues

1. **Import Errors:** Ensure `PYTHONPATH` includes framework root
2. **Fixture Not Found:** Check fixture scope and dependencies
3. **Test Isolation:** Use `temp_dir` fixture for file operations
4. **Performance Failures:** Check system load and adjust thresholds

### Debug Commands

```bash
# Run single test with verbose output
pytest tests/unit/test_example.py::TestExample::test_function -v -s

# Run with debug logging
pytest --log-cli-level=DEBUG

# Run with coverage and show missing lines
pytest --cov=. --cov-report=term-missing
```

## Best Practices

### Test Design

1. **Arrange-Act-Assert:** Clear test structure
2. **Descriptive Names:** Test names should explain what is tested
3. **Single Responsibility:** Each test should test one thing
4. **Isolation:** Tests should not depend on each other

### Test Data

1. **Use Fixtures:** Reusable test data and setup
2. **Mock External Dependencies:** Avoid network calls in tests
3. **Clean Up:** Always clean up after tests
4. **Realistic Data:** Use realistic but minimal test data

### Performance

1. **Fast Execution:** Unit tests should be fast
2. **Parallel Execution:** Use pytest-xdist for parallel runs
3. **Resource Management:** Clean up resources properly
4. **Benchmarking:** Track performance over time

## Contributing

### Adding New Tests

1. Create test file in appropriate directory
2. Use existing fixtures when possible
3. Add appropriate markers
4. Ensure test isolation
5. Update this README if needed

### Test Review Checklist

- [ ] Tests are isolated and don't depend on each other
- [ ] Tests use appropriate fixtures
- [ ] Tests have descriptive names
- [ ] Tests include proper assertions
- [ ] Tests handle edge cases
- [ ] Tests meet performance targets
- [ ] Tests have appropriate markers

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [JSON Schema Validation](https://python-jsonschema.readthedocs.io/)
- [Test Strategy Best Practices](https://martinfowler.com/articles/practical-test-pyramid.html)

## Support

For questions about the test implementation:

1. Check this README first
2. Review existing test examples
3. Check pytest documentation
4. Contact the QA platform team

---

**Last Updated:** 2025-08-24  
**Version:** 1.0  
**Owner:** qa_platform  
**Priority:** P0
