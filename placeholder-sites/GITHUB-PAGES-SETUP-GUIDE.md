# GitHub Pages Setup Guide

**Complete step-by-step instructions for enabling GitHub Pages on all 3 placeholder repositories**

---

## 📋 PREREQUISITES

Before enabling GitHub Pages, ensure:

- [x] GitHub repositories created
  - datumai-xyz
  - oceandatum-ai
  - takoradi-xyz
- [x] Code pushed to `main` branch
- [ ] DNS configured in GoDaddy (A records + CNAME)
- [ ] DNS propagation verified with `nslookup`

**NOTE:** DNS must be configured before custom domains will work!

---

## 🚀 QUICK SETUP (All 3 Repositories)

### Step 1: datumai-xyz

**Navigate to repository settings:**
https://github.com/theshipsagent/datumai-xyz/settings/pages

**Configure GitHub Pages:**

1. **Source:**
   - Deploy from a branch
   - Branch: `main`
   - Folder: `/ (root)`
   - Click **Save**

2. **Custom domain:**
   - Enter: `datumai.xyz`
   - Click **Save**
   - ⏳ Wait for DNS check (shows ✓ when ready)

3. **Enforce HTTPS:**
   - ⚠️ Only available AFTER DNS check passes
   - ✓ Check "Enforce HTTPS"
   - Click **Save**

4. **Verify deployment:**
   - Check: https://github.com/theshipsagent/datumai-xyz/deployments
   - Status should show: ✅ Active

5. **Test live site:**
   - Visit: https://datumai.xyz
   - Should show: "Datum - envisioning maritime supply chains of the future"

---

### Step 2: oceandatum-ai

**Navigate to repository settings:**
https://github.com/theshipsagent/oceandatum-ai/settings/pages

**Configure GitHub Pages:**

1. **Source:**
   - Deploy from a branch
   - Branch: `main`
   - Folder: `/ (root)`
   - Click **Save**

2. **Custom domain:**
   - Enter: `oceandatum.ai`
   - Click **Save**
   - ⏳ Wait for DNS check (shows ✓ when ready)

3. **Enforce HTTPS:**
   - ⚠️ Only available AFTER DNS check passes
   - ✓ Check "Enforce HTTPS"
   - Click **Save**

4. **Verify deployment:**
   - Check: https://github.com/theshipsagent/oceandatum-ai/deployments
   - Status should show: ✅ Active

5. **Test live site:**
   - Visit: https://oceandatum.ai
   - Should show: "Datum - envisioning maritime supply chains of the future"

---

### Step 3: takoradi-xyz

**Navigate to repository settings:**
https://github.com/theshipsagent/takoradi-xyz/settings/pages

**Configure GitHub Pages:**

1. **Source:**
   - Deploy from a branch
   - Branch: `main`
   - Folder: `/ (root)`
   - Click **Save**

2. **Custom domain:**
   - Enter: `takoradi.xyz`
   - Click **Save**
   - ⏳ Wait for DNS check (shows ✓ when ready)

3. **Enforce HTTPS:**
   - ⚠️ Only available AFTER DNS check passes
   - ✓ Check "Enforce HTTPS"
   - Click **Save**

4. **Verify deployment:**
   - Check: https://github.com/theshipsagent/takoradi-xyz/deployments
   - Status should show: ✅ Active

5. **Test live site:**
   - Visit: https://takoradi.xyz
   - Should show: "Takoradi - maritime, trade, supply chain ai transformations"

---

## ⏱️ TIMELINE

| Step | Time |
|------|------|
| Enable GitHub Pages (each repo) | 2 minutes |
| Initial site deployment | 1-3 minutes |
| Add custom domain | 1 minute |
| DNS check to pass | 5-60 minutes |
| HTTPS certificate generation | 1-24 hours |
| **Total time per repo** | **10-90 minutes** |

**Note:** You can configure all 3 repos simultaneously. They'll all be waiting for DNS checks at the same time.

---

## 🔍 VERIFICATION CHECKLIST

### datumai-xyz
- [ ] GitHub Pages enabled (Source: main branch)
- [ ] Custom domain added (datumai.xyz)
- [ ] DNS check passed (✓ green checkmark)
- [ ] HTTPS enforced
- [ ] Site accessible: https://datumai.xyz
- [ ] Content correct: "Datum" branding
- [ ] Contact email link works
- [ ] HTTPS enabled (padlock icon in browser)

### oceandatum-ai
- [ ] GitHub Pages enabled (Source: main branch)
- [ ] Custom domain added (oceandatum.ai)
- [ ] DNS check passed (✓ green checkmark)
- [ ] HTTPS enforced
- [ ] Site accessible: https://oceandatum.ai
- [ ] Content correct: "Datum" branding
- [ ] Contact email link works
- [ ] HTTPS enabled (padlock icon in browser)

