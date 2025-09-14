# 🔒 Security Best Practices for MCP Servers

## Overview

This document outlines security considerations and best practices when deploying MCP servers, particularly the Forecasting Calculator.

## 🛡️ Key Security Principles

### 1. Never Expose Personal Paths

❌ **BAD - Exposes user directory structure:**
```json
{
  "command": "/Users/johndoe/Desktop/Personal Projects/mcp/server.sh"
}
```

✅ **GOOD - Generic path structure:**
```json
{
  "command": "/opt/mcp-servers/forecasting-calculator/run.sh"
}
```

### 2. Environment Isolation

Always use virtual environments to:
- Prevent dependency conflicts
- Isolate package installations
- Maintain system Python integrity

```bash
# Create isolated environment
python3 -m venv mcp_venv
source mcp_venv/bin/activate
```

### 3. Input Validation

The server implements multiple validation layers:

```python
# Data validation example
def validate_data(data: List[float]) -> Tuple[bool, str]:
    if not data or len(data) < 3:
        return False, "Need at least 3 data points"
    if len(data) > 10000:
        return False, "Data series too large"
    if not all(isinstance(x, (int, float)) for x in data):
        return False, "All data points must be numeric"
    return True, "Valid"
```

### 4. Error Handling

Never expose system internals in error messages:

❌ **BAD - Exposes system path:**
```python
except FileNotFoundError as e:
    return f"Error: {e}"  # May expose full file paths
```

✅ **GOOD - Generic error message:**
```python
except FileNotFoundError:
    return "Configuration file not found"
```

## 🔐 Configuration Security

### File Permissions

Set appropriate permissions for sensitive files:

```bash
# macOS/Linux
chmod 600 claude_desktop_config.json  # Read/write for owner only
chmod 700 run_forecasting_calculator.sh  # Execute for owner only

# Verify permissions
ls -la claude_desktop_config.json
```

### Path Security

1. **Use absolute paths** - Prevents path traversal attacks
2. **Avoid symlinks** - Can be manipulated
3. **Validate paths** - Ensure they exist and are accessible

```python
import os

def validate_path(path: str) -> bool:
    """Validate path is safe and exists"""
    # Resolve to absolute path
    abs_path = os.path.abspath(path)
    
    # Check if path exists and is a file
    if not os.path.isfile(abs_path):
        return False
    
    # Ensure path is within expected directory
    if not abs_path.startswith('/expected/base/path'):
        return False
    
    return True
```

## 🚫 Common Security Mistakes

### 1. Hardcoded Credentials

Never include API keys or passwords in:
- Source code
- Configuration files
- Documentation
- Git commits

Use environment variables instead:

```python
import os

# Good practice
api_key = os.environ.get('FORECAST_API_KEY')

# Never do this
api_key = "sk-1234567890abcdef"  # NEVER!
```

### 2. Unsafe Deserialization

Avoid using `eval()` or `exec()` with user input:

❌ **DANGEROUS:**
```python
result = eval(user_input)  # Can execute arbitrary code
```

✅ **SAFE:**
```python
import json
result = json.loads(user_input)  # Safe JSON parsing
```

### 3. Logging Sensitive Data

Configure logging to exclude sensitive information:

```python
import logging

# Configure safe logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create filter to remove sensitive data
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        # Remove potential sensitive patterns
        if hasattr(record, 'msg'):
            record.msg = record.msg.replace('/Users/', '/path/')
        return True

logger = logging.getLogger(__name__)
logger.addFilter(SensitiveDataFilter())
```

## 🔍 Security Checklist

Before deploying an MCP server, verify:

- [ ] No personal information in documentation
- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] Error messages are generic
- [ ] File permissions are restrictive
- [ ] Virtual environment is used
- [ ] Dependencies are from trusted sources
- [ ] No use of eval/exec with user input
- [ ] Logging doesn't expose sensitive data
- [ ] Configuration files are protected

## 🛠️ Security Tools

### Dependency Scanning

Regularly check for vulnerabilities:

```bash
# Install safety tool
pip install safety

# Scan dependencies
safety check -r requirements.txt
```

### Static Analysis

Use tools to find security issues:

```bash
# Install bandit
pip install bandit

# Run security scan
bandit -r . -ll
```

## 📊 Security Configuration Examples

### Secure Directory Structure

```
/opt/mcp-servers/
├── forecasting-calculator/
│   ├── mcp_venv/           (700)
│   ├── server.py            (644)
│   ├── run.sh               (700)
│   └── config/              (700)
│       └── settings.json    (600)
└── logs/                    (700)
    └── server.log           (600)
```

### Secure Wrapper Script

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Define base directory (no personal paths)
BASE_DIR="/opt/mcp-servers/forecasting-calculator"

# Validate directory exists
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Server directory not found"
    exit 1
fi

# Change to directory
cd "$BASE_DIR" || exit 1

# Activate virtual environment
source mcp_venv/bin/activate || exit 1

# Run with restricted permissions
exec python forecasting_calculator_server.py
```

## 🔄 Regular Security Maintenance

### Weekly Tasks
- Review logs for anomalies
- Check for dependency updates
- Verify file permissions

### Monthly Tasks
- Run security scans
- Update dependencies
- Review access logs

### Quarterly Tasks
- Full security audit
- Update documentation
- Review and rotate any keys

## 🚨 Incident Response

If a security issue is discovered:

1. **Isolate** - Stop the affected server
2. **Assess** - Determine scope of issue
3. **Patch** - Fix the vulnerability
4. **Test** - Verify the fix works
5. **Deploy** - Roll out the update
6. **Document** - Record lessons learned

## 📚 Additional Resources

- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [MCP Security Guidelines](https://modelcontextprotocol.io/docs/security)

---

**Remember:** Security is not a one-time task but an ongoing process. Stay vigilant and keep your systems updated.