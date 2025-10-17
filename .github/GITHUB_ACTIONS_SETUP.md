# GitHub Actions Setup Guide

This document explains how to configure GitHub Actions for automated testing and releases in the CTMU project.

## Overview

Three workflows have been configured:
1. **test.yml** - Automated testing on push/PR
2. **release.yml** - Production releases to PyPI and GitHub
3. **test-release.yml** - Test releases to TestPyPI

## Quick Start

### 1. Enable GitHub Actions

1. Go to https://github.com/JohnThre/CTMU-for-macOS
2. Click on the **Actions** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**

### 2. Push Your Code

```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin main
```

The test workflow will run automatically! No secrets needed for basic testing.

## Setting Up GitHub Secrets

**Where to find this:** Go to your repository → Settings → Secrets and variables → Actions

**Direct link:** https://github.com/JohnThre/CTMU-for-macOS/settings/secrets/actions

### Step-by-Step Instructions:

1. **Navigate to secrets page:**
   - Go to https://github.com/JohnThre/CTMU-for-macOS
   - Click **"Settings"** (top menu bar)
   - In left sidebar, click **"Secrets and variables"** → **"Actions"**

2. **Add a new secret:**
   - Click green **"New repository secret"** button
   - Enter **Name** (e.g., `CODECOV_TOKEN`)
   - Enter **Value** (paste your token)
   - Click **"Add secret"**

3. **Repeat for each secret** you want to configure (see sections below)

## Test Workflow

The test workflow runs automatically on:
- Pushes to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Features:**
- Tests on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Runs on macOS runners (for macOS-specific features)
- Code coverage with pytest-cov
- Linting with flake8, black, and isort (soft failures)
- Optional Codecov integration

**No additional setup required** - the workflow runs out of the box.

### Optional: Codecov Integration

For code coverage reporting and badges:

**Secret Name:** `CODECOV_TOKEN`

