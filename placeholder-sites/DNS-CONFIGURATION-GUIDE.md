# DNS Configuration Guide for GitHub Pages

**Domains to configure:**
- datumai.xyz
- oceandatum.ai
- takoradi.xyz

---

## 🎯 DNS Records Needed

For **each domain**, you need to add:

### A Records (4 total)
These point your domain to GitHub Pages servers.

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 185.199.108.153 | 600 |
| A | @ | 185.199.109.153 | 600 |
| A | @ | 185.199.110.153 | 600 |
| A | @ | 185.199.111.153 | 600 |

### CNAME Record (1 total)
This handles the www subdomain.

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | theshipsagent.github.io | 3600 |

---

## 📋 MANUAL CONFIGURATION (GoDaddy Web Interface)

### For datumai.xyz

1. **Login to GoDaddy**
   - Go to: https://dcc.godaddy.com/manage/dns
   - Or: My Products → Domains → Manage DNS

2. **Select datumai.xyz**

3. **Add A Records**
   - Click "Add" button
   - For each of the 4 IP addresses:
     - Type: **A**
     - Name: **@**
     - Value: **[IP address from table above]**
     - TTL: **600** (or Custom: 10 minutes)
   - Click "Save"
   - Repeat 4 times for all 4 IPs

4. **Add CNAME Record**
   - Click "Add" button
   - Type: **CNAME**
   - Name: **www**
   - Value: **theshipsagent.github.io**
   - TTL: **3600** (or 1 hour)
   - Click "Save"

5. **Remove conflicting records (if any)**
   - If you see existing A records for @ or CNAME for www
   - Delete them (they'll conflict with the new ones)

6. **Save all changes**

### For oceandatum.ai

Repeat steps 1-6 above, but select **oceandatum.ai** in step 2.

### For takoradi.xyz

Repeat steps 1-6 above, but select **takoradi.xyz** in step 2.

---

## 🤖 AUTOMATED CONFIGURATION (Using GoDaddy API)

If you have GoDaddy API credentials, you can automate this:

### Step 1: Set API Credentials

```powershell
$env:GODADDY_API_KEY = "your_key_here"
$env:GODADDY_API_SECRET = "your_secret_here"
```

### Step 2: Run Configuration Script

```powershell
cd "G:\My Drive\LLM\theshipsagent.github.io\placeholder-sites"
pwsh -File configure-dns.ps1
```

### How to Get GoDaddy API Credentials

1. Login to GoDaddy Developer Portal: https://developer.godaddy.com/keys
2. Click "Create New API Key"
3. Environment: **Production**
4. Name it: "GitHub Pages DNS Configuration"
5. Copy the **Key** and **Secret** (shown only once!)
6. Save them securely

---

## ✅ VERIFICATION

After configuring DNS (manual or automated), verify the records:

### Check DNS Propagation

**Using nslookup (Windows PowerShell):**

```powershell
nslookup datumai.xyz
nslookup oceandatum.ai
nslookup takoradi.xyz
```

**Expected output:**
```
Non-authoritative answer:
Name:    datumai.xyz
Addresses:  185.199.108.153
            185.199.109.153
            185.199.110.153
            185.199.111.153
```

### Online DNS Check

Use these tools to verify propagation:
- https://www.whatsmydns.net/
- https://dnschecker.org/

Enter your domain and check for:
- **A records** showing all 4 GitHub IPs
- **CNAME record** for www showing theshipsagent.github.io

---

## ⏱️ TIMELINE

| Step | Time |
|------|------|
| Add DNS records in GoDaddy | 5 minutes |
| DNS propagation starts | Immediate |
| DNS visible in some locations | 5-30 minutes |
| DNS fully propagated globally | 30-60 minutes |
| Maximum propagation time | Up to 24 hours |

**Typical:** Most DNS changes propagate in 15-30 minutes.

---

## 🚨 TROUBLESHOOTING

### "DNS Check Failed" in GitHub Pages

**Cause:** DNS not propagated yet
**Solution:** Wait 15-30 minutes, try again

### nslookup shows old/wrong IP addresses

**Cause:** DNS cache
**Solution:**
```powershell
ipconfig /flushdns
nslookup datumai.xyz
```

### Can't add A record - "Record already exists"

**Cause:** Conflicting existing record
**Solution:**
1. Find existing A record for @
2. Delete it
3. Add the 4 new GitHub A records

### CNAME shows "parking page" or wrong destination

**Cause:** Old CNAME still active
**Solution:**
1. Delete old CNAME for www
2. Add new CNAME pointing to theshipsagent.github.io

---

## 📊 DNS CONFIGURATION CHECKLIST

### datumai.xyz
- [ ] 4 A records added (185.199.108/109/110/111.153)
- [ ] 1 CNAME record added (www → theshipsagent.github.io)
- [ ] Old conflicting records removed
- [ ] Changes saved in GoDaddy
- [ ] DNS propagation verified with nslookup
- [ ] Online DNS checker shows correct records

### oceandatum.ai
- [ ] 4 A records added (185.199.108/109/110/111.153)
- [ ] 1 CNAME record added (www → theshipsagent.github.io)
- [ ] Old conflicting records removed
- [ ] Changes saved in GoDaddy
- [ ] DNS propagation verified with nslookup
- [ ] Online DNS checker shows correct records

### takoradi.xyz
- [ ] 4 A records added (185.199.108/109/110/111.153)
- [ ] 1 CNAME record added (www → theshipsagent.github.io)
- [ ] Old conflicting records removed
- [ ] Changes saved in GoDaddy
- [ ] DNS propagation verified with nslookup
- [ ] Online DNS checker shows correct records

---

## 📱 QUICK REFERENCE

**Copy/paste these values when adding records:**

### A Records (add all 4):
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### CNAME Record:
```
theshipsagent.github.io
```

---

## ➡️ NEXT STEPS

After DNS is configured and propagated:

1. **Enable GitHub Pages** for each repository
   - Go to: Repository → Settings → Pages
   - Source: Deploy from branch `main`
   - Custom domain: [your domain]
   - Wait for DNS check ✅
   - Enable "Enforce HTTPS"

2. **Test the live sites**
   - https://datumai.xyz
   - https://oceandatum.ai
   - https://takoradi.xyz

3. **Verify HTTPS**
   - May take 1-24 hours after DNS verification
   - GitHub auto-generates SSL certificates

---

## 🆘 NEED HELP?

**GoDaddy Support:**
- https://www.godaddy.com/help/manage-dns-680

**GitHub Pages DNS:**
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

**DNS Propagation:**
- https://www.whatsmydns.net/

---

**You're ready to configure DNS!** Choose manual or automated method above.
