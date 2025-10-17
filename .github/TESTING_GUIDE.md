# Testing Guide - Step by Step

This guide walks you through testing all GitHub Actions workflows from basic to production release.

## Prerequisites

✅ You've already set up secrets (see SECRETS_SETUP.md)
✅ Repository secrets: `CODECOV_TOKEN` (optional), `TEST_PYPI_API_TOKEN`
✅ Environment `production` created with: `PYPI_API_TOKEN`, `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`

## Testing Phases

We'll test in this order:
1. **Phase 1:** Basic test workflow (no releases)
2. **Phase 2:** TestPyPI release (safe testing)
3. **Phase 3:** Production release (real deal)

---

## Phase 1: Test Basic Workflow

This tests that your code passes all tests on GitHub's servers.

### Step 1: Commit and Push

```bash
# Make sure all changes are committed
git add .
git commit -m "Add GitHub Actions workflows"
git push origin main
```

### Step 2: Watch the Workflow

1. **Go to:** https://github.com/JohnThre/CTMU-for-macOS/actions
2. **You should see:** A workflow run named "Tests" with your commit message
3. **Click on it** to see details
4. **Wait for it to complete** (about 5-10 minutes for all Python versions)

### Step 3: Check Results

**Success indicators:**
- ✅ Green checkmark next to the workflow
- ✅ All jobs show green (test, lint)
- ✅ All Python versions (3.8-3.12) passed
- ✅ (If Codecov configured) Coverage report uploaded

**If it fails:**
- ❌ Red X - click to see which step failed
- Common issues:
  - Missing dependencies in requirements.txt
  - Import errors in tests
  - Failing test cases

**Fix and retry:**
```bash
# Fix the issue, then
git add .
git commit -m "Fix test issues"
git push origin main
# Workflow runs automatically again
```

---

## Phase 2: Test Release to TestPyPI

This publishes a test version to test.pypi.org to verify packaging works.

### Step 1: Create a Test Tag

```bash
# Use test- prefix for test releases
git tag test-v2.0.0-alpha.1
git push origin test-v2.0.0-alpha.1
```

### Step 2: Watch the Test Release Workflow

1. **Go to:** https://github.com/JohnThre/CTMU-for-macOS/actions
2. **Look for:** "Test Release" workflow
3. **Click on it** to watch progress

**What it does:**
- ✅ Runs all tests
- ✅ Builds Python packages (wheel + source)
- ✅ Uploads to test.pypi.org
- ✅ Tests installation from TestPyPI

### Step 3: Verify TestPyPI Upload

1. **Go to:** https://test.pypi.org/project/ctmu/
2. **You should see:** Version 2.0.0a1 (or similar)
3. **Check:** Files tab shows .whl and .tar.gz

### Step 4: Test Installation

**On your local machine:**

```bash
# Create a test virtualenv
python -m venv test_env
source test_env/bin/activate  # On macOS/Linux

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ctmu

# Test it works
ctmu --help
ctmu qr https://github.com --style bauhaus

# Clean up
deactivate
rm -rf test_env
```

**Success indicators:**
- ✅ Package installs without errors
- ✅ `ctmu --help` works
- ✅ Basic commands work

**If it fails:**
- Check package dependencies in setup.py
- Verify requirements.txt and setup.py match
- Check workflow logs for build errors

### Step 5: Delete Test Tag (Optional)

```bash
# Clean up test tags if you want
git tag -d test-v2.0.0-alpha.1
git push origin :refs/tags/test-v2.0.0-alpha.1
```

---

## Phase 3: Production Release

This creates the official release with PyPI publishing and signed macOS packages.

### Before You Start

**Checklist:**
- ✅ All tests passing in Phase 1
- ✅ TestPyPI release worked in Phase 2
- ✅ Version number in setup.py is correct and updated
- ✅ CHANGELOG.md updated (if you have one)
- ✅ All secrets configured correctly

### Step 1: Update Version Number

```bash
# Edit setup.py
# Change version="2.0.0" to your new version
# Example: version="2.1.0"

# Commit the version bump
git add setup.py
git commit -m "Bump version to 2.1.0"
git push origin main
```

### Step 2: Create Production Tag

```bash
# Use v prefix for production (NO "test-")
git tag v2.1.0
git push origin v2.1.0
```

### Step 3: Approve the Deployment (if protection enabled)

If you enabled environment protection rules:

1. **Go to:** https://github.com/JohnThre/CTMU-for-macOS/actions
2. **Click on:** The "Release" workflow run
3. **You'll see:** Yellow "Review deployments" button
4. **Click:** "Review deployments"
5. **Check:** ✅ production
6. **Click:** "Approve and deploy"

**The workflow will then:**
- ✅ Run all tests
- ✅ Build Python packages (wheel + source)
- ✅ Import GPG key
- ✅ Build macOS PKG installer
- ✅ Build macOS DMG disk image
- ✅ Sign PKG with GPG → creates .asc file
- ✅ Sign DMG with GPG → creates .asc file
- ✅ Create signed checksums file
- ✅ Create GitHub Release with all artifacts
- ✅ Publish to PyPI

