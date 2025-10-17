# GitHub Environments Setup

This project uses **GitHub Environments** for production secrets to add an extra layer of security.

## Environment Structure

### Repository Secrets (Testing)
- `CODECOV_TOKEN` - Code coverage reporting
- `TEST_PYPI_API_TOKEN` - TestPyPI releases

### Environment Secrets (Production)
**Environment name:** `production`
- `PYPI_API_TOKEN` - Production PyPI releases
- `GPG_PRIVATE_KEY` - GPG signing for PKG/DMG
- `GPG_PASSPHRASE` - GPG key passphrase

## Setting Up the Production Environment

### Step 1: Create the Environment

1. **Go to:** https://github.com/JohnThre/CTMU-for-macOS/settings/environments
2. **Click:** "New environment" button
3. **Name:** `production` (must be exactly this)
4. **Click:** "Configure environment"

### Step 2: (Optional) Add Protection Rules

You can add extra safety by requiring manual approval:

1. **Check:** "Required reviewers"
2. **Add yourself** as a reviewer
3. This means you'll get a notification and must manually approve each production release

**Deployment branches:**
- Select "Selected branches"
- Add rule: `refs/tags/v*.*.*`
- This ensures only version tags can trigger production releases

### Step 3: Add Environment Secrets

Still on the environment configuration page:

1. **Scroll to:** "Environment secrets" section
2. **Click:** "Add secret" button
3. **Add each secret:**

#### PYPI_API_TOKEN
```
Name: PYPI_API_TOKEN
Value: pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### GPG_PRIVATE_KEY
```
Name: GPG_PRIVATE_KEY
Value: [Paste entire GPG private key including BEGIN/END lines]
```

#### GPG_PASSPHRASE
```
Name: GPG_PASSPHRASE
Value: [Your GPG key passphrase]
```

4. **Click:** "Add secret" for each one

## Setting Up Repository Secrets

These are used for testing and don't need environment protection.

1. **Go to:** https://github.com/JohnThre/CTMU-for-macOS/settings/secrets/actions
2. **Click:** "New repository secret"
3. **Add:**

#### CODECOV_TOKEN (Optional)
```
Name: CODECOV_TOKEN
Value: [Your Codecov token]
```

#### TEST_PYPI_API_TOKEN
```
Name: TEST_PYPI_API_TOKEN
Value: pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Verification

### Check Environment Setup

1. Go to: https://github.com/JohnThre/CTMU-for-macOS/settings/environments/production
2. You should see:
   - ✅ Environment name: `production`
   - ✅ 3 secrets (PYPI_API_TOKEN, GPG_PRIVATE_KEY, GPG_PASSPHRASE)
   - ✅ (Optional) Protection rules configured

### Check Repository Secrets

1. Go to: https://github.com/JohnThre/CTMU-for-macOS/settings/secrets/actions
2. You should see:
   - ✅ CODECOV_TOKEN (if you added it)
   - ✅ TEST_PYPI_API_TOKEN

## How It Works

### Test Workflow (test.yml)
- **Uses:** Repository secrets only
- **Triggers:** Every push to main/develop
- **No approval needed**

### Test Release Workflow (test-release.yml)
- **Uses:** Repository secret `TEST_PYPI_API_TOKEN`
- **Triggers:** Tags like `test-v2.1.0-alpha.1`
- **No approval needed**

### Production Release Workflow (release.yml)
- **Uses:** Environment secrets from `production`
- **Triggers:** Tags like `v2.1.0`
- **With protection rules:** Requires manual approval ✋
- **Builds:** Python packages + macOS PKG/DMG
- **Signs:** All packages with GPG
- **Publishes:** To PyPI and GitHub Releases

## Security Benefits

### With Environment Protection:

1. **Manual Approval:** You approve each production release
2. **Audit Trail:** GitHub logs all approvals
3. **Branch Restrictions:** Only version tags can trigger
4. **Separate Secrets:** Production secrets isolated from testing

### Workflow:

```
Developer pushes tag v2.1.0
         ↓
GitHub Actions starts release workflow
         ↓
🛑 PAUSED - Waiting for approval
         ↓
You review and click "Approve and deploy"
         ↓
✅ Workflow continues:
   - Builds packages
   - Signs with GPG
   - Publishes to PyPI
   - Creates GitHub release
```

## Quick Reference

| What | Where | Protection |
|------|-------|------------|
| Code coverage | Repository secret | None |
| Test releases | Repository secret | None |
| Production releases | Environment secret | Optional approval |
| GPG signing | Environment secret | Optional approval |

---

**Next Steps:** See [TESTING_GUIDE.md](TESTING_GUIDE.md) for step-by-step testing instructions.
