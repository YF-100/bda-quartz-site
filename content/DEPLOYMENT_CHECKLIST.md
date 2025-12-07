# Quartz Deployment Configuration Checklist

**Use this checklist before running `make site/setup` for the first time.**

---

## ✅ Pre-Flight Checklist

### 1. Cloudflare Account Setup

- [ ] **Cloudflare account created** → [Sign up](https://dash.cloudflare.com/sign-up)
- [ ] **Zero Trust Access enabled**
  - Go to Dashboard → Zero Trust
  - Click "Enable Access" or "Start for free"
  - Verify in Access → Overview that it shows as active
- [ ] **Cloudflare Pages enabled**
  - Go to Dashboard → Workers & Pages
  - Confirm you can see "Create application" button

### 2. API Token Created

- [ ] **Token created with correct permissions:**
  - Go to Profile → API Tokens → Create Token
  - Use **Custom Token**
  - Permissions:
    - ✅ Account → Cloudflare Pages: **Edit**
    - ✅ Zone → DNS: **Edit** (if using custom domain)
    - ✅ Account → Access: Apps and Policies: **Edit**
  - Account Resources: Include → Specific account → [Your Account]
  - Token created successfully

- [ ] **Token copied and stored securely**
  - ⚠️ You can only view it once!
  - Save in password manager or secure note

### 3. Account ID Retrieved

- [ ] **Cloudflare Account ID obtained:**
  - Go to Dashboard → Workers & Pages
  - Look at right sidebar under "Account ID"
  - Format: 32-character hex string (e.g., `a1b2c3d4e5f6...`)
  - Copy the full ID

### 4. GitHub CLI Authenticated

- [ ] **GitHub CLI installed:**
  ```bash
  # macOS
  brew install gh
  
  # Or check if already installed
  gh --version
  ```

- [ ] **GitHub CLI authenticated:**
  ```bash
  gh auth login
  # Follow prompts to authenticate
  
  # Verify
  gh auth status
  ```

### 5. Custom Domain (Optional)

If you want to use a custom domain:

- [ ] **Domain added to Cloudflare:**
  - Go to Dashboard → Websites → Add a Site
  - Enter your domain name
  - Follow nameserver setup instructions
  - Wait for status to show "Active" (may take 24-48 hours)

- [ ] **Domain active and using Cloudflare nameservers:**
  ```bash
  # Check current nameservers
  dig NS yourdomain.com +short
  
  # Should show Cloudflare nameservers (e.g., ns1.cloudflaressl.com)
  ```

If you don't have a custom domain:
- [ ] **Will use default `.pages.dev` URL** (no action needed)

### 6. Email Domain for Access Control

- [ ] **Decided which email domains to allow:**
  - University domain: `esiee.fr`
  - Student email domain: `edu.esiee.fr`
  - Alumni domain: `alumni.esiee.fr`
  - Other: `_________________`

- [ ] **Email domains format checked:**
  - Comma-separated, no spaces
  - Example: `esiee.fr,edu.esiee.fr`
  - Will use: `_________________`

---

## 📝 Configuration Variables Worksheet

Fill this out, then transfer to `setup_quartz_cloudflare.sh`:

```bash
# Your values (fill in):
GH_USER="___________________"              # Your GitHub username
REPO="bda-quartz-site"                     # Keep or customize
PROJ="___________________"                 # Cloudflare project name (lowercase, no spaces)
DOMAIN="___________________"               # Your domain OR "CHANGE_ME_DOMAIN"
EMAIL_DOMAIN="___________________"         # e.g., "esiee.fr,edu.esiee.fr"
ACCESS_APP_NAME="___________________"      # e.g., "BDA Course Access"
CLOUDFLARE_ACCOUNT_ID="___________________" # 32-char hex from dashboard
CLOUDFLARE_API_TOKEN="___________________"  # From API Tokens page
```

### Variable Guidelines

| Variable | Example | Notes |
|----------|---------|-------|
| `GH_USER` | `YF-100` | Your GitHub username (case-sensitive) |
| `REPO` | `bda-quartz-site` | Repository name (will be created if doesn't exist) |
| `PROJ` | `bda-course-site` | Cloudflare project (lowercase, alphanumeric + hyphens) |
| `DOMAIN` | `courses.example.com` or `CHANGE_ME_DOMAIN` | Must be active in Cloudflare first |
| `EMAIL_DOMAIN` | `esiee.fr,edu.esiee.fr` | Comma-separated, no @ symbol |
| `ACCESS_APP_NAME` | `BDA Course Access` | Display name for Cloudflare Access app |
| `CLOUDFLARE_ACCOUNT_ID` | `a1b2c3d4...` | 32-character hex string |
| `CLOUDFLARE_API_TOKEN` | `abc123xyz...` | Long alphanumeric string |

---

## 🔧 Edit Configuration File

- [ ] **Opened `setup_quartz_cloudflare.sh` in editor:**
  ```bash
  nano setup_quartz_cloudflare.sh
  # Or use VS Code:
  code setup_quartz_cloudflare.sh
  ```

- [ ] **Updated all CHANGE_ME_ placeholders:**
  - Search for `CHANGE_ME_` in the file
  - Replace with your actual values from worksheet above
  - Ensure no spaces around `=` signs

- [ ] **Saved the file:**
  - In nano: `Ctrl+O`, `Enter`, `Ctrl+X`
  - In VS Code: `Cmd+S` (macOS) or `Ctrl+S` (Linux)

- [ ] **Verified no placeholders remain:**
  ```bash
  grep -i "CHANGE_ME" setup_quartz_cloudflare.sh
  # Should return no results (or only commented examples)
  ```

---

## 🖥️ Local System Requirements

- [ ] **Operating System:**
  - [ ] macOS 10.15+ or
  - [ ] Linux (Ubuntu 20.04+, Debian, Fedora, etc.)
  - ⚠️ Windows users: Use WSL2

- [ ] **Required tools installed:**
  ```bash
  # Check all at once:
  for tool in bash git curl jq; do
    if command -v $tool >/dev/null; then
      echo "✓ $tool"
    else
      echo "✗ $tool - NOT INSTALLED"
    fi
  done
  ```
  - [ ] bash
  - [ ] git
  - [ ] curl
  - [ ] jq

- [ ] **If any missing, install:**
  ```bash
  # macOS
  brew install git curl jq
  
  # Ubuntu/Debian
  sudo apt-get update && sudo apt-get install -y git curl jq
  
  # Fedora
  sudo dnf install -y git curl jq
  ```

- [ ] **Python 3 installed:**
  ```bash
  python3 --version
  # Should show 3.8 or higher
  ```

- [ ] **Node.js 22+ (will be installed by script if missing):**
  - Script uses nvm to install Node.js 22
  - No manual action needed

---

## 📁 Repository Structure Check

- [ ] **Currently in repository root:**
  ```bash
  pwd
  # Should show: /Users/your-username/.../BIG_DATA_TD
  ```

- [ ] **Files exist:**
  ```bash
  ls -la setup_quartz_cloudflare.sh Makefile
  # Both should be listed
  ```

- [ ] **Script is not yet executable (will be fixed by make):**
  ```bash
  ls -l setup_quartz_cloudflare.sh
  # Shows: -rw-r--r-- (no 'x')
  # This is fine - make site/setup will add execute permission
  ```

---

## 🔐 Security Verification

- [ ] **API token is private:**
  - [ ] Not committed to git
  - [ ] Not shared publicly
  - [ ] Stored securely (password manager)

- [ ] **Script is not in git (if contains secrets):**
  ```bash
  # If you accidentally committed secrets:
  git rm --cached setup_quartz_cloudflare.sh
  echo "setup_quartz_cloudflare.sh" >> .gitignore
  git commit -m "Remove script with secrets from git"
  
  # Then edit file again with your tokens
  ```

- [ ] **.gitignore includes sensitive files:**
  ```bash
  # Check your .gitignore contains:
  grep -E "(\.env|.*token.*|.*secret.*)" .gitignore
  ```

---

## 🧪 Pre-Flight Test (Optional)

Before full deployment, verify basic setup:

- [ ] **GitHub authentication works:**
  ```bash
  gh repo list --limit 1
  # Should list one of your repos
  ```

- [ ] **Cloudflare API works:**
  ```bash
  # Replace with your actual values:
  curl -X GET "https://api.cloudflare.com/client/v4/user" \
    -H "Authorization: Bearer YOUR_API_TOKEN" \
    -H "Content-Type: application/json"
  
  # Should return JSON with your user info, no errors
  ```

- [ ] **Access API is enabled:**
  ```bash
  # Replace with your values:
  curl -X GET \
    "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/access/apps" \
    -H "Authorization: Bearer YOUR_API_TOKEN" \
    -H "Content-Type: application/json"
  
  # Should NOT return: "access.api.error.not_enabled"
  # If it does, enable Access in dashboard first
  ```

---

## ✨ Ready to Deploy!

If all checkboxes are marked:

```bash
# Run first-time setup:
make site/setup

# Expected duration: 5-10 minutes
# Watch for any error messages
```

### What to Watch For

During deployment, monitor for:
- ✅ "Checking base tools" → Should pass
- ✅ "Ensuring Node.js 22 via nvm" → Downloads Node if needed
- ✅ "Authenticating with GitHub and Cloudflare" → Uses stored credentials
- ✅ "Creating or refreshing the Quartz scaffold" → Clones template
- ✅ "Building the site" → Compiles static files
- ✅ "Deploying to Cloudflare Pages" → Uploads to CDN
- ✅ "Configuring Cloudflare Access" → Sets up authentication

### Success Indicators

At the end, you should see:
```
[HH:MM:SS] 14) Deployment complete
Site URL: https://your-project.pages.dev
Repository: https://github.com/YOUR_USER/bda-quartz-site
```

### If Errors Occur

1. **Read the error message carefully**
2. **Check relevant section in this checklist**
3. **Fix the issue**
4. **Re-run:** `make site/setup`

Common issues:
- "Set CLOUDFLARE_API_TOKEN" → Token not set in script
- "access.api.error.not_enabled" → Enable Access in dashboard
- "gh: command not found" → Install GitHub CLI
- "Permission denied" → Run from repo root, not as root user

---

## 📊 Post-Deployment Verification

After successful deployment:

- [ ] **Site is accessible:**
  ```bash
  # Visit URL shown in output
  # Or: https://PROJ.pages.dev
  ```

- [ ] **Access control works:**
  - [ ] Prompted to log in
  - [ ] Can log in with allowed email domain
  - [ ] Cannot log in with other domains

- [ ] **Content is visible:**
  - [ ] Homepage loads (from README.md)
  - [ ] Labs are listed
  - [ ] Notebooks are accessible at `/static/nb/...`

- [ ] **GitHub repository created:**
  ```bash
  # Visit: https://github.com/YOUR_USER/REPO_NAME
  # Should show Quartz site content
  ```

- [ ] **Cloudflare project exists:**
  - Go to Dashboard → Workers & Pages
  - Should see your project listed
  - Status: "Active"

---

## 🔄 Next Steps

After successful deployment:

1. **Bookmark your site URL**
2. **Test making changes:**
   ```bash
   # Edit any .md file in the repo
   # Then update:
   make site/update
   # Wait 1-2 minutes, refresh site
   ```

3. **Read the roadmap:**
   - See `BDA_ROADMAP.md` for course structure

4. **Start Lab 0:**
   - Navigate to `bigdata/lab0/`
   - Open `BDA_Lab0_Starter_v2.ipynb`

5. **Set up CI/CD (optional):**
   - Add GitHub secrets for automatic deployment
   - See `QUARTZ_DEPLOYMENT_GUIDE.md` → CI/CD Integration

---

## 📋 Maintenance Reminders

Set calendar reminders:

- [ ] **Quarterly:** Rotate API token
- [ ] **Monthly:** Update dependencies (`npm update` in site dir)
- [ ] **Weekly:** Review access logs (Cloudflare → Zero Trust → Logs)
- [ ] **After each lab:** Update site with `make site/update`

---

## 🆘 Need Help?

If stuck:

1. **Review full guide:** [QUARTZ_DEPLOYMENT_GUIDE.md](QUARTZ_DEPLOYMENT_GUIDE.md)
2. **Check Cloudflare status:** [status.cloudflare.com](https://status.cloudflare.com)
3. **Verify API token hasn't expired:** Cloudflare → Profile → API Tokens
4. **Check GitHub CLI auth:** `gh auth status`
5. **Review script output:** Look for specific error messages
6. **Start fresh:** `make site/clean && make site/setup`

---

**Good luck! 🚀**

*Save this checklist for future reference or when helping teammates set up their environments.*
