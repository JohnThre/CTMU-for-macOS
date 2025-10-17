# GitHub Secrets Setup - Quick Reference

This is a quick visual guide for setting up GitHub secrets for the CTMU project.

## Where to Set Up Secrets

### Direct Link
🔗 **https://github.com/JohnThre/CTMU-for-macOS/settings/secrets/actions**

### Manual Navigation
1. Go to: https://github.com/JohnThre/CTMU-for-macOS
2. Click: **"Settings"** (top navigation bar - you need admin access)
3. Left sidebar → **"Secrets and variables"** → **"Actions"**

## All Secrets at a Glance

| Secret Name | Required? | Used For | Get It From |
|-------------|-----------|----------|-------------|
| `CODECOV_TOKEN` | Optional | Code coverage badges | [codecov.io](https://codecov.io) |
| `TEST_PYPI_API_TOKEN` | Optional | Test releases | [test.pypi.org](https://test.pypi.org/manage/account/#api-tokens) |
| `PYPI_API_TOKEN` | Optional | Production releases | [pypi.org](https://pypi.org/manage/account/#api-tokens) |
| `GPG_PRIVATE_KEY` | Optional | Signing macOS packages | Export from your GPG keychain |
| `GPG_PASSPHRASE` | Optional | GPG key password | Your GPG key passphrase |

## Step-by-Step for Each Secret

### 1. CODECOV_TOKEN

**Purpose:** Upload code coverage reports and display coverage badges

**Steps:**
```
1. Go to: https://codecov.io
2. Sign in with GitHub
3. Click: "Add a repository" → select "CTMU-for-macOS"
4. Go to repository settings
5. Copy the "upload token"
6. Add to GitHub:
   Name: CODECOV_TOKEN
   Value: [paste token]
```

**Result:** Coverage badge in README will work, detailed coverage reports on Codecov

---

### 2. TEST_PYPI_API_TOKEN

**Purpose:** Publish test releases to TestPyPI for testing before production

**Steps:**
```
1. Go to: https://test.pypi.org/account/register/
2. Create account and verify email
3. Go to: https://test.pypi.org/manage/account/#api-tokens
4. Click: "Add API token"
   - Token name: CTMU GitHub Actions
   - Scope: Entire account
5. Copy token (starts with "pypi-") - SAVE IT NOW, you can't see it again!
6. Add to GitHub:
   Name: TEST_PYPI_API_TOKEN
   Value: [paste token starting with pypi-]
```

**Test it:**
```bash
git tag test-v2.1.0-alpha.1
git push origin test-v2.1.0-alpha.1
```

**Result:** Package published to test.pypi.org, can test installation

---

### 3. PYPI_API_TOKEN

**Purpose:** Publish production releases to PyPI (pip install ctmu)

**Steps:**
```
1. Go to: https://pypi.org/account/register/
2. Create account and verify email
3. Go to: https://pypi.org/manage/account/#api-tokens
4. Click: "Add API token"
   - Token name: CTMU GitHub Actions
   - Scope: Entire account (or select CTMU project after first release)
5. Copy token (starts with "pypi-") - SAVE IT NOW, you can't see it again!
6. Add to GitHub:
   Name: PYPI_API_TOKEN
   Value: [paste token starting with pypi-]
```

**Create release:**
```bash
git tag v2.1.0
git push origin v2.1.0
```

**Result:** Package published to pypi.org, anyone can: `pip install ctmu`

---

### 4. GPG_PRIVATE_KEY + GPG_PASSPHRASE

**Purpose:** Sign macOS PKG and DMG files with your GPG signature

**Steps:**
```
1. Export your GPG key:
   gpg --armor --export-secret-key jnc@freew.org > /tmp/private-key.asc

2. Open the file:
   cat /tmp/private-key.asc

3. Copy ENTIRE contents (including BEGIN/END lines)

4. Add to GitHub:
   Name: GPG_PRIVATE_KEY
   Value: [paste entire key, all lines]

5. If your key has a passphrase:
   Name: GPG_PASSPHRASE
   Value: [your passphrase]

6. Delete the exported file:
   rm -P /tmp/private-key.asc
```

**Security Warning:**
- Never commit this key to git
- Never share it publicly
- The file export is temporary only
- Delete it after copying to GitHub

**Result:** PKG and DMG files will have .asc signature files for verification

---

## How to Add a Secret to GitHub

### Visual Steps:

```
1. Navigate to secrets page (see "Where to Set Up Secrets" above)

2. Click: [New repository secret] (green button, top right)

3. Form appears with two fields:
   ┌─────────────────────────────────────┐
   │ Name *                              │
   │ [CODECOV_TOKEN________________]    │ ← Enter secret name (EXACT spelling)
   │                                     │
   │ Secret *                            │
   │ [************************_____]    │ ← Paste the token/key value
   │ [************************_____]    │
   │ [************************_____]    │
   │                                     │
   │ [Add secret]                        │ ← Click to save
   └─────────────────────────────────────┘

4. Secret is now saved and will appear in the list
   - You can update it but not view the value again
   - Workflows can access it via ${{ secrets.SECRET_NAME }}
```

---

## Testing Your Setup

### Minimal Setup (No Secrets)
Just push code - tests will run automatically:
```bash
git push origin main
```
✅ Tests run on Python 3.8-3.12

### With TEST_PYPI_API_TOKEN
Create a test release:
```bash
git tag test-v2.1.0-rc1
git push origin test-v2.1.0-rc1
```
✅ Package builds and uploads to test.pypi.org

### With PYPI_API_TOKEN
Create a production release:
```bash
git tag v2.1.0
git push origin v2.1.0
```
✅ Package builds and uploads to pypi.org
✅ GitHub release created with artifacts

### With All Secrets
```bash
git tag v2.1.0
git push origin v2.1.0
```
✅ Full release with:
- Python packages (wheel + source)
- macOS packages (PKG + DMG)
- GPG signatures (.asc files)
- Signed checksums
- PyPI publication
- Codecov reports

---

## Troubleshooting

### "Secret not found" Error
- Check spelling is EXACT (case-sensitive)
- Verify secret is added to the correct repository
- Make sure you're in "Actions" secrets, not "Dependabot" secrets

### PyPI Upload Fails
- Token might have expired (they don't expire by default, but check)
- Token might have wrong scope (needs "Entire account" or specific project)
- Package name might already exist (first release needs manual reservation)
- Version might already exist (can't reupload same version)

### GPG Signing Fails
- Key export must include `-----BEGIN PGP PRIVATE KEY BLOCK-----` header
- Key might be expired (check with: `gpg --list-secret-keys`)
- Passphrase might be wrong
- Make sure the key ID matches: `jnc@freew.org`

### Codecov Not Working
- Token is optional but recommended
- Check repository is added to Codecov account
- Verify tests are actually running (check Actions tab)
- Coverage data might take a few minutes to appear

---

## Security Best Practices

1. **Never commit secrets to git**
   - Check with: `git grep -i "pypi-"`
   - Secrets should ONLY be in GitHub settings

2. **Rotate tokens periodically**
   - Delete old tokens after creating new ones
   - Update GitHub secret with new value

3. **Use scoped tokens when possible**
   - After first PyPI release, create project-scoped token
   - Replace the "Entire account" token

4. **Monitor secret usage**
   - GitHub logs when secrets are accessed
   - Check Actions tab → Workflow runs → Logs

5. **Delete temporary files**
   - Always `rm -P` GPG exports
   - Clear terminal history if you pasted secrets: `history -c`

---

## Quick Command Reference

### Get Codecov Token
```bash
# Sign up at codecov.io, then find token at:
open "https://codecov.io/gh/JohnThre/CTMU-for-macOS/settings"
```

### Create PyPI Tokens
```bash
# Test PyPI
open "https://test.pypi.org/manage/account/#api-tokens"

# Production PyPI
open "https://pypi.org/manage/account/#api-tokens"
```

### Export GPG Key
```bash
gpg --armor --export-secret-key jnc@freew.org > /tmp/key.asc
cat /tmp/key.asc  # Copy this to GitHub
rm -P /tmp/key.asc  # Delete after copying
```

### Test Workflows
```bash
# Run tests
git push origin main

# Test release
git tag test-v2.1.0-beta.1
git push origin test-v2.1.0-beta.1

# Production release
git tag v2.1.0
git push origin v2.1.0
```

---

**Questions?** See the main [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed explanations.
