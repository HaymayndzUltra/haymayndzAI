"""
Pytest Configuration and Fixtures — T-08 (Test Strategy Implementation)
Framework: fwk-001-cursor-rules
Owner: qa_platform
Priority: P0
"""

import os
import sys
import tempfile
import shutil
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Add framework root to Python path
FRAMEWORK_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(FRAMEWORK_ROOT))

# Test configuration
TEST_ARTIFACTS_DIR = FRAMEWORK_ROOT / "tests" / "fixtures" / "test_artifacts"
TEST_DATA_DIR = FRAMEWORK_ROOT / "tests" / "fixtures" / "test_data"


@pytest.fixture(scope="session")
def framework_root():
    """Return the framework root directory."""
    return FRAMEWORK_ROOT


@pytest.fixture(scope="session")
def test_artifacts_dir():
    """Return the test artifacts directory."""
    return TEST_ARTIFACTS_DIR


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the test data directory."""
    return TEST_DATA_DIR


@pytest.fixture(scope="function")
def temp_dir():
    """Create a temporary directory for test isolation."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def mock_artifact():
    """Create a mock artifact for testing."""
    return {
        "id": "test_artifact",
        "version": "1.0.0",
        "status": "review",
        "framework": "fwk-001-cursor-rules",
        "kind": "test_artifact",
        "checksumSha256": "a" * 64,
        "createdAt": "2025-08-24T00:00:00Z",
        "updatedAt": "2025-08-24T00:00:00Z"
    }


@pytest.fixture(scope="function")
def mock_schema():
    """Create a mock JSON schema for testing."""
    return {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "version": {"type": "string"},
            "status": {"type": "string"},
            "framework": {"type": "string"},
            "kind": {"type": "string"},
            "checksumSha256": {"type": "string"},
            "createdAt": {"type": "string"},
            "updatedAt": {"type": "string"}
        },
        "required": ["id", "version", "status", "framework", "kind"]
    }


@pytest.fixture(scope="function")
def mock_contract():
    """Create a mock framework contract for testing."""
    return {
        "framework": "fwk-001-cursor-rules",
        "version": "1.0.0",
        "artifacts": ["routing", "hydration", "contracts", "promotion"],
        "rules": ["schema_validation", "contract_enforcement"],
        "tests": ["unit", "contract", "e2e"]
    }


@pytest.fixture(scope="function")
def sample_md_file(temp_dir):
    """Create a sample Markdown file for testing."""
    md_file = Path(temp_dir) / "sample.md"
    md_file.write_text("# Sample Document\n\nThis is a test document.")
    return md_file


@pytest.fixture(scope="function")
def sample_sidecar_file(temp_dir):
    """Create a sample sidecar JSON file for testing."""
    sidecar_file = Path(temp_dir) / "sample.md.sidecar.json"
    sidecar_data = {
        "id": "sample",
        "version": "1.0.0",
        "status": "review",
        "framework": "fwk-001-cursor-rules",
        "kind": "document",
        "checksumSha256": "b" * 64,
        "createdAt": "2025-08-24T00:00:00Z",
        "updatedAt": "2025-08-24T00:00:00Z"
    }
    sidecar_file.write_text(json.dumps(sidecar_data, indent=2))
    return sidecar_file


@pytest.fixture(scope="function")
def mock_file_system(temp_dir):
    """Create a mock file system structure for testing."""
    # Create directory structure
    (Path(temp_dir) / "routing").mkdir(exist_ok=True)
    (Path(temp_dir) / "hydration").mkdir(exist_ok=True)
    (Path(temp_dir) / "contracts").mkdir(exist_ok=True)
    (Path(temp_dir) / "promotion").mkdir(exist_ok=True)
    (Path(temp_dir) / "schemas").mkdir(exist_ok=True)
    
    # Create sample files
    (Path(temp_dir) / "routing" / "artifact_routing.mdc").write_text("# Routing Rules")
    (Path(temp_dir) / "hydration" / "hydration_rules.mdc").write_text("# Hydration Rules")
    (Path(temp_dir) / "contracts" / "framework_contract.mdc").write_text("# Framework Contract")
    (Path(temp_dir) / "promotion" / "promotion_rules.mdc").write_text("# Promotion Rules")
    (Path(temp_dir) / "schemas" / "artifact.schema.json").write_text('{"type": "object"}')
    
    return temp_dir


@pytest.fixture(scope="function")
def mock_index_data():
    """Create mock index data for testing."""
    return {
        "artifacts": [
            {
                "id": "artifact_1",
                "version": "1.0.0",
                "status": "approved",
                "framework": "fwk-001-cursor-rules",
                "kind": "routing",
                "checksumSha256": "c" * 64,
                "createdAt": "2025-08-24T00:00:00Z",
                "updatedAt": "2025-08-24T00:00:00Z"
            },
            {
                "id": "artifact_2",
                "version": "1.0.0",
                "status": "review",
                "framework": "fwk-001-cursor-rules",
                "kind": "hydration",
                "checksumSha256": "d" * 64,
                "createdAt": "2025-08-24T00:00:00Z",
                "updatedAt": "2025-08-24T00:00:00Z"
            }
        ],
        "metadata": {
            "version": "1.0.0",
            "last_updated": "2025-08-24T00:00:00Z",
            "total_artifacts": 2
        }
    }


@pytest.fixture(scope="function")
def mock_environment_variables():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        "TEST_ENVIRONMENT": "test",
        "PYTHONPATH": str(FRAMEWORK_ROOT),
        "COVERAGE_FILE": ".coverage.test"
    }):
        yield


@pytest.fixture(scope="function")
def performance_timer():
    """Simple performance timer for testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            
        def start(self):
            self.start_time = time.time()
            
        def stop(self):
            self.end_time = time.time()
            
        def elapsed(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time) * 1000  # Convert to milliseconds
            return 0
    
    return Timer()


# Test markers for categorization
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "contract: Contract validation tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, external deps)"
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end workflow tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer than 1 second"
    )
    config.addinivalue_line(
        "markers", "performance: Performance benchmark tests"
    )
    config.addinivalue_line(
        "markers", "security: Security-related tests"
    )
    config.addinivalue_line(
        "markers", "schema: Schema validation tests"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "contract" in str(item.fspath):
            item.add_marker(pytest.mark.contract)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        
        # Add slow marker for tests that might be slow
        if "performance" in str(item.fspath) or "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.slow)


# Test result hooks
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom summary information."""
    # Coverage summary
    if hasattr(terminalreporter, '_cov_controller'):
        terminalreporter.write_sep("=", "Coverage Summary")
        terminalreporter.write_line(f"Coverage: {terminalreporter._cov_controller.cov.get_coverage()}")
    
    # Performance summary
    if hasattr(terminalreporter, '_benchmark'):
        terminalreporter.write_sep("=", "Performance Summary")
        terminalreporter.write_line("Performance benchmarks completed")


# Cleanup hooks
def pytest_sessionfinish(session, exitstatus):
    """Clean up after test session."""
    # Remove temporary files
    temp_files = [
        ".coverage.test",
        "test-results.xml",
        "test-results.html",
        "coverage.json",
        "coverage.xml"
    ]
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass
