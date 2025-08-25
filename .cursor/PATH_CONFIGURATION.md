# Path Configuration Guide

## 🎯 Problem
Different environments have different root paths:
- **Local:** `/home/haymayndz/HaymayndzAI/`
- **AI Workspace:** `/workspace/`
- **Cloud/Container:** `/app/` or `/code/`

## 🔧 Solution: Environment Variables + Relative Paths

### **1. Set Environment Variable (Recommended)**
```bash
# In your local environment
export REPO_ROOT="/home/haymayndz/HaymayndzAI"

# Or in AI workspace
export REPO_ROOT="/workspace"
```

### **2. Use Relative Paths (Always Works)**
Instead of absolute paths, use relative paths from project root:
```bash
# ❌ Don't use absolute paths
/home/haymayndz/HaymayndzAI/.cursor/rules/
/workspace/.cursor/rules/

# ✅ Use relative paths (works everywhere)
.cursor/rules/
memory-bank/plan/
frameworks/fwk-001-cursor-rules/
```

### **3. Scripts Auto-Detect Environment**
The `auto_restore_templates.py` script automatically detects:
1. **REPO_ROOT** environment variable (if set)
2. **/workspace** directory (AI workspace)
3. **Current working directory** (fallback)

## 📁 File Structure (Use Relative Paths)
```
.cursor/
├── rules/                    # ✅ .cursor/rules/
├── PATH_CONFIGURATION.md     # This file
└── paths.env                 # Environment config

memory-bank/
├── plan/                     # ✅ memory-bank/plan/
├── storage/                  # ✅ memory-bank/storage/
└── queue-system/             # ✅ memory-bank/queue-system/

frameworks/
└── fwk-001-cursor-rules/    # ✅ frameworks/fwk-001-cursor-rules/
    ├── templates/            # ✅ frameworks/fwk-001-cursor-rules/templates/
    ├── examples/             # ✅ frameworks/fwk-001-cursor-rules/examples/
    └── DOCS/                 # ✅ frameworks/fwk-001-cursor-rules/DOCS/
```

## 🚀 Best Practices

### **For Documentation:**
- Use relative paths: `.cursor/rules/`
- Document both environments if needed
- Reference `$REPO_ROOT` for flexibility

### **For Scripts:**
- Use `Path.cwd()` or environment detection
- Always resolve relative to project root
- Handle both local and workspace paths

### **For AI Instructions:**
- Specify relative paths from project root
- Use environment variables when possible
- Avoid hardcoded absolute paths

## 🔍 Environment Detection Example
```python
def resolve_repo_root() -> Path:
    # 1. Check environment variable
    env_root = os.getenv("REPO_ROOT")
    if env_root:
        return Path(env_root).resolve()
    
    # 2. Check AI workspace
    workspace = Path("/workspace")
    if workspace.exists():
        return workspace.resolve()
    
    # 3. Fallback to current directory
    return Path.cwd().resolve()
```

## 📝 Summary
- **Use relative paths** from project root
- **Set REPO_ROOT** environment variable for flexibility
- **Scripts auto-detect** environment
- **Document both paths** when necessary
- **Avoid hardcoded absolute paths**