**How to get it:**
1. Sign up at [codecov.io](https://codecov.io) with your GitHub account
2. Add your repository to Codecov (click "Add a repository")
3. Copy the upload token shown on the repository settings page
4. Add it to GitHub secrets as `CODECOV_TOKEN`

**Optional** - Codecov works without a token but using one is more secure.

## Test Release Workflow (TestPyPI)

This workflow lets you test releases before publishing to production PyPI.

**When to use:**
- Testing new versions before official release
- Verifying package builds correctly
- Checking installation works as expected

### Setting Up TestPyPI

**Secret Name:** `TEST_PYPI_API_TOKEN`

**How to get it:**
1. Create an account at [test.pypi.org](https://test.pypi.org/account/register/)
2. Verify your email address
3. Go to Account Settings → API tokens: https://test.pypi.org/manage/account/#api-tokens
4. Click **"Add API token"**
   - Token name: `CTMU GitHub Actions`
   - Scope: **"Entire account"** (or create project first and select it)
5. Copy the token (starts with `pypi-`) - **you can only see it once!**
6. Add to GitHub secrets:
   - **Name:** `TEST_PYPI_API_TOKEN`
   - **Value:** (paste the token)

**Creating a test release:**
```bash
# Tag with test- prefix
git tag test-v2.1.0-alpha.1
git push origin test-v2.1.0-alpha.1

# Or use manual trigger in Actions tab
```

**Testing installation:**
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ctmu
```

## Production Release Workflow

The release workflow creates GitHub releases and publishes to production PyPI.

### Required Secrets for Production

#### 1. PyPI Publishing (Recommended)

**Secret Name:** `PYPI_API_TOKEN`

**How to get it:**
1. Create an account at [pypi.org](https://pypi.org/account/register/)
2. Verify your email address
3. Go to Account Settings → API tokens: https://pypi.org/manage/account/#api-tokens
4. Click **"Add API token"**
   - Token name: `CTMU GitHub Actions`
   - Scope: **"Entire account"** (or create project first and select it)
5. Copy the token (starts with `pypi-`) - **you can only see it once!**
6. Add to GitHub secrets:
   - **Name:** `PYPI_API_TOKEN`
   - **Value:** (paste the token)

**Important:** This is different from TestPyPI! Use production PyPI for real releases.

#### 2. GPG Signing (Optional)

For signing macOS release packages (PKG/DMG):

**Secret Names:** `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE`

**How to set up:**

1. **Export your GPG private key:**
   ```bash
   gpg --armor --export-secret-key jnc@freew.org > private-key.asc
   ```

2. **Add GPG_PRIVATE_KEY to GitHub:**
   - Open `private-key.asc` in a text editor
   - Copy the **entire contents** (including `-----BEGIN PGP PRIVATE KEY BLOCK-----` and `-----END PGP PRIVATE KEY BLOCK-----`)
   - Add to GitHub secrets:
     - **Name:** `GPG_PRIVATE_KEY`
     - **Value:** (paste entire key)

3. **Add GPG_PASSPHRASE (if your key has one):**
   - **Name:** `GPG_PASSPHRASE`
   - **Value:** Your GPG key passphrase

4. **Securely delete the exported file:**
   ```bash
   rm -P private-key.asc  # macOS
   # or
   shred -u private-key.asc  # Linux
   ```

**Security Note:** Never commit GPG keys to git! The workflows will only sign if these secrets are present.

## Creating a Release

### Method 1: Git Tag (Recommended)

```bash
# Update version in setup.py first
git add setup.py
git commit -m "Bump version to 2.1.0"

# Create and push tag
git tag v2.1.0
git push origin v2.1.0
```

The workflow will:
1. Run all tests
2. Build Python packages (wheel and sdist)
3. Build macOS packages (PKG and DMG) if GPG is configured
4. Create a GitHub release with all artifacts
5. Publish to PyPI if token is configured

### Method 2: Manual Trigger

1. Go to Actions > Release
2. Click "Run workflow"
3. Enter the version tag (e.g., `v2.1.0`)
4. Click "Run workflow"

## Workflow Outputs

### Test Workflow Artifacts
- Test results in the workflow logs
- Code coverage report (if Codecov is configured)

### Release Workflow Artifacts

Every release includes:
- **Python Packages:**
  - `ctmu-X.X.X-py3-none-any.whl` (wheel)
  - `ctmu-X.X.X.tar.gz` (source distribution)
- **Checksums:**
  - `checksums.txt` (SHA256 hashes)

If GPG signing is configured, also includes:
- **macOS Packages:**
  - `CTMU-X.X.X.pkg` (macOS installer)
  - `CTMU-X.X.X.dmg` (disk image)
- **GPG Signatures:**
  - `*.asc` files for all packages
  - `CTMU-X.X.X-checksums.txt.asc` (signed checksums)

## Troubleshooting

### Tests Failing

Check the Actions tab for detailed error messages. Common issues:
- Missing dependencies (add to requirements.txt)
- macOS-specific features not working on runners
- Import errors (check package structure)

### Release Not Publishing to PyPI

Verify:
- `PYPI_API_TOKEN` secret is set correctly
- Token has not expired
- Package name is not already taken on PyPI
- Version number is higher than previous releases

### GPG Signing Failing

Verify:
- `GPG_PRIVATE_KEY` is the full armored export
- Key is not expired
- Passphrase (if any) is correct in `GPG_PASSPHRASE`

### Workflow Not Triggering

Check:
- Workflows are enabled in the Actions tab
- Tag follows the pattern `vX.X.X`
- You have push access to the repository

## Customization

### Changing Python Versions

Edit `.github/workflows/test.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
```

### Changing Branch Triggers

Edit the `on:` section in either workflow:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]
```

### Modifying Release Notes

Edit the release body template in `.github/workflows/release.yml`:

```yaml
body: |
  ## CTMU v${{ steps.get_version.outputs.version }}

  [Your custom release notes here]
```

## Best Practices

1. **Version Numbering:** Use semantic versioning (vMAJOR.MINOR.PATCH)
2. **Testing:** Always ensure tests pass before creating a release
3. **Changelog:** Keep a CHANGELOG.md and reference it in releases
4. **Security:** Rotate secrets periodically
5. **Dependencies:** Keep requirements.txt and setup.py in sync

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [GPG Signing Guide](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [Codecov Documentation](https://docs.codecov.com/)
