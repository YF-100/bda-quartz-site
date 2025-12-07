# Quartz & Cloudflare Deployment Guide

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Last Updated:** December 6, 2025

## Overview

This guide helps you deploy your Big Data Analytics course materials (labs, assignments, and projects) as a professional static website using Quartz and Cloudflare Pages.

## Prerequisites

Before starting, ensure you have:

1. **macOS or Linux** with bash, git, curl, and jq
2. **Cloudflare account** with Pages enabled
3. **GitHub CLI** (`gh`) authenticated
4. **Cloudflare API Token** with appropriate permissions (see below)
5. **Custom domain** (optional) - if you have one in Cloudflare

## Quick Start

### Step 1: Configure the Script

Open `setup_quartz_cloudflare.sh` and update these variables at the top:

```bash
export GH_USER="YOUR_GITHUB_USERNAME"              # Your GitHub username/org
export REPO="bda-quartz-site"                      # Your Quartz repo name
export PROJ="bda-course-site"                      # Cloudflare project name
export DOMAIN="yourdomain.com"                     # Optional: your custom domain
export EMAIL_DOMAIN="esiee.fr,edu.esiee.fr"       # Allowed email domains for access
export ACCESS_APP_NAME="BDA Course Access"         # Cloudflare Access app name
export CLOUDFLARE_ACCOUNT_ID="YOUR_ACCOUNT_ID"     # Get from Cloudflare dashboard
export CLOUDFLARE_API_TOKEN="YOUR_API_TOKEN"       # Create from API Tokens page
```

**Important Notes:**
- If you don't have a custom domain, leave `DOMAIN="CHANGE_ME_DOMAIN"` and the script will use `<project>.pages.dev`
- The `EMAIL_DOMAIN` restricts site access to specific email domains (e.g., your university domain)

### Step 2: Create Cloudflare API Token

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) → Profile → API Tokens
2. Click **Create Token**
3. Use **Custom Token** with these permissions:
   - **Account → Cloudflare Pages**: Edit
   - **Zone → DNS**: Edit (if using custom domain)
   - **Account → Access: Apps and Policies**: Edit

4. Set **Account Resources** to your account
5. Save the token securely (you can't view it again)

### Step 3: Enable Cloudflare Access (Critical!)

**Before running the script**, enable Zero Trust Access:

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) → Zero Trust
2. If you see "Enable Access", click it
3. If you haven't created a Zero Trust account, click "Start for free"
4. Navigate to **Access** → **Overview** and ensure it's activated

⚠️ **Without this step**, the access restrictions won't work and your site will be public!

### Step 4: Bootstrap the Site

Run the automated setup:

```bash
# First-time setup (handles chmod and execution)
make site/setup
```

This will:
- Install Node.js 22 (via nvm)
- Install required tools (GitHub CLI, Wrangler, nbconvert)
- Clone Quartz template
- Convert notebooks to HTML
- Build the static site
- Create GitHub repository
- Deploy to Cloudflare Pages
- Configure access restrictions

**Expected Duration:** 5-10 minutes (first run)

### Step 5: Verify Deployment

After completion, you should see:

```
[HH:MM:SS] 14) Deployment complete
Site URL: https://your-project.pages.dev
Repository: https://github.com/YOUR_USER/bda-quartz-site
```

Visit the URL and verify:
1. You're prompted to authenticate with your ESIEE email
2. The site loads with your course materials
3. Labs and notebooks are accessible

## Subsequent Updates

After making changes to your course materials (labs, notebooks, documentation):

```bash
# Rebuild and redeploy
make site/update
```

This is much faster (1-2 minutes) as it skips initial setup steps.

## Optional: Code Quality Checks

Before committing changes:

```bash
# Run lint checks (black for Python, bash syntax)
make site/check
```

## Project Structure

After deployment, your structure will be:

```
~/course-website/
└── bda-quartz-site/          # Quartz site root
    ├── content/               # Markdown content
    │   ├── index.md          # Homepage (from README.md)
    │   ├── labs-final/       # Lab assignments
    │   ├── project-final/    # Final project
    │   └── roadmap/          # Course roadmap
    ├── quartz/
    │   └── static/
    │       ├── nb/           # Converted notebooks (HTML)
    │       └── img/          # Images
    ├── public/               # Built site (generated)
    └── quartz.config.ts      # Quartz configuration
```

## Key Features

### 1. Automatic Notebook Conversion
- All `.ipynb` files are converted to HTML using `nbconvert`
- Notebooks are accessible at `/static/nb/<path>`
- Index page lists all notebooks with descriptions

### 2. Access Control
- Restricts access to specified email domains
- Uses Cloudflare Access for authentication
- Configurable per-domain rules

