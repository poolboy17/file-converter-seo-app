# Git Hooks Setup Guide

## Overview

This project uses git hooks to ensure code quality and prevent broken code from being pushed. The hooks run automatically at different stages of your git workflow.

## What Gets Checked

### On `git commit` (Pre-commit)
- ✅ **Code Formatting** (Black)
- ✅ **Linting** (Ruff)
- ✅ **Security Checks** (Bandit)
- ✅ **Type Checking** (MyPy)
- ✅ **File Checks** (trailing whitespace, large files, etc.)

### On `git push` (Pre-push)
- ✅ **Full Test Suite** (pytest)
- ✅ **Code Coverage** (minimum 50% required)
- ✅ **93 tests** must pass

## Quick Start

### One-Time Setup

#### On Windows:
```bash
.\scripts\install-hooks.bat
```

#### On macOS/Linux:
```bash
chmod +x scripts/install-hooks.sh
./scripts/install-hooks.sh
```

That's it! The hooks are now active.

## Manual Installation

If you prefer to install manually:

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install --install-hooks
pre-commit install --hook-type pre-push

# Test the setup
pre-commit run --all-files
```

## How It Works

### Pre-commit Hook

When you run `git commit`, the following happens automatically:

1. **Black** formats your Python code
2. **Ruff** checks for linting issues and auto-fixes them
3. **Bandit** scans for security vulnerabilities
4. **MyPy** performs type checking
5. **Pre-commit hooks** check for common issues:
   - Trailing whitespace
   - Large files (>5MB)
   - Merge conflicts
   - Invalid YAML/JSON/TOML
   - Private keys

If any check fails, the commit is aborted and you must fix the issues.

### Pre-push Hook

When you run `git push`, the following happens:

1. **Pytest** runs the entire test suite (93 tests)
2. **Coverage** is calculated and must be ≥50%
3. Tests run with verbose output showing which tests pass/fail

If any test fails or coverage is too low, the push is aborted.

## Example Workflow

### Successful Commit
```bash
$ git add .
$ git commit -m "Add new feature"

🧪 Running pre-push checks...

black....................................................................Passed
ruff.....................................................................Passed
bandit...................................................................Passed
mypy.....................................................................Passed
trailing-whitespace......................................................Passed
end-of-file-fixer........................................................Passed
check-yaml...............................................................Passed
check-json...............................................................Passed

[main abc1234] Add new feature
 2 files changed, 50 insertions(+), 10 deletions(-)
```

### Successful Push
```bash
$ git push origin main

🧪 Running pre-push checks...

Running test suite...

======================== test session starts =========================
collected 93 items

tests/converters/test_csv_converter.py .......... PASSED
tests/converters/test_txt_converter.py ........ PASSED
tests/converters/test_docx_converter.py .... PASSED
tests/converters/test_wxr_converter.py ...... PASSED
tests/utils/test_frontmatter_generator.py ................... PASSED
tests/utils/test_file_utils.py ........... PASSED
tests/utils/test_seo_enhancer.py ........... PASSED
tests/utils/test_image_handler.py ....... PASSED
tests/integration/test_conversion_pipeline.py ............ PASSED

======================= 93 passed in 2.14s =======================

Coverage: 52%

✅ All tests passed! Proceeding with push.

Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
...
```

### Failed Push (Tests Failing)
```bash
$ git push origin main

🧪 Running pre-push checks...

Running test suite...

======================== test session starts =========================
FAILED tests/converters/test_csv_converter.py::test_convert_basic_csv

❌ Tests failed! Push aborted.

Please fix the failing tests before pushing.
You can run tests locally with: pytest -v

To bypass this check (NOT RECOMMENDED), use: git push --no-verify
```

## Bypassing Hooks

**⚠️ NOT RECOMMENDED** - Only use in emergencies

### Skip commit hooks:
```bash
git commit --no-verify -m "Emergency fix"
```

### Skip push hooks:
```bash
git push --no-verify
```

## Configuration Files

### `.pre-commit-config.yaml`
Main configuration file for all pre-commit hooks. Defines:
- Which tools to run
- Tool versions
- Arguments for each tool
- When to run (commit vs push)

### `.git/hooks/pre-push`
Bash script that runs pytest before allowing a push.

### `pytest.ini`
Pytest configuration including:
- Coverage requirements (50%)
- Test discovery patterns
- Coverage report formats

## Troubleshooting

### Hooks not running

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install --install-hooks
pre-commit install --hook-type pre-push
```

### Tests failing locally

```bash
# Run tests to see what's failing
pytest -v

# Run with detailed output
pytest -v --tb=long

# Run only failed tests
pytest --lf
```

### Hooks taking too long

```bash
# Skip slow tests during commit (they'll still run on push)
pytest -m "not slow"

# Or temporarily disable
git commit --no-verify
```

### Update hook versions

```bash
# Update to latest versions
pre-commit autoupdate

# Install updated hooks
pre-commit install --install-hooks
```

## Best Practices

### 1. Run Tests Before Committing
```bash
# Run tests locally first
pytest -v

# Then commit
git add .
git commit -m "Your message"
```

### 2. Keep Commits Small
Small commits = faster hook execution

### 3. Fix Issues Immediately
Don't bypass hooks - fix the issues instead

### 4. Use Branches
```bash
# Work on feature branch
git checkout -b feature/new-feature

# Test your changes
pytest -v

# Commit and push
git commit -m "Add feature"
git push origin feature/new-feature
```

### 5. Run Hooks Manually
```bash
# Run all pre-commit hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run pytest --hook-stage push
```

## CI/CD Integration

These hooks complement your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -v --cov=converters --cov=utils --cov-fail-under=50
```

## What Gets Tested

### Converter Tests (28 tests)
- CSV conversion (95% coverage)
- TXT conversion (78% coverage)
- DOCX conversion (56% coverage)
- WXR conversion (73% coverage)

### Utils Tests (53 tests)
- Frontmatter generation (82% coverage)
- SEO enhancement (87% coverage)
- File utilities (48% coverage)
- Image handling (25% coverage)

### Integration Tests (12 tests)
- Complete conversion pipelines
- Multi-file processing
- Error handling
- Unicode support

## Customization

### Change Coverage Requirement

Edit `pytest.ini`:
```ini
addopts =
    --cov-fail-under=70  # Increase to 70%
```

### Add More Hooks

Edit `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/your/hook
    rev: v1.0.0
    hooks:
      - id: your-hook
```

### Skip Specific Hooks

```bash
# Skip only bandit
SKIP=bandit git commit -m "message"

# Skip multiple hooks
SKIP=bandit,mypy git commit -m "message"
```

## Additional Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Project Testing Guide](../tests/README.md)
- [Testing Summary](../TESTING_SUMMARY.md)

## Support

If you encounter issues:

1. Check this guide
2. Run `pre-commit run --all-files` for detailed output
3. Check the logs in `.git/hooks/`
4. Reinstall hooks with the installation script

---

**Remember**: These hooks are here to help maintain code quality and prevent bugs from reaching production. Embrace them! 🚀
