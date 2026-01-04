# PowerShell script to configure DNS for GitHub Pages
# Configures DNS records for all 3 placeholder domains

$ErrorActionPreference = "Stop"

Write-Host "🌐 DNS Configuration for GitHub Pages" -ForegroundColor Cyan
Write-Host ""

# GitHub Pages IP addresses (A records)
$GITHUB_IPS = @(
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153"
)

# Domains to configure
$DOMAINS = @(
    "datumai.xyz",
    "oceandatum.ai",
    "takoradi.xyz"
)

# Check for GoDaddy credentials
if (-not $env:GODADDY_API_KEY -or -not $env:GODADDY_API_SECRET) {
    Write-Host "⚠️  GoDaddy API credentials not found in environment" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPTION 1: Set credentials and run script" -ForegroundColor Green
    Write-Host "  `$env:GODADDY_API_KEY = 'your_key'" -ForegroundColor Gray
    Write-Host "  `$env:GODADDY_API_SECRET = 'your_secret'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "OPTION 2: Configure DNS manually" -ForegroundColor Green
    Write-Host "  See DNS-CONFIGURATION-GUIDE.md for step-by-step instructions" -ForegroundColor Gray
    Write-Host ""

    $response = Read-Host "Do you want to see manual configuration instructions? (y/n)"
    if ($response -eq "y") {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Cyan
        Write-Host "MANUAL DNS CONFIGURATION INSTRUCTIONS" -ForegroundColor Cyan
        Write-Host "==================================================" -ForegroundColor Cyan
        Write-Host ""

        foreach ($domain in $DOMAINS) {
            Write-Host "📋 $domain" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "1. Login to GoDaddy: https://dcc.godaddy.com/manage/dns" -ForegroundColor White
            Write-Host "2. Select domain: $domain" -ForegroundColor White
            Write-Host "3. Add the following DNS records:" -ForegroundColor White
            Write-Host ""

            Write-Host "   A RECORDS (add all 4):" -ForegroundColor Green
            foreach ($ip in $GITHUB_IPS) {
                Write-Host "   - Type: A, Name: @, Value: $ip, TTL: 600" -ForegroundColor Gray
            }
            Write-Host ""

            Write-Host "   CNAME RECORD:" -ForegroundColor Green
            Write-Host "   - Type: CNAME, Name: www, Value: theshipsagent.github.io, TTL: 3600" -ForegroundColor Gray
            Write-Host ""
            Write-Host "4. Save changes" -ForegroundColor White
            Write-Host ""
            Write-Host "--------------------------------------------------" -ForegroundColor DarkGray
            Write-Host ""
        }

        Write-Host "⏱️  DNS propagation takes 5-60 minutes (sometimes up to 24 hours)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "🔍 Check propagation status:" -ForegroundColor Cyan
        foreach ($domain in $DOMAINS) {
            Write-Host "   nslookup $domain" -ForegroundColor Gray
        }
        Write-Host ""
    }

    exit 0
}

# If credentials are available, configure via API
Write-Host "✅ GoDaddy credentials found - configuring via API..." -ForegroundColor Green
Write-Host ""

$headers = @{
    "Authorization" = "sso-key $($env:GODADDY_API_KEY):$($env:GODADDY_API_SECRET)"
    "Content-Type" = "application/json"
}

foreach ($domain in $DOMAINS) {
    Write-Host "🔧 Configuring DNS for $domain..." -ForegroundColor Cyan

    # Prepare A records
    $aRecords = @()
    foreach ($ip in $GITHUB_IPS) {
        $aRecords += @{
            type = "A"
            name = "@"
            data = $ip
            ttl = 600
        }
    }

    # Prepare CNAME record
    $cnameRecord = @{
        type = "CNAME"
        name = "www"
        data = "theshipsagent.github.io"
        ttl = 3600
    }

    try {
        # Get existing records
        Write-Host "  → Fetching existing DNS records..."
        $existingRecords = Invoke-RestMethod -Uri "https://api.godaddy.com/v1/domains/$domain/records" `
            -Method Get `
            -Headers $headers

        # Filter out old A and CNAME records for @ and www
        $keepRecords = $existingRecords | Where-Object {
            -not (($_.type -eq "A" -and $_.name -eq "@") -or ($_.type -eq "CNAME" -and $_.name -eq "www"))
        }

        # Combine with new records
        $allRecords = $keepRecords + $aRecords + $cnameRecord

        # Update DNS records
        Write-Host "  → Updating DNS records..."
        Invoke-RestMethod -Uri "https://api.godaddy.com/v1/domains/$domain/records" `
            -Method Put `
            -Headers $headers `
            -Body ($allRecords | ConvertTo-Json -Depth 10) `
            -ContentType "application/json"

        Write-Host "  ✅ DNS configured for $domain" -ForegroundColor Green
        Write-Host ""
    }
    catch {
        Write-Host "  ❌ Error configuring $domain" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
    }
}

Write-Host "✅ DNS configuration complete!" -ForegroundColor Green
Write-Host ""
Write-Host "⏱️  DNS propagation typically takes 5-60 minutes" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔍 Verify DNS propagation with:" -ForegroundColor Cyan
foreach ($domain in $DOMAINS) {
    Write-Host "   nslookup $domain" -ForegroundColor White
}
Write-Host ""
Write-Host "📋 Next step: Enable GitHub Pages for each repository"
Write-Host "   See MULTI_DOMAIN_IMPLEMENTATION_SUMMARY.md"
