# 🎣 Git Hooks - Quick Reference

## One-Time Setup

### Windows
```bash
.\scripts\install-hooks.bat
```

### macOS/Linux
```bash
./scripts/install-hooks.sh
```

## What Happens When

### ✅ On `git commit`
- Code formatting (Black)
- Linting (Ruff)
- Security checks (Bandit)
- Type checking (MyPy)

### ✅ On `git push`
- **Full test suite** (93 tests)
- **Coverage check** (50% minimum)
- **Tests must pass** or push is blocked

## Quick Commands

```bash
# Run all checks manually
pre-commit run --all-files

# Run only tests
pytest -v

# Bypass hooks (emergency only)
git push --no-verify
```

## Need Help?

See full documentation: [docs/GIT_HOOKS_SETUP.md](docs/GIT_HOOKS_SETUP.md)
