# PowerShell script to enable GitHub Pages for placeholder site repositories

$ErrorActionPreference = "Stop"

Write-Host "📄 Enabling GitHub Pages for Placeholder Sites" -ForegroundColor Cyan
Write-Host ""

# Configuration
$GITHUB_USERNAME = "theshipsagent"
$REPOS = @(
    @{ name = "datumai-xyz"; domain = "datumai.xyz" },
    @{ name = "oceandatum-ai"; domain = "oceandatum.ai" },
    @{ name = "takoradi-xyz"; domain = "takoradi.xyz" }
)

# Check for GitHub token
if (-not $env:GITHUB_TOKEN) {
    Write-Host "⚠️  GitHub token not found in environment" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPTION 1: Set token and run script (Automated)" -ForegroundColor Green
    Write-Host "  `$env:GITHUB_TOKEN = 'your_token_here'" -ForegroundColor Gray
    Write-Host "  Then run this script again" -ForegroundColor Gray
    Write-Host ""
    Write-Host "OPTION 2: Configure manually (Recommended)" -ForegroundColor Green
    Write-Host "  See instructions below" -ForegroundColor Gray
    Write-Host ""

    $response = Read-Host "Show manual configuration instructions? (y/n)"
    if ($response -eq "y") {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Cyan
        Write-Host "MANUAL GITHUB PAGES CONFIGURATION" -ForegroundColor Cyan
        Write-Host "==================================================" -ForegroundColor Cyan
        Write-Host ""

        foreach ($repo in $REPOS) {
            Write-Host "📦 Repository: $($repo.name)" -ForegroundColor Yellow
            Write-Host "🌐 Domain: $($repo.domain)" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "1. Go to: https://github.com/$GITHUB_USERNAME/$($repo.name)/settings/pages" -ForegroundColor White
            Write-Host ""
            Write-Host "2. Under 'Build and deployment':" -ForegroundColor White
            Write-Host "   - Source: Deploy from a branch" -ForegroundColor Gray
            Write-Host "   - Branch: main" -ForegroundColor Gray
            Write-Host "   - Folder: / (root)" -ForegroundColor Gray
            Write-Host "   - Click 'Save'" -ForegroundColor Gray
            Write-Host ""
            Write-Host "3. Under 'Custom domain':" -ForegroundColor White
            Write-Host "   - Enter: $($repo.domain)" -ForegroundColor Gray
            Write-Host "   - Click 'Save'" -ForegroundColor Gray
            Write-Host "   - Wait for DNS check (green checkmark ✓)" -ForegroundColor Gray
            Write-Host ""
            Write-Host "4. After DNS check passes:" -ForegroundColor White
            Write-Host "   - ✓ Check 'Enforce HTTPS'" -ForegroundColor Gray
            Write-Host ""
            Write-Host "5. Wait for site to build (1-2 minutes)" -ForegroundColor White
            Write-Host "   - Green checkmark appears when ready" -ForegroundColor Gray
            Write-Host ""
            Write-Host "6. Test: https://$($repo.domain)" -ForegroundColor White
            Write-Host ""
            Write-Host "--------------------------------------------------" -ForegroundColor DarkGray
            Write-Host ""
        }

        Write-Host "⚠️  IMPORTANT NOTES:" -ForegroundColor Yellow
        Write-Host "- DNS must be configured BEFORE custom domain will work" -ForegroundColor White
        Write-Host "- DNS check can take 5-60 minutes to pass" -ForegroundColor White
        Write-Host "- HTTPS certificate generation takes 1-24 hours" -ForegroundColor White
        Write-Host "- Sites are live at username.github.io/repo-name immediately" -ForegroundColor White
        Write-Host ""
    }

    exit 0
}

# Automated configuration with GitHub API
Write-Host "✅ GitHub token found - configuring via API..." -ForegroundColor Green
Write-Host ""

$headers = @{
    "Authorization" = "token $env:GITHUB_TOKEN"
    "Accept" = "application/vnd.github.v3+json"
}

foreach ($repo in $REPOS) {
    Write-Host "🔧 Configuring GitHub Pages for $($repo.name)..." -ForegroundColor Cyan

    try {
        # Enable GitHub Pages
        Write-Host "  → Enabling GitHub Pages (branch: main)..."
        $pagesConfig = @{
            source = @{
                branch = "main"
                path = "/"
            }
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "https://api.github.com/repos/$GITHUB_USERNAME/$($repo.name)/pages" `
            -Method Post `
            -Headers $headers `
            -Body $pagesConfig `
            -ContentType "application/json"

        Write-Host "  ✅ GitHub Pages enabled" -ForegroundColor Green

        # Wait a moment for Pages to initialize
        Start-Sleep -Seconds 3

        # Set custom domain
        Write-Host "  → Setting custom domain: $($repo.domain)..."
        $domainConfig = @{
            cname = $repo.domain
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "https://api.github.com/repos/$GITHUB_USERNAME/$($repo.name)/pages" `
            -Method Put `
            -Headers $headers `
            -Body $domainConfig `
            -ContentType "application/json"

        Write-Host "  ✅ Custom domain configured: $($repo.domain)" -ForegroundColor Green

        # Note: HTTPS enforcement must be enabled manually after DNS verification
        Write-Host "  ⚠️  Enable HTTPS manually after DNS check passes" -ForegroundColor Yellow
        Write-Host ""
    }
    catch {
        $errorMessage = $_.Exception.Message
        if ($errorMessage -match "409") {
            Write-Host "  ℹ️  GitHub Pages already enabled for $($repo.name)" -ForegroundColor Cyan
        }
        else {
            Write-Host "  ❌ Error: $errorMessage" -ForegroundColor Red
        }
        Write-Host ""
    }
}

Write-Host "✅ GitHub Pages configuration complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Wait for DNS check to pass (5-60 minutes)" -ForegroundColor White
Write-Host "2. Enable 'Enforce HTTPS' for each repo (Settings → Pages)" -ForegroundColor White
Write-Host "3. Wait for HTTPS certificate (1-24 hours)" -ForegroundColor White
Write-Host "4. Test sites:" -ForegroundColor White
foreach ($repo in $REPOS) {
    Write-Host "   - https://$($repo.domain)" -ForegroundColor Gray
}
Write-Host ""
Write-Host "🔍 Check build status:" -ForegroundColor Cyan
foreach ($repo in $REPOS) {
    Write-Host "   https://github.com/$GITHUB_USERNAME/$($repo.name)/actions" -ForegroundColor Gray
}