### Step 4: Watch the Build

**Monitor progress:**
1. **Actions tab:** Watch each step complete
2. **Look for:** Green checkmarks on each job
3. **Build takes:** ~10-15 minutes total

**Jobs:**
- `build` - Creates all packages and GitHub release
- `publish-pypi` - Publishes to PyPI

### Step 5: Verify GitHub Release

1. **Go to:** https://github.com/JohnThre/CTMU-for-macOS/releases
2. **You should see:** Release v2.1.0

**Check artifacts:**
- ✅ `ctmu-2.1.0-py3-none-any.whl` - Python wheel
- ✅ `ctmu-2.1.0.tar.gz` - Source distribution
- ✅ `CTMU-0.1.pkg` - macOS installer
- ✅ `CTMU-0.1.dmg` - macOS disk image
- ✅ `CTMU-0.1.pkg.asc` - PKG GPG signature
- ✅ `CTMU-0.1.dmg.asc` - DMG GPG signature
- ✅ `checksums.txt` - SHA256 checksums
- ✅ `CTMU-0.1-checksums.txt.asc` - Signed checksums

### Step 6: Verify PyPI Publication

1. **Go to:** https://pypi.org/project/ctmu/
2. **You should see:** Version 2.1.0
3. **Check:** Files tab shows wheel and source

### Step 7: Test Installation from PyPI

```bash
# Fresh virtualenv
python -m venv prod_test
source prod_test/bin/activate

# Install from production PyPI
pip install ctmu

# Test
ctmu --help
ctmu --version  # Should show 2.1.0

# Clean up
deactivate
rm -rf prod_test
```

### Step 8: Test macOS Packages

**PKG Installer:**
1. Download `CTMU-0.1.pkg` from GitHub release
2. Download `CTMU-0.1.pkg.asc` signature
3. Verify signature:
   ```bash
   gpg --verify CTMU-0.1.pkg.asc CTMU-0.1.pkg
   ```
4. Double-click PKG to install
5. Test: open Terminal, run `ctmu --help`

**DMG Disk Image:**
1. Download `CTMU-0.1.dmg` from GitHub release
2. Download `CTMU-0.1.dmg.asc` signature
3. Verify signature:
   ```bash
   gpg --verify CTMU-0.1.dmg.asc CTMU-0.1.dmg
   ```
4. Double-click DMG to mount
5. Drag CTMU.app to Applications

---

## Troubleshooting

### Test Workflow Fails

**Check:**
- Tests passing locally? Run `pytest tests/ -v`
- Dependencies installed? Check requirements.txt
- Python version compatible? Test with Python 3.8+

**Common fixes:**
- Add missing dependencies to requirements.txt
- Fix failing tests
- Update setup.py with correct dependencies

### TestPyPI Upload Fails

**Check:**
- `TEST_PYPI_API_TOKEN` secret set correctly?
- Token expired? Generate new one
- Package name conflict? First upload might need manual reservation

**Fix:**
- Verify token at https://test.pypi.org/manage/account/#api-tokens
- Re-add secret with new token

### Production Release Fails

**GPG Signing Issues:**
```
Error: gpg: signing failed: No secret key
```

**Fix:**
- Verify `GPG_PRIVATE_KEY` includes full key (BEGIN/END lines)
- Check key ID matches: should be for jnc@freew.org
- Verify passphrase in `GPG_PASSPHRASE`

**PyPI Upload Issues:**
```
Error: 403 Invalid or non-existent authentication
```

**Fix:**
- Verify `PYPI_API_TOKEN` in production environment
- Check token scope includes project
- Ensure version number is higher than previous

### Environment Not Found

```
Error: environment 'production' not found
```

**Fix:**
1. Go to: https://github.com/JohnThre/CTMU-for-macOS/settings/environments
2. Create environment named exactly: `production`
3. Add secrets to that environment

---

## Summary

### Test Checklist

- [ ] Phase 1: Push code → Test workflow passes
- [ ] Phase 2: Tag `test-v*` → TestPyPI upload works → Installation works
- [ ] Phase 3: Tag `v*` → Production release succeeds
  - [ ] GitHub Release created with all files
  - [ ] PyPI shows new version
  - [ ] Installation from PyPI works
  - [ ] PKG signature verifies
  - [ ] DMG signature verifies

### Common Command Reference

```bash
# Phase 1: Test workflow
git push origin main

# Phase 2: Test release
git tag test-v2.0.0-alpha.1
git push origin test-v2.0.0-alpha.1

# Phase 3: Production release
# 1. Update version in setup.py
git add setup.py
git commit -m "Bump version to 2.1.0"
git push origin main

# 2. Create and push tag
git tag v2.1.0
git push origin v2.1.0

# 3. Approve deployment in Actions tab (if protected)
# 4. Wait for workflow to complete
# 5. Verify on GitHub Releases and PyPI
```

---

**Questions?** Check the main [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) or [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md).