### 3. Asset Management
- Automatically copies CSV, JSON, SQL, PDF, images
- Creates download sections in folder index pages
- Excludes raw data files (in `data/` directories)

### 4. Continuous Deployment
- Push to GitHub main branch triggers rebuild
- Cloudflare Pages automatically deploys updates
- GitHub Actions validate code quality

## Customization

### Change Allowed Email Domains

Edit `setup_quartz_cloudflare.sh`:

```bash
export EMAIL_DOMAIN="youruniversity.edu,alumni.youruniversity.edu"
```

### Add Custom Domain

1. Add domain to Cloudflare (must be active)
2. Update script:
   ```bash
   export DOMAIN="courses.youruniversity.edu"
   ```
3. Redeploy: `make site/update`
4. Update DNS records as prompted

### Modify Site Theme/Layout

Edit `~/course-website/bda-quartz-site/quartz.config.ts`:
- Change colors, fonts, layout
- Add/remove plugins
- Configure navigation

See [Quartz documentation](https://quartz.jzhao.xyz/) for details.

## Troubleshooting

### Error: "Set CLOUDFLARE_API_TOKEN before running"
- You didn't set the API token in the script
- Solution: Edit `setup_quartz_cloudflare.sh` and set `CLOUDFLARE_API_TOKEN`

### Error: "access.api.error.not_enabled"
- Cloudflare Access not enabled
- Solution: Enable Zero Trust Access in Cloudflare dashboard (see Step 3)

### Site is publicly accessible
- Access policy wasn't created
- Check: Cloudflare Dashboard → Zero Trust → Access → Applications
- Should see application for your domain
- Solution: Ensure Access is enabled, then rerun `make site/update`

### Notebooks not showing
- Check: `~/course-website/bda-quartz-site/quartz/static/nb/`
- Should contain `.html` files
- If empty, nbconvert failed
- Solution: Install Jupyter: `python3 -m pip install --user jupyter nbconvert`

### Custom domain not working
- Ensure domain is added to Cloudflare
- Check DNS settings: must point to Cloudflare nameservers
- Verify in Cloudflare Pages → Custom domains
- May take 24-48 hours for DNS propagation

### Build fails with Node.js error
- Quartz requires Node.js 18+
- Solution: Script installs Node 22 via nvm
- Manually: `nvm install 22 && nvm use 22`

## Maintenance

### Rotate API Token (Recommended Quarterly)
1. Create new token (same permissions)
2. Update `setup_quartz_cloudflare.sh`
3. Delete old token in Cloudflare
4. Update GitHub repository secrets if using CI/CD

### Clean Build (Nuclear Option)
If site is corrupted or you want fresh start:

```bash
# Remove generated site
make site/clean

# Start over
make site/setup
```

### Monitor Usage
- Cloudflare Pages: Free tier = 500 builds/month, 100 GB-hours
- Check: Cloudflare Dashboard → Pages → your project → Analytics

## Security Best Practices

1. **Never commit API tokens** to git
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Restrict token permissions**
   - Only grant necessary scopes
   - Use separate tokens for CI/CD vs local

3. **Review access logs**
   - Cloudflare Dashboard → Zero Trust → Logs
   - Monitor authentication attempts

4. **Update dependencies**
   - Run `npm update` in Quartz directory monthly
   - Update Python packages: `pip install --upgrade jupyter nbconvert`

## CI/CD Integration

The repository includes `.github/workflows/site-ci.yml` for automated deployment:

1. **On every push to main:**
   - Validates Python code with Black
   - Checks bash script syntax
   - Builds Quartz site
   - Deploys to Cloudflare Pages

2. **Required GitHub Secrets:**
   - `CLOUDFLARE_ACCOUNT_ID`
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_PROJECT`

3. **Set up:**
   - Go to GitHub repo → Settings → Secrets and variables → Actions
   - Add the three secrets above

## Resources

- **Quartz Documentation:** https://quartz.jzhao.xyz/
- **Cloudflare Pages:** https://developers.cloudflare.com/pages/
- **Cloudflare Access:** https://developers.cloudflare.com/cloudflare-one/policies/access/
- **Course Roadmap:** See `BDA/roadmap-labs-project-BDA.md`

## Support

For issues specific to this deployment:
1. Check this guide first
2. Review Cloudflare/Quartz documentation
3. Check GitHub Issues in your repository
4. Contact course instructor: Badr TAJINI

---

**Next Steps:**
1. Complete Step 1-5 above
2. Read [Course Roadmap](BDA/roadmap-labs-project-BDA.md) for lab sequence
3. Start with Lab 0 (Bootstrap)
4. Deploy updates after completing each lab

Good luck with your Big Data Analytics journey! 🚀
