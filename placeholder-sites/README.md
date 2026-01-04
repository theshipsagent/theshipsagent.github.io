# Maritime Domains - Placeholder Sites

**Created:** January 3, 2026
**Purpose:** Brand placeholder sites for multi-domain strategy

---

## 📁 DIRECTORY STRUCTURE

```
placeholder-sites/
├── datumai-xyz/           → Deploy to datumai.xyz
│   ├── index.html
│   └── images/
├── oceandatum-ai/         → Deploy to oceandatum.ai
│   ├── index.html
│   └── images/
└── takoradi-xyz/          → Deploy to takoradi.xyz
    ├── index.html
    └── images/
```

---

## 🌐 DOMAIN DETAILS

### datumai.xyz
**Brand:** Datum
**Tagline:** "envisioning maritime supply chains of the future"
**Contact:** contact@theshipsagent.com
**Status:** Ready for deployment

### oceandatum.ai
**Brand:** Datum
**Tagline:** "envisioning maritime supply chains of the future"
**Contact:** contact@theshipsagent.com
**Status:** Ready for deployment
**Note:** Same content as datumai.xyz (both Datum brand)

### takoradi.xyz
**Brand:** Takoradi
**Tagline:** "maritime, trade, supply chain ai transformations"
**Contact:** contact@theshipsagent.com
**Status:** Ready for deployment

---

## ✅ COMPLETED WORK

- [x] Directory structure created
- [x] Landing page template copied from theshipsagent.com
- [x] Upper right content customized for each domain
- [x] Contact email links updated (contact@theshipsagent.com)
- [x] All navigation links removed (clean, simple placeholders)
- [x] Background images copied
- [x] Local testing completed

---

## 🚀 NEXT STEPS (Deployment)

### Step 1: Create GitHub Repositories
For each placeholder site, create a new repo:
- datumai-xyz
- oceandatum-ai
- takoradi-xyz

### Step 2: Initialize Git and Push
```bash
cd datumai-xyz
git init
git add .
git commit -m "Initial placeholder site for datumai.xyz"
git remote add origin https://github.com/[USERNAME]/datumai-xyz.git
git branch -M main
git push -u origin main
```

Repeat for oceandatum-ai and takoradi-xyz.

### Step 3: Configure DNS (GoDaddy)
For each domain, add these DNS records:

**A Records:**
```
Type: A, Name: @, Value: 185.199.108.153
Type: A, Name: @, Value: 185.199.109.153
Type: A, Name: @, Value: 185.199.110.153
Type: A, Name: @, Value: 185.199.111.153
```

**CNAME Record:**
```
Type: CNAME, Name: www, Value: [GITHUB_USERNAME].github.io
```

### Step 4: Configure GitHub Pages
For each repository:
1. Settings → Pages
2. Source: Deploy from branch `main`
3. Custom domain: [domain name]
4. Wait for DNS check (green checkmark)
5. Enable "Enforce HTTPS"

---

## 🔍 TESTING CHECKLIST

After deployment, verify for each domain:

- [ ] Domain loads at https://[domain]
- [ ] Shows correct brand name and tagline
- [ ] Contact email link works (opens email client)
- [ ] No other navigation links present
- [ ] HTTPS enabled (padlock icon)
- [ ] Mobile responsive design
- [ ] Background image loads
- [ ] Professional appearance

---

## 📧 CONTACT EMAIL SETUP

**Email:** contact@theshipsagent.com

**Action Required:**
1. Setup email account in GoDaddy or email provider
2. Configure forwarding to primary email if needed
3. Test receiving emails
4. Optional: Setup auto-responder

---

## 📝 DESIGN NOTES

**Template Source:** theshipsagent.com (simplified landing page)

**What's Identical:**
- Layout and structure
- Color scheme
- Typography
- Footer ("coming soon")
- Background water image
- Button/link styling
- Responsive breakpoints

**What's Different:**
- Only the upper right brand text
- Site name (Datum vs. Takoradi)
- Tagline/description

**Why This Approach:**
- Consistent branding across all placeholders
- Professional appearance
- Easy to maintain
- Quick to deploy
- Clear brand differentiation through text only

---

## 🔐 SECURITY

**Remember:**
- .env file is in .gitignore (NEVER commit credentials)
- Keep GoDaddy API keys secure
- GitHub tokens have appropriate scopes only
- HTTPS enforced on all domains

---

## 📖 DOCUMENTATION

**Full instructions:** See `/website/pages/CLAUDE_CODE_MULTI_DOMAIN_INSTRUCTIONS.md`
**Quick start:** See `/website/pages/QUICK_START_MULTI_DOMAIN.md`
**Content specs:** See `/website/pages/DOMAIN_CONTENT_SPECS.md`

---

**Status:** Local development complete ✅
**Next:** Deploy to production (GitHub Pages + DNS configuration)
