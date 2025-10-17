# GitHub Actions Documentation

This directory contains all documentation for GitHub Actions workflows and release automation.

## Quick Links

### 🚀 Getting Started
1. **[ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)** - Create the `production` environment and add secrets
2. **[SECRETS_SETUP.md](SECRETS_SETUP.md)** - Quick reference for all secrets
3. **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Step-by-step testing instructions

### 📚 Reference
- **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)** - Detailed workflow documentation
- **[workflows/](workflows/)** - Actual workflow files

## Environment Configuration Summary

### Repository Secrets (Testing)
```
https://github.com/JohnThre/CTMU-for-macOS/settings/secrets/actions

✅ CODECOV_TOKEN (optional)
✅ TEST_PYPI_API_TOKEN
```

### Environment Secrets (Production)
```
https://github.com/JohnThre/CTMU-for-macOS/settings/environments/production

Environment: production
✅ PYPI_API_TOKEN
✅ GPG_PRIVATE_KEY
✅ GPG_PASSPHRASE
```

## Testing Workflow

Follow these phases in order:

### Phase 1: Basic Tests
```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin main
```
→ Watch: https://github.com/JohnThre/CTMU-for-macOS/actions

### Phase 2: TestPyPI Release
```bash
git tag test-v2.0.0-alpha.1
git push origin test-v2.0.0-alpha.1
```
→ Verify: https://test.pypi.org/project/ctmu/

### Phase 3: Production Release
```bash
# Update version in setup.py first!
git add setup.py
git commit -m "Bump version to 2.1.0"
git push origin main

git tag v2.1.0
git push origin v2.1.0
```
→ Approve deployment in Actions tab
→ Verify: https://pypi.org/project/ctmu/
→ Check: https://github.com/JohnThre/CTMU-for-macOS/releases

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **test.yml** | Push to main/develop | Run tests on Python 3.8-3.12 |
| **test-release.yml** | Tag `test-v*.*.*` | Publish to TestPyPI |
| **release.yml** | Tag `v*.*.*` | Production release (PyPI + GitHub) |

## Files in This Directory

```
.github/
├── README.md                    # This file
├── ENVIRONMENT_SETUP.md         # How to create production environment
├── SECRETS_SETUP.md             # Quick secrets reference
├── TESTING_GUIDE.md             # Step-by-step testing
├── GITHUB_ACTIONS_SETUP.md      # Detailed workflow docs
├── FUNDING.yml                  # GitHub sponsors config
└── workflows/
    ├── test.yml                 # Test workflow
    ├── test-release.yml         # TestPyPI workflow
    └── release.yml              # Production release workflow
```

## Need Help?

1. **First time?** Start with [TESTING_GUIDE.md](TESTING_GUIDE.md)
2. **Setting up secrets?** See [SECRETS_SETUP.md](SECRETS_SETUP.md)
3. **Environment issues?** Check [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
4. **Detailed info?** Read [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)
