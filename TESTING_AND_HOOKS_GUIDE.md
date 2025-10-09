# 🧪 Complete Testing & Git Hooks Guide

## 🎯 Executive Summary

This project now has:
- ✅ **93 passing tests** with **52% code coverage**
- ✅ **Automated pre-push hooks** that run tests before every push
- ✅ **Pre-commit hooks** for code quality (formatting, linting, security)
- ✅ **Modern best practices** following industry standards

## 🚀 Quick Start (5 Minutes)

### 1. Install Testing Dependencies
```bash
pip install pytest pytest-cov pytest-mock pillow
```

### 2. Setup Git Hooks
```bash
# Windows
.\scripts\install-hooks.bat

# macOS/Linux
./scripts/install-hooks.sh
```

### 3. Verify Setup
```bash
# Run tests
pytest -v

# Test pre-commit hook
git add .
git commit -m "Test commit"  # Hooks will run automatically
```

**That's it!** You're now protected from pushing broken code.

---

## 📊 Testing Overview

### Test Statistics
- **Total Tests**: 93 (all passing)
- **Coverage**: 52% (664/1289 statements)
- **Execution Time**: ~2 seconds
- **Test Files**: 12 files organized by module

### Coverage Breakdown

| Module | Coverage | Tests | Status |
|--------|----------|-------|--------|
| CSV Converter | 95% | 10 | ✅ Excellent |
| SEO Enhancer | 87% | 11 | ✅ Excellent |
| Frontmatter Generator | 82% | 19 | ✅ Excellent |
| TXT Converter | 78% | 8 | ✅ Good |
| WXR Converter | 73% | 6 | ✅ Good |
| DOCX Converter | 56% | 4 | ⚠️ Moderate |
| File Utils | 48% | 11 | ⚠️ Moderate |
| Image Handler | 25% | 7 | ❌ Needs Work |

### Test Organization

```
tests/
├── conftest.py                      # 15 shared fixtures
├── converters/                      # 28 converter tests
│   ├── test_csv_converter.py
│   ├── test_docx_converter.py
│   ├── test_txt_converter.py
│   └── test_wxr_converter.py
├── utils/                           # 53 utility tests
│   ├── test_file_utils.py
│   ├── test_frontmatter_generator.py
│   ├── test_image_handler.py
│   └── test_seo_enhancer.py
└── integration/                     # 12 integration tests
    └── test_conversion_pipeline.py
```

---

## 🎣 Git Hooks System

### Two-Layer Protection

#### Layer 1: Pre-Commit Hooks (On `git commit`)
Runs **before** code is committed:

1. **Black** - Code formatting
2. **Ruff** - Linting and auto-fixes
3. **Bandit** - Security vulnerability scanning
4. **MyPy** - Type checking
5. **File checks** - Whitespace, large files, conflicts, etc.

**Result**: Clean, secure, well-formatted code in every commit.

#### Layer 2: Pre-Push Hooks (On `git push`)
Runs **before** code is pushed:

1. **Full test suite** - All 93 tests must pass
2. **Coverage check** - Minimum 50% coverage required
3. **Fail fast** - Stops on first test failure

**Result**: Only tested, working code reaches the remote repository.

### Workflow Example

```bash
# 1. Make changes
echo "new code" >> converters/csv_converter.py

# 2. Stage changes
git add .

# 3. Commit (pre-commit hooks run automatically)
git commit -m "Add feature"
# → Black formats code
# → Ruff checks linting
# → Bandit scans for security issues
# → MyPy checks types
# ✅ Commit succeeds if all pass

# 4. Push (pre-push hooks run automatically)
git push origin main
# → Pytest runs 93 tests
# → Coverage is calculated
# → Push proceeds only if tests pass
# ✅ Code is now safely in remote
```

### What It Looks Like

#### Successful Commit
```
$ git commit -m "Add CSV export feature"

black............................Passed
ruff.............................Passed
bandit...........................Passed
mypy.............................Passed
trailing-whitespace..............Passed
end-of-file-fixer................Passed

[main abc1234] Add CSV export feature
 2 files changed, 50 insertions(+)
```

#### Successful Push
```
$ git push origin main

🧪 Running pre-push checks...

Running test suite...

======================= test session starts =======================
tests/converters/test_csv_converter.py .......... PASSED
tests/utils/test_frontmatter_generator.py ................... PASSED
...
======================= 93 passed in 2.14s =======================

Coverage: 52%

✅ All tests passed! Proceeding with push.

Enumerating objects: 5, done.
To github.com:user/repo.git
   abc1234..def5678  main -> main
```

#### Failed Push
```
$ git push origin main

🧪 Running pre-push checks...

Running test suite...

FAILED tests/converters/test_csv_converter.py::test_convert_empty

❌ Tests failed! Push aborted.

Please fix the failing tests before pushing.
You can run tests locally with: pytest -v

To bypass this check (NOT RECOMMENDED): git push --no-verify
```

---

## 🛠️ Common Commands

### Testing Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=converters --cov=utils --cov-report=html

# Run specific test file
pytest tests/converters/test_csv_converter.py

# Run specific test
pytest tests/converters/test_csv_converter.py::TestCsvConverter::test_convert_basic_csv

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Show detailed output on failure
pytest -v --tb=long
```

### Hook Commands

```bash
# Run all pre-commit hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run pytest --hook-stage push

# Update hook versions
pre-commit autoupdate

# Reinstall hooks
pre-commit uninstall
pre-commit install --install-hooks
pre-commit install --hook-type pre-push

# Skip hooks (emergency only)
git commit --no-verify
git push --no-verify

# Skip specific hooks
SKIP=bandit git commit -m "message"
SKIP=bandit,mypy git commit -m "message"
```

### Coverage Commands

```bash
# Generate HTML coverage report
pytest --cov-report=html
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux

# Show missing lines
pytest --cov-report=term-missing

# Generate JSON report
pytest --cov-report=json

# Fail if coverage below threshold
pytest --cov-fail-under=50
```

---

## 📁 Configuration Files

### `.pre-commit-config.yaml`
Defines all pre-commit hooks:
- Code formatters (Black)
- Linters (Ruff)
- Security scanners (Bandit)
- Type checkers (MyPy)
- File validators
- Test runner (Pytest on push)

### `pytest.ini`
Pytest configuration:
```ini
[pytest]
testpaths = tests
addopts =
    --verbose
    --cov=converters
    --cov=utils
    --cov-fail-under=50
    --cov-report=term-missing
    --cov-report=html:htmlcov

markers =
    unit: Unit tests
    integration: Integration tests
    converter: Converter tests
    utils: Utility tests
    slow: Long-running tests
```

### `pyproject.toml`
Development dependencies:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "pillow>=10.0.0",
]
```

---

## 🎓 Best Practices

### 1. Test Before Committing
```bash
# Always run tests locally first
pytest -v

# Then commit
git add .
git commit -m "Your message"
```

### 2. Write Tests for New Code
```python
# tests/converters/test_new_converter.py
import pytest
from converters.new_converter import NewConverter

class TestNewConverter:
    @pytest.fixture
    def converter(self):
        return NewConverter()

    @pytest.mark.unit
    def test_convert_basic(self, converter, sample_file):
        result = converter.convert(sample_file)
        assert isinstance(result, str)
        assert len(result) > 0
```

### 3. Keep Tests Fast
- Use fixtures for setup
- Mock external dependencies
- Mark slow tests with `@pytest.mark.slow`

### 4. Don't Bypass Hooks
- Fix issues instead of using `--no-verify`
- Bypassing hooks defeats their purpose
- Only use in genuine emergencies

### 5. Update Coverage Goals
As coverage improves, increase the threshold:
```ini
# pytest.ini
--cov-fail-under=60  # Increase from 50% to 60%
```

---

## 🔧 Troubleshooting

### Tests Failing Locally

```bash
# See detailed failure info
pytest -v --tb=long

# Run only failed tests
pytest --lf

# Debug specific test
pytest tests/path/to/test.py::test_name -v -s
```

### Hooks Not Running

```bash
# Check if hooks are installed
ls -la .git/hooks/

# Reinstall
pre-commit uninstall
pre-commit install --install-hooks
pre-commit install --hook-type pre-push

# Check hook is executable (Unix/Mac)
chmod +x .git/hooks/pre-push
```

### Import Errors in Tests

```bash
# Make sure you're in project root
pwd

# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Coverage Not Updating

```bash
# Clear coverage cache
rm -rf .coverage htmlcov/

# Run fresh
pytest --cov=converters --cov=utils --cov-report=html
```

---

## 📚 Documentation Links

- **[tests/README.md](tests/README.md)** - Detailed testing guide
- **[docs/GIT_HOOKS_SETUP.md](docs/GIT_HOOKS_SETUP.md)** - Complete hook documentation
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Testing implementation summary
- **[README_HOOKS.md](README_HOOKS.md)** - Quick hook reference

---

## 🎯 Roadmap to 80% Coverage

### Phase 1: High Priority (50% → 65%)
1. Add HTML Generator tests
2. Add SEO Validator tests
3. Improve Image Handler tests
4. Improve File Utils tests

### Phase 2: Medium Priority (65% → 75%)
1. Add Static Site Generator tests
2. Add Template Manager tests
3. Improve DOCX Converter tests
4. Add more edge case tests

### Phase 3: Polish (75% → 80%+)
1. Property-based testing (Hypothesis)
2. Performance benchmarks
3. Mutation testing
4. Visual regression tests

---

## 🌟 Benefits

### For You
- ✅ Catch bugs before they reach production
- ✅ Refactor with confidence
- ✅ Faster code reviews
- ✅ Better sleep at night

### For The Team
- ✅ Consistent code quality
- ✅ Automated quality gates
- ✅ Clear testing standards
- ✅ Easier onboarding

### For The Project
- ✅ Fewer production bugs
- ✅ Higher code quality
- ✅ Better maintainability
- ✅ Professional standards

---

## ❓ FAQ

**Q: Can I skip the hooks?**
A: Yes with `--no-verify`, but don't make it a habit. The hooks are there to help you.

**Q: What if tests are too slow?**
A: Mark slow tests with `@pytest.mark.slow` and exclude them during development: `pytest -m "not slow"`

**Q: How do I update hook versions?**
A: Run `pre-commit autoupdate` then `pre-commit install --install-hooks`

**Q: Can I run hooks in CI/CD?**
A: Yes! Use `pre-commit run --all-files` in your CI pipeline.

**Q: What if I need to push urgent fix?**
A: Use `git push --no-verify` but create a follow-up PR to fix the tests.

---

## 🎉 Summary

You now have a professional testing and quality control system:

1. **93 automated tests** catching bugs before they happen
2. **Pre-commit hooks** ensuring code quality standards
3. **Pre-push hooks** preventing broken code from being pushed
4. **52% test coverage** with clear path to 80%+
5. **Comprehensive documentation** for the team

**The result**: Higher quality code, fewer bugs, faster development, and happier developers! 🚀

---

**Next Steps:**
1. ✅ Install hooks: `./scripts/install-hooks.sh`
2. ✅ Run tests: `pytest -v`
3. ✅ Make a commit: hooks run automatically
4. ✅ Push your code: tests run automatically
5. ✅ Start writing more tests!

Happy testing! 🧪