### takoradi-xyz
- [ ] GitHub Pages enabled (Source: main branch)
- [ ] Custom domain added (takoradi.xyz)
- [ ] DNS check passed (✓ green checkmark)
- [ ] HTTPS enforced
- [ ] Site accessible: https://takoradi.xyz
- [ ] Content correct: "Takoradi" branding
- [ ] Contact email link works
- [ ] HTTPS enabled (padlock icon in browser)

---

## 🚨 TROUBLESHOOTING

### "DNS check failed" error

**Cause:** DNS not configured or not propagated yet

**Solutions:**
1. Verify DNS is configured correctly in GoDaddy
2. Wait 15-30 minutes for DNS propagation
3. Check DNS with: `nslookup datumai.xyz`
4. Try removing and re-adding custom domain

---

### "Domain is already taken" error

**Cause:** Domain configured in another GitHub repo

**Solutions:**
1. Check if domain used in another repo
2. Remove domain from other repo first
3. GitHub Pages allows ONE repo per custom domain

---

### Site shows 404 error

**Cause:** GitHub Pages not finding index.html

**Solutions:**
1. Verify `index.html` exists in repo root
2. Check branch is set to `main` (not `master`)
3. Check folder is set to `/ (root)` (not `/docs`)
4. Wait 2-3 minutes for deployment to complete

---

### HTTPS not available

**Cause:** Certificate not generated yet

**Solutions:**
1. Verify DNS check passed (✓ green checkmark)
2. Wait up to 24 hours for certificate generation
3. GitHub auto-generates Let's Encrypt certificates
4. Can't manually trigger - just wait
5. Site works without HTTPS during this time

---

### Site loads but shows wrong content

**Cause:** Browser cache or old deployment

**Solutions:**
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Try incognito/private browsing window
4. Check deployment status in repo

---

## 📊 DEPLOYMENT STATUS

Check build and deployment status:

- **datumai-xyz:** https://github.com/theshipsagent/datumai-xyz/actions
- **oceandatum-ai:** https://github.com/theshipsagent/oceandatum-ai/actions
- **takoradi-xyz:** https://github.com/theshipsagent/takoradi-xyz/actions

**Green checkmark (✓)** = Deployment successful
**Red X** = Deployment failed (check logs)

---

## 🔐 SECURITY NOTES

### CNAME file

When you add a custom domain, GitHub creates a `CNAME` file in your repo:
- This is normal and expected
- Contains just your domain name
- Don't delete it (GitHub Pages needs it)
- Will appear in next git pull

### HTTPS enforcement

- Always enable HTTPS after DNS check passes
- Protects visitor data with encryption
- Required for modern browser features
- Free via Let's Encrypt (GitHub handles it)

---

## 📱 TESTING CHECKLIST

After all sites are deployed, test thoroughly:

### Functionality Tests
- [ ] All 3 domains load without errors
- [ ] Contact email links open email client
- [ ] Background images load correctly
- [ ] Text displays properly (no encoding issues)
- [ ] Footer shows "coming soon"

### Mobile Responsive Tests
- [ ] Sites display properly on mobile (use browser dev tools)
- [ ] Text is readable on small screens
- [ ] Images scale appropriately
- [ ] Layout doesn't break

### Cross-Browser Tests
- [ ] Test in Chrome
- [ ] Test in Firefox
- [ ] Test in Edge
- [ ] Test in Safari (if available)

### Performance Tests
- [ ] Sites load quickly (<3 seconds)
- [ ] No console errors (check browser dev tools)
- [ ] Images optimized

---

## 📈 POST-DEPLOYMENT

After sites are live:

### Monitor
- Check GitHub Actions for deployment errors
- Monitor site uptime
- Check for any DNS issues

### Document
- Update MULTI_DOMAIN_IMPLEMENTATION_SUMMARY.md
- Mark sites as "LIVE" in status tracking

### Announce
- Update any business cards/materials
- Verify contact@theshipsagent.com is working
- Test email delivery

---

## 🎯 SUCCESS CRITERIA

**Project is complete when:**

✅ All 3 placeholder sites are live:
- https://datumai.xyz
- https://oceandatum.ai
- https://takoradi.xyz

✅ All sites show correct content:
- Proper branding (Datum or Takoradi)
- Correct taglines
- Working contact email links

✅ All sites secured:
- HTTPS enabled
- Green padlock in browsers
- No security warnings

✅ All sites accessible:
- Load quickly (<3 seconds)
- Mobile responsive
- Cross-browser compatible

---

## 🆘 NEED HELP?

**GitHub Pages Documentation:**
- https://docs.github.com/en/pages

**GitHub Pages Custom Domain:**
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

**GitHub Support:**
- https://support.github.com/

**DNS Issues:**
- See: DNS-CONFIGURATION-GUIDE.md

---

**You're ready to enable GitHub Pages!**

Follow the steps above for each repository. Start with all 3 simultaneously - they can all be configured in parallel.

**Estimated total time:** 30 minutes active work + waiting for DNS/HTTPS
