#!/usr/bin/env python3
"""
Security Configuration Validator — T-09 (Security Implementation)
Framework: fwk-001-cursor-rules
Owner: security_platform
Priority: P1
"""

import json
import jsonschema
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime, timezone


class SecurityConfigValidator:
    """Validates security configuration files and policies."""
    
    def __init__(self, framework_root: Path):
        self.framework_root = framework_root
        # If we're already in the security directory, use current directory
        if Path.cwd().name == "security":
            self.security_dir = Path.cwd()
        else:
            self.security_dir = framework_root / "security"
        self.acl_file = self.security_dir / "acl.json"
        self.policies_file = self.security_dir / "access_policies.md"
        
        # Security schema for ACL validation
        self.acl_schema = {
            "type": "object",
            "required": ["version", "framework", "owner", "priority", "roles", "resources"],
            "properties": {
                "version": {"type": "string"},
                "framework": {"type": "string"},
                "owner": {"type": "string"},
                "priority": {"type": "string"},
                "roles": {"type": "object"},
                "resources": {"type": "object"},
                "access_control": {"type": "object"},
                "secrets_management": {"type": "object"},
                "compliance": {"type": "object"}
            }
        }
    
    def validate_acl_structure(self) -> Tuple[bool, List[str]]:
        """Validate ACL JSON structure and required fields."""
        errors = []
        
        try:
            with open(self.acl_file, 'r') as f:
                acl_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            errors.append(f"Failed to load ACL file: {e}")
            return False, errors
        
        # Validate against schema
        try:
            jsonschema.validate(instance=acl_data, schema=self.acl_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"ACL schema validation failed: {e}")
        
        # Check required fields
        required_fields = ["version", "framework", "owner", "priority", "risk_reference"]
        for field in required_fields:
            if field not in acl_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate framework identifier
        if acl_data.get("framework") != "fwk-001-cursor-rules":
            errors.append("Framework identifier mismatch")
        
        # Validate priority
        valid_priorities = ["P0", "P1", "P2", "P3"]
        if acl_data.get("priority") not in valid_priorities:
            errors.append(f"Invalid priority: {acl_data.get('priority')}")
        
        return len(errors) == 0, errors
    
    def validate_roles(self) -> Tuple[bool, List[str]]:
        """Validate role definitions and permissions."""
        errors = []
        
        try:
            with open(self.acl_file, 'r') as f:
                acl_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False, ["Failed to load ACL file"]
        
        roles = acl_data.get("roles", {})
        
        # Check for required roles
        required_roles = ["framework_developer", "qa_engineer", "devops_engineer", "security_analyst", "framework_admin"]
        for role in required_roles:
            if role not in roles:
                errors.append(f"Missing required role: {role}")
        
        # Validate each role
        for role_name, role_config in roles.items():
            if not isinstance(role_config, dict):
                errors.append(f"Invalid role configuration for {role_name}")
                continue
            
            # Check required role fields
            required_role_fields = ["description", "permissions", "authentication"]
            for field in required_role_fields:
                if field not in role_config:
                    errors.append(f"Role {role_name} missing field: {field}")
            
            # Validate permissions structure
            permissions = role_config.get("permissions", {})
            if isinstance(permissions, dict):
                for resource_type, resource_perms in permissions.items():
                    if not isinstance(resource_perms, dict):
                        errors.append(f"Invalid permissions for {role_name}.{resource_type}")
                        continue
                    
                    # Check permission fields
                    perm_fields = ["read", "write", "delete", "admin"]
                    for perm_field in perm_fields:
                        if perm_field not in resource_perms:
                            errors.append(f"Missing permission field {perm_field} in {role_name}.{resource_type}")
            
            # Validate authentication configuration
            auth = role_config.get("authentication", {})
            if isinstance(auth, dict):
                if "mfa_required" not in auth:
                    errors.append(f"Role {role_name} missing MFA configuration")
                if "session_timeout" not in auth:
                    errors.append(f"Role {role_name} missing session timeout")
        
        return len(errors) == 0, errors
    
    def validate_resources(self) -> Tuple[bool, List[str]]:
        """Validate resource definitions and access controls."""
        errors = []
        
        try:
            with open(self.acl_file, 'r') as f:
                acl_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False, ["Failed to load ACL file"]
        
        resources = acl_data.get("resources", {})
        
        # Check for required resource types
        required_resource_types = ["artifacts", "snapshots", "metadata"]
        for resource_type in required_resource_types:
            if resource_type not in resources:
                errors.append(f"Missing required resource type: {resource_type}")
        
        # Validate artifacts configuration
        artifacts = resources.get("artifacts", {})
        if isinstance(artifacts, dict):
            required_artifact_levels = ["public", "internal", "sensitive", "critical"]
            for level in required_artifact_levels:
                if level not in artifacts:
                    errors.append(f"Missing artifact access level: {level}")
                else:
                    artifact_config = artifacts[level]
                    if not isinstance(artifact_config, dict):
                        errors.append(f"Invalid configuration for artifact level: {level}")
                    else:
                        # Check required artifact fields
                        required_artifact_fields = ["path_pattern", "access_level", "encryption", "audit_logging"]
                        for field in required_artifact_fields:
                            if field not in artifact_config:
                                errors.append(f"Artifact level {level} missing field: {field}")
        
        # Validate snapshots configuration
        snapshots = resources.get("snapshots", {})
        if isinstance(snapshots, dict):
            required_snapshot_types = ["promotion", "rollback", "audit"]
            for snapshot_type in required_snapshot_types:
                if snapshot_type not in snapshots:
                    errors.append(f"Missing snapshot type: {snapshot_type}")
        
        return len(errors) == 0, errors
    
    def validate_security_policies(self) -> Tuple[bool, List[str]]:
        """Validate security policy document exists and is readable."""
        errors = []
        
        if not self.policies_file.exists():
            errors.append("Access policies document not found")
            return False, errors
        
        # Check file size (should be substantial)
        file_size = self.policies_file.stat().st_size
        if file_size < 1000:  # Less than 1KB
            errors.append("Access policies document appears too small")
        
        # Check if file is readable
        try:
            with open(self.policies_file, 'r') as f:
                content = f.read()
                if len(content) < 1000:
                    errors.append("Access policies document content too short")
        except Exception as e:
            errors.append(f"Failed to read access policies document: {e}")
        
        return len(errors) == 0, errors
    
    def validate_compliance_standards(self) -> Tuple[bool, List[str]]:
        """Validate compliance standards configuration."""
        errors = []
        
        try:
            with open(self.acl_file, 'r') as f:
                acl_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False, ["Failed to load ACL file"]
        
        compliance = acl_data.get("compliance", {})
        if not isinstance(compliance, dict):
            errors.append("Invalid compliance configuration")
            return False, errors
        
        standards = compliance.get("standards", {})
        if not isinstance(standards, dict):
            errors.append("Invalid compliance standards configuration")
            return False, errors
        
        # Check for required compliance standards
        required_standards = ["gdpr", "soc2", "iso27001"]
        for standard in required_standards:
            if standard not in standards:
                errors.append(f"Missing compliance standard: {standard}")
            else:
                standard_config = standards[standard]
                if not isinstance(standard_config, dict):
                    errors.append(f"Invalid configuration for standard: {standard}")
                elif "enabled" not in standard_config:
                    errors.append(f"Standard {standard} missing enabled field")
        
        return len(errors) == 0, errors
    
    def validate_encryption_config(self) -> Tuple[bool, List[str]]:
        """Validate encryption configuration."""
        errors = []
        
        try:
            with open(self.acl_file, 'r') as f:
                acl_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False, ["Failed to load ACL file"]
        
        # Check metadata encryption standards
        metadata = acl_data.get("metadata", {})
        encryption_standards = metadata.get("encryption_standards", [])
        
        required_encryption_standards = ["AES-256-GCM", "SHA-256"]
        for standard in required_encryption_standards:
            if standard not in encryption_standards:
                errors.append(f"Missing required encryption standard: {standard}")
        
        # Check secrets management encryption
        secrets_mgmt = acl_data.get("secrets_management", {})
        if isinstance(secrets_mgmt, dict):
            encryption = secrets_mgmt.get("encryption", {})
            if not isinstance(encryption, dict):
                errors.append("Invalid secrets management encryption configuration")
            else:
                required_encryption_fields = ["algorithm", "key_derivation", "key_rotation"]
                for field in required_encryption_fields:
                    if field not in encryption:
                        errors.append(f"Secrets management missing encryption field: {field}")
        
        return len(errors) == 0, errors
    
    def validate_incident_response(self) -> Tuple[bool, List[str]]:
        """Validate incident response configuration."""
        errors = []
        
        try:
            with open(self.acl_file, 'r') as f:
                acl_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False, ["Failed to load ACL file"]
        
        incident_response = acl_data.get("incident_response", {})
        if not isinstance(incident_response, dict):
            errors.append("Invalid incident response configuration")
            return False, errors
        
        # Check required incident response sections
        required_sections = ["detection", "response", "notification"]
        for section in required_sections:
            if section not in incident_response:
                errors.append(f"Missing incident response section: {section}")
        
        # Validate notification configuration
        notification = incident_response.get("notification", {})
        if isinstance(notification, dict):
            required_notifications = ["security_team", "stakeholders", "regulatory"]
            for notif_type in required_notifications:
                if notif_type not in notification:
                    errors.append(f"Missing notification type: {notif_type}")
        
        return len(errors) == 0, errors
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete security configuration validation."""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "framework": "fwk-001-cursor-rules",
            "validation": "security_config",
            "overall_status": "PASS",
            "checks": {},
            "errors": [],
            "warnings": []
        }
        
        # Run all validation checks
        validation_checks = [
            ("acl_structure", self.validate_acl_structure),
            ("roles", self.validate_roles),
            ("resources", self.validate_resources),
            ("security_policies", self.validate_security_policies),
            ("compliance_standards", self.validate_compliance_standards),
            ("encryption_config", self.validate_encryption_config),
            ("incident_response", self.validate_incident_response)
        ]
        
        for check_name, check_func in validation_checks:
            try:
                passed, errors = check_func()
                results["checks"][check_name] = {
                    "status": "PASS" if passed else "FAIL",
                    "errors": errors
                }
                
                if not passed:
                    results["overall_status"] = "FAIL"
                    results["errors"].extend(errors)
                
            except Exception as e:
                results["checks"][check_name] = {
                    "status": "ERROR",
                    "errors": [f"Validation error: {e}"]
                }
                results["overall_status"] = "ERROR"
                results["errors"].append(f"Check {check_name} failed: {e}")
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable validation report."""
        report = []
        report.append("=" * 60)
        report.append("SECURITY CONFIGURATION VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"Framework: {results['framework']}")
        report.append(f"Timestamp: {results['timestamp']}")
        report.append(f"Overall Status: {results['overall_status']}")
        report.append("")
        
        # Summary of checks
        report.append("VALIDATION CHECKS SUMMARY:")
        report.append("-" * 40)
        for check_name, check_result in results["checks"].items():
            status = check_result["status"]
            error_count = len(check_result["errors"])
            report.append(f"{check_name:.<30} {status} ({error_count} errors)")
        report.append("")
        
        # Detailed results
        if results["errors"]:
            report.append("DETAILED ERRORS:")
            report.append("-" * 40)
            for i, error in enumerate(results["errors"], 1):
                report.append(f"{i}. {error}")
            report.append("")
        
        # Recommendations
        if results["overall_status"] == "FAIL":
            report.append("RECOMMENDATIONS:")
            report.append("-" * 40)
            report.append("1. Review and fix all validation errors")
            report.append("2. Ensure all required security policies are in place")
            report.append("3. Validate compliance with organizational standards")
            report.append("4. Test security controls in non-production environment")
        elif results["overall_status"] == "PASS":
            report.append("VALIDATION SUCCESSFUL!")
            report.append("-" * 40)
            report.append("All security configuration checks passed.")
            report.append("Security policies are properly configured.")
        
        report.append("=" * 60)
        return "\n".join(report)


def main():
    """Main validation function."""
    if len(sys.argv) > 1:
        framework_root = Path(sys.argv[1])
    else:
        framework_root = Path.cwd()
    
    if not framework_root.exists():
        print(f"Error: Framework root directory not found: {framework_root}")
        sys.exit(1)
    
    # Use current directory for results
    security_dir = Path.cwd()
    
    # Initialize validator
    validator = SecurityConfigValidator(framework_root)
    
    # Run validation
    print("Running security configuration validation...")
    results = validator.run_full_validation()
    
    # Generate and display report
    report = validator.generate_report(results)
    print(report)
    
    # Save results to file
    results_file = security_dir / "validation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nValidation results saved to: {results_file}")
    
    # Exit with appropriate code
    if results["overall_status"] == "PASS":
        print("✅ Security configuration validation PASSED")
        sys.exit(0)
    else:
        print("❌ Security configuration validation FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
