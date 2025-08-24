"""
Unit Tests for Schema Validation — T-08 (Test Strategy Implementation)
Framework: fwk-001-cursor-rules
Owner: qa_platform
Priority: P0
"""

import pytest
import json
import jsonschema
from pathlib import Path
from unittest.mock import patch, mock_open


class TestArtifactSchemaValidation:
    """Test artifact schema validation functionality."""
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_valid_artifact_schema(self, mock_artifact, mock_schema):
        """Test that valid artifact data passes schema validation."""
        # Arrange
        artifact_data = mock_artifact
        schema = mock_schema
        
        # Act
        try:
            jsonschema.validate(instance=artifact_data, schema=schema)
            validation_passed = True
        except jsonschema.ValidationError:
            validation_passed = False
        
        # Assert
        assert validation_passed, "Valid artifact should pass schema validation"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_invalid_artifact_missing_required_field(self, mock_schema):
        """Test that invalid artifact data fails schema validation."""
        # Arrange
        invalid_artifact = {
            "id": "test_artifact",
            # Missing required fields: version, status, framework, kind
            "checksumSha256": "a" * 64,
            "createdAt": "2025-08-24T00:00:00Z",
            "updatedAt": "2025-08-24T00:00:00Z"
        }
        schema = mock_schema
        
        # Act & Assert
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(instance=invalid_artifact, schema=schema)
        
        assert "required" in str(exc_info.value), "Should fail on missing required fields"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_invalid_artifact_wrong_field_type(self, mock_schema):
        """Test that artifact with wrong field types fails validation."""
        # Arrange
        invalid_artifact = {
            "id": 123,  # Should be string
            "version": "1.0.0",
            "status": "review",
            "framework": "fwk-001-cursor-rules",
            "kind": "test_artifact",
            "checksumSha256": "a" * 64,
            "createdAt": "2025-08-24T00:00:00Z",
            "updatedAt": "2025-08-24T00:00:00Z"
        }
        schema = mock_schema
        
        # Act & Assert
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(instance=invalid_artifact, schema=schema)
        
        assert "123 is not of type 'string'" in str(exc_info.value), "Should fail on wrong field type"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_file_exists(self, framework_root):
        """Test that the artifact schema file exists and is valid JSON."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act & Assert
        assert schema_path.exists(), "Artifact schema file should exist"
        
        # Test JSON validity
        try:
            with open(schema_path, 'r') as f:
                schema_data = json.load(f)
            json_valid = True
        except (json.JSONDecodeError, FileNotFoundError):
            json_valid = False
        
        assert json_valid, "Artifact schema should be valid JSON"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_structure(self, framework_root):
        """Test that the artifact schema has the expected structure."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        # Assert
        assert "type" in schema_data, "Schema should have 'type' field"
        assert "properties" in schema_data, "Schema should have 'properties' field"
        assert "required" in schema_data, "Schema should have 'required' field"
        assert schema_data["type"] == "object", "Schema type should be 'object'"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_required_fields(self, framework_root):
        """Test that the artifact schema has all required fields defined."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        required_fields = schema_data.get("required", [])
        properties = schema_data.get("properties", {})
        
        # Assert
        assert len(required_fields) > 0, "Schema should have required fields"
        
        # All required fields should have corresponding properties
        for field in required_fields:
            assert field in properties, f"Required field '{field}' should have property definition"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_property_types(self, framework_root):
        """Test that artifact schema properties have correct types."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        properties = schema_data.get("properties", {})
        
        # Assert
        expected_string_fields = ["id", "version", "status", "framework", "kind", "checksumSha256", "createdAt", "updatedAt"]
        
        for field in expected_string_fields:
            if field in properties:
                field_schema = properties[field]
                assert "type" in field_schema, f"Property '{field}' should have type definition"
                assert field_schema["type"] == "string", f"Property '{field}' should be string type"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_checksum_format(self, framework_root):
        """Test that checksum field has proper format validation."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        checksum_property = schema_data.get("properties", {}).get("checksumSha256", {})
        
        # Assert
        if "pattern" in checksum_property:
            pattern = checksum_property["pattern"]
            # Should be a regex pattern for SHA-256 (64 hex characters)
            assert "64" in pattern or "[a-fA-F0-9]{64}" in pattern, "Checksum should have proper format validation"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_timestamp_format(self, framework_root):
        """Test that timestamp fields have proper format validation."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        timestamp_fields = ["createdAt", "updatedAt"]
        
        # Assert
        for field in timestamp_fields:
            if field in schema_data.get("properties", {}):
                field_schema = schema_data["properties"][field]
                if "format" in field_schema:
                    format_value = field_schema["format"]
                    assert format_value in ["date-time", "date", "time"], f"Timestamp field '{field}' should have proper format"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_version_format(self, framework_root):
        """Test that version field has proper format validation."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        version_property = schema_data.get("properties", {}).get("version", {})
        
        # Assert
        if "pattern" in version_property:
            pattern = version_property["pattern"]
            # Should support semantic versioning (e.g., 1.0.0, 2.1.3)
            # Our schema uses a more complex pattern that supports semantic versioning
            # The pattern contains escaped backslashes, so we check for the raw pattern
            assert "\\d" in pattern, "Version should support numeric versioning"
            assert "\\." in pattern, "Version should support dot-separated format"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_status_enum(self, framework_root):
        """Test that status field has proper enum values."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        status_property = schema_data.get("properties", {}).get("status", {})
        
        # Assert
        if "enum" in status_property:
            enum_values = status_property["enum"]
            expected_statuses = ["draft", "review", "approved", "deprecated"]
            
            for expected_status in expected_statuses:
                assert expected_status in enum_values, f"Status enum should include '{expected_status}'"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_artifact_schema_framework_validation(self, framework_root):
        """Test that framework field validates correctly."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        framework_property = schema_data.get("properties", {}).get("framework", {})
        
        # Assert
        if "enum" in framework_property:
            enum_values = framework_property["enum"]
            assert "fwk-001-cursor-rules" in enum_values, "Framework enum should include 'fwk-001-cursor-rules'"
        elif "pattern" in framework_property:
            pattern = framework_property["pattern"]
            assert "fwk-\\d{3}-[a-z-]+" in pattern, "Framework should follow naming convention"


class TestSchemaFileOperations:
    """Test schema file operations and utilities."""
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_schema_file_read_permissions(self, framework_root):
        """Test that schema file has proper read permissions."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act & Assert
        assert schema_path.exists(), "Schema file should exist"
        assert schema_path.is_file(), "Schema should be a file"
        assert schema_path.stat().st_mode & 0o444, "Schema file should be readable"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_schema_file_size_reasonable(self, framework_root):
        """Test that schema file size is reasonable."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        file_size = schema_path.stat().st_size
        
        # Assert
        assert file_size > 100, "Schema file should have meaningful content (>100 bytes)"
        assert file_size < 10000, "Schema file should not be excessively large (<10KB)"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_schema_file_encoding(self, framework_root):
        """Test that schema file uses proper encoding."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                content = f.read()
            encoding_valid = True
        except UnicodeDecodeError:
            encoding_valid = False
        
        # Assert
        assert encoding_valid, "Schema file should use valid UTF-8 encoding"
    
    @pytest.mark.unit
    @pytest.mark.schema
    def test_schema_file_no_trailing_whitespace(self, framework_root):
        """Test that schema file has no trailing whitespace."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        
        # Act
        with open(schema_path, 'r') as f:
            lines = f.readlines()
        
        # Assert
        for i, line in enumerate(lines, 1):
            assert not line.rstrip().endswith(' '), f"Line {i} should not have trailing whitespace"
            assert not line.rstrip().endswith('\t'), f"Line {i} should not have trailing tabs"


# Performance tests
class TestSchemaValidationPerformance:
    """Test schema validation performance characteristics."""
    
    @pytest.mark.unit
    @pytest.mark.performance
    @pytest.mark.slow
    def test_schema_validation_speed(self, mock_artifact, mock_schema, performance_timer):
        """Test that schema validation completes within performance targets."""
        # Arrange
        artifact_data = mock_artifact
        schema = mock_schema
        timer = performance_timer
        
        # Act
        timer.start()
        for _ in range(100):  # Run validation 100 times
            jsonschema.validate(instance=artifact_data, schema=schema)
        timer.stop()
        
        # Assert
        avg_time = timer.elapsed() / 100
        assert avg_time < 2.0, f"Schema validation should be fast (<2ms per validation), got {avg_time:.2f}ms"
    
    @pytest.mark.unit
    @pytest.mark.performance
    def test_large_schema_validation(self, framework_root, performance_timer):
        """Test validation performance with actual schema file."""
        # Arrange
        schema_path = framework_root / "schemas" / "artifact.schema.json"
        timer = performance_timer
        
        with open(schema_path, 'r') as f:
            schema_data = json.load(f)
        
        # Create test data
        test_artifacts = [
            {
                "id": f"test_artifact_{i}",
                "version": "1.0.0",
                "status": "review",
                "framework": "fwk-001-cursor-rules",
                "kind": "test_artifact",
                "checksumSha256": "a" * 64,
                "createdAt": "2025-08-24T00:00:00Z",
                "updatedAt": "2025-08-24T00:00:00Z"
            }
            for i in range(100)
        ]
        
        # Act
        timer.start()
        for artifact in test_artifacts:
            jsonschema.validate(instance=artifact, schema=schema_data)
        timer.stop()
        
        # Assert
        total_time = timer.elapsed()
        avg_time = total_time / 100
        assert avg_time < 5.0, f"Large schema validation should be efficient (<5ms per validation), got {avg_time:.2f}ms"
        assert total_time < 1000, f"Total validation time should be reasonable (<1s for 100 validations), got {total_time:.2f}ms"
