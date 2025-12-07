# Quartz Deployment - Quick Reference

## Prerequisites Checklist

- [ ] Cloudflare account created
- [ ] Custom domain added to Cloudflare (optional)
- [ ] Cloudflare API token created with correct permissions
- [ ] Cloudflare Zero Trust Access enabled
- [ ] GitHub CLI (`gh`) installed and authenticated
- [ ] Variables updated in `setup_quartz_cloudflare.sh`

## Essential Commands

```bash
# First-time setup (run once)
make site/setup

# Update site after changes (run often)
make site/update

# Check code quality before commit
make site/check

# Nuclear option: delete and start over
make site/clean
```

## Configuration Variables (edit setup_quartz_cloudflare.sh)

```bash
GH_USER="YOUR_GITHUB_USERNAME"          # Required
REPO="bda-quartz-site"                  # Your choice
PROJ="bda-course-site"                  # Your choice
DOMAIN="yourdomain.com"                 # Optional (or leave as CHANGE_ME_DOMAIN)
EMAIL_DOMAIN="esiee.fr,edu.esiee.fr"    # Required for access control
CLOUDFLARE_ACCOUNT_ID="abc123..."       # From Cloudflare dashboard
CLOUDFLARE_API_TOKEN="secret_token..."  # From API Tokens page
```

## Where to Find Configuration Values

| Variable | Location | Example |
|----------|----------|---------|
| `GH_USER` | Your GitHub username | `YF-100` |
| `CLOUDFLARE_ACCOUNT_ID` | Dashboard → Workers & Pages → Account ID (right sidebar) | `a1b2c3d4e5f6...` |
| `CLOUDFLARE_API_TOKEN` | Dashboard → Profile → API Tokens → Create Token | `abc123xyz...` |

## API Token Permissions Needed

When creating your Cloudflare API token, grant:

✅ **Account → Cloudflare Pages**: Edit  
✅ **Zone → DNS**: Edit (if using custom domain)  
✅ **Account → Access: Apps and Policies**: Edit  

## Typical Workflow

1. **First Time:**
   ```bash
   # Edit setup_quartz_cloudflare.sh (update variables)
   make site/setup
   # Wait 5-10 minutes
   # Visit your site URL
   ```

2. **After Making Changes:**
   ```bash
   # Edit notebooks, markdown, code
   make site/update
   # Wait 1-2 minutes
   # Refresh your site
   ```

3. **Before Committing:**
   ```bash
   make site/check
   git add .
   git commit -m "Update course materials"
   git push
   ```

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| "Set CLOUDFLARE_API_TOKEN" | Edit `setup_quartz_cloudflare.sh` and add token |
| "access.api.error.not_enabled" | Enable Zero Trust in Cloudflare dashboard |
| Site is public | Enable Cloudflare Access first, then rerun |
| Notebooks missing | Install: `pip install jupyter nbconvert` |
| Wrong Node version | Run: `nvm install 22 && nvm use 22` |
| Build corrupted | Run: `make site/clean && make site/setup` |

## File Locations

```
Repository root:
  setup_quartz_cloudflare.sh    ← Edit this with your config
  Makefile                      ← Commands defined here
  QUARTZ_DEPLOYMENT_GUIDE.md    ← Full documentation
  
Generated site:
  ~/course-website/bda-quartz-site/
    content/                    ← Markdown content
    quartz/static/nb/          ← Converted notebooks
    public/                    ← Built site (deployed)
```

## What Gets Deployed

✅ All `.md` files (with frontmatter added)  
✅ All `.ipynb` notebooks (converted to HTML)  
✅ Assets: CSV, JSON, SQL, PDF, images, scripts  
✅ Lab outputs and proof directories  
❌ Raw data files (in `data/` directories)  
❌ Python cache, node_modules, .git  

## Access Control

By default, only emails ending in:
- `@esiee.fr`
- `@edu.esiee.fr`

Can access the site after Cloudflare authentication.

To change, edit `EMAIL_DOMAIN` in the script.

## Site URLs

- **Default:** `https://<PROJ>.pages.dev`
- **Custom:** `https://<DOMAIN>` (if configured)
- **Notebooks:** `https://<URL>/static/nb/<path>`
- **Assets:** `https://<URL>/static/<path>`

## Next Steps

1. ✅ Read `QUARTZ_DEPLOYMENT_GUIDE.md` for detailed instructions
2. ✅ Update variables in `setup_quartz_cloudflare.sh`
3. ✅ Enable Cloudflare Access
4. ✅ Run `make site/setup`
5. ✅ Read course roadmap: `BDA/roadmap-labs-project-BDA.md`
6. ✅ Start Lab 0

---

**Need Help?** See full guide: `QUARTZ_DEPLOYMENT_GUIDE.md`  
**Course Materials:** See roadmap: `BDA/roadmap-labs-project-BDA.md`
