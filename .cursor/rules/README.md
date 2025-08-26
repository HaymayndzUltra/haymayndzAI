# Cursor Rules System

## Overview
This directory contains a comprehensive set of Cursor Rules that provide guidance for AI-assisted development across multiple technology stacks and development phases.

## Rule Architecture

### Core Rules (Always Applied)
These rules provide fundamental development standards and are always active:

- **[Development Excellence](mdc:.cursor/rules/development-excellence.mdc)** - Master rule covering all development aspects
- **[AI System Architecture](mdc:.cursor/rules/ai-system-architecture.mdc)** - AI role system and memory management
- **[Development Workflow](mdc:.cursor/rules/development-workflow.mdc)** - Pipeline and quality gate management
- **[Security and Compliance](mdc:.cursor/rules/security-and-compliance.mdc)** - Security standards and compliance requirements
- **[Testing and Quality](mdc:.cursor/rules/testing-and-quality.mdc)** - Quality assurance and testing standards

### Technology-Specific Rules
These rules provide guidance for specific technologies and frameworks:

- **[Python Development Standards](mdc:.cursor/rules/python-development-standards.mdc)** - Python coding standards and best practices
- **[Technology Stack Rules](mdc:.cursor/rules/technology-stacks.mdc)** - Master index of all technology-specific rules

### Management and Organization
These rules help manage and maintain the rule system:

- **[Test Rules Management](mdc:.cursor/rules/test-rules-management.mdc)** - Organization and maintenance of test rules
- **[Project Guidance](mdc:.cursor/rules/project-guidance.mdc)** - Domain-specific AI assistant behavior

## Quick Start

### 1. For New Projects
1. Start with [Development Excellence](mdc:.cursor/rules/development-excellence.mdc)
2. Add [Python Development Standards](mdc:.cursor/rules/python-development-standards.mdc) for Python projects
3. Reference [Technology Stack Rules](mdc:.cursor/rules/technology-stacks.mdc) for framework-specific guidance

### 2. For Specific Technologies
1. Check [Technology Stack Rules](mdc:.cursor/rules/technology-stacks.mdc) for your technology
2. Apply relevant framework-specific rules from `.cursor/test-rules/`
3. Ensure compliance with [Security and Compliance](mdc:.cursor/rules/security-and-compliance.mdc)

### 3. For Development Phases
1. **Planning**: Use [Development Workflow](mdc:.cursor/rules/development-workflow.mdc) and [AI System Architecture](mdc:.cursor/rules/ai-system-architecture.mdc)
2. **Development**: Apply [Python Development Standards](mdc:.cursor/rules/python-development-standards.mdc) and technology-specific rules
3. **Testing**: Follow [Testing and Quality](mdc:.cursor/rules/testing-and-quality.mdc) guidelines
4. **Deployment**: Use [Development Workflow](mdc:.cursor/rules/development-workflow.mdc) deployment phase guidance

## Rule Categories

### Development Standards
- Code quality and formatting
- Testing requirements and coverage
- Documentation standards
- Performance considerations
- Security best practices

### AI System Integration
- Role coordination and handoffs
- Memory management and persistence
- Workflow execution and quality gates
- Error handling and recovery

### Technology Support
- **Python**: FastAPI, Django, Flask, ML, Security
- **JavaScript/TypeScript**: React, Vue, Svelte, Node.js, Mobile
- **PHP**: Laravel, WordPress, WooCommerce
- **Other Languages**: Rust, Go, Java, Kotlin, Swift
- **Blockchain**: Solidity, Solana, OnchainKit
- **Game Development**: Unity, Pixi.js, Three.js
- **Enterprise**: Salesforce, Shopify, Drupal

### Security and Compliance
- Defense in depth principles
- Data protection and encryption
- Access control and authentication
- GDPR, CCPA, HIPAA compliance
- Security testing and incident response

## Usage Examples

### Example 1: Python Web Development
```python
# This code follows our Python Development Standards
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class UserModel(BaseModel):
    """User data model with validation"""
    id: int
    name: str
    email: str
    is_active: bool = True

def create_user(user_data: Dict[str, Any]) -> UserModel:
    """Create a new user with proper validation"""
    try:
        user = UserModel(**user_data)
        # Use atomic operations for database writes
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Example 2: Security Implementation
```python
import hashlib
import secrets
from typing import Optional

class SecureAuth:
    """Secure authentication following our security standards"""
    
    def __init__(self):
        self.salt_length = 32
        self.hash_iterations = 100000
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt using PBKDF2"""
        salt = secrets.token_hex(self.salt_length)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            self.hash_iterations
        )
        return f"{salt}:{hash_obj.hex()}"
```

### Generate Cursor Rules (Curated Library)
Run from repo root to promote curated `.cursor/test-rules` into `.cursor/rules` based on detected markers:
```bash
python tools/generate_cursor_rules.py --lint
```
This runs detector → selector → linter and prints a JSON summary.

## Best Practices

### 1. Rule Selection
- **Start with core rules** for fundamental guidance
- **Add technology rules** based on your project stack
- **Consider security rules** for all projects
- **Use testing rules** to ensure quality

### 2. Rule Maintenance
- **Regular updates** based on technology changes
- **Performance monitoring** to ensure efficiency
- **User feedback** incorporation
- **Version control** for rule evolution

### 3. Rule Integration
- **Avoid conflicts** between overlapping rules
- **Maintain consistency** across technology stacks
- **Update references** when rules change
- **Document dependencies** between rules

## Troubleshooting

### Common Issues

#### Rule Not Applying
1. Check file extension (must be `.mdc`)
2. Verify frontmatter format
3. Ensure proper file location
4. Check for syntax errors

#### Rule Conflicts
1. Review rule priorities
2. Check for overlapping guidance
3. Resolve conflicts in favor of security/quality
4. Document resolution decisions

#### Performance Issues
1. Monitor rule response times
2. Check for infinite loops or recursion
3. Validate rule complexity
4. Optimize rule content

### Getting Help
1. Check [Test Rules Management](mdc:.cursor/rules/test-rules-management.mdc) for organization guidance
2. Review [AI System Architecture](mdc:.cursor/rules/ai-system-architecture.mdc) for system understanding
3. Use [Development Workflow](mdc:.cursor/rules/development-workflow.mdc) for process guidance
4. Reference [Project Guidance](mdc:.cursor/rules/project-guidance.mdc) for domain-specific help

## Contributing

### Adding New Rules
1. **Create in test-rules** directory first
2. **Test thoroughly** with real projects
3. **Validate format** and content
4. **Update indexes** and references
5. **Move to main rules** when ready

### Updating Existing Rules
1. **Version control** all changes
2. **Test updates** before deployment
3. **Update references** and dependencies
4. **Document changes** and rationale

### Rule Review Process
1. **Content review** for accuracy
2. **Format validation** for Cursor compatibility
3. **Performance testing** for efficiency
4. **User feedback** incorporation

## Resources

### Internal Documentation
- [Cursor Rules Directory](mdc:.cursor/rules/)
- [Test Rules Directory](mdc:.cursor/test-rules/)
- [AI System Documentation](mdc:.cursor/docs/)

### External Resources
- **OWASP**: Web application security
- **NIST**: Cybersecurity framework
- **ISO 27001**: Information security management
- **Agile Manifesto**: Development methodology

### Support and Maintenance
- **Regular Reviews**: Monthly rule assessments
- **Performance Monitoring**: Continuous optimization
- **User Training**: Team adoption support
- **Documentation Updates**: Continuous improvement

## Conclusion

The Cursor Rules System provides comprehensive guidance for AI-assisted development across multiple technology stacks. By following these rules, developers can ensure high-quality, secure, and maintainable code while leveraging the full power of AI assistance.

**Remember**: Rules are tools to enhance development, not constraints to limit creativity. Use them wisely and adapt them to your specific project needs while maintaining the core principles of quality, security, and excellence.
