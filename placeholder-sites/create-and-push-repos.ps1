# PowerShell script to create GitHub repos and push placeholder sites
# Run this in PowerShell to deploy all 3 placeholder sites

$ErrorActionPreference = "Stop"

Write-Host "🚀 Creating GitHub repositories and deploying placeholder sites..." -ForegroundColor Cyan
Write-Host ""

# GitHub configuration
$GITHUB_USERNAME = "theshipsagent"

# Check if GITHUB_TOKEN is set
if (-not $env:GITHUB_TOKEN) {
    Write-Host "❌ ERROR: GITHUB_TOKEN environment variable not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your GitHub personal access token:" -ForegroundColor Yellow
    Write-Host '  $env:GITHUB_TOKEN = "your_token_here"' -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or create repos manually at https://github.com/new" -ForegroundColor Yellow
    exit 1
}

# Repository configurations
$repos = @(
    @{
        name = "datumai-xyz"
        description = "Placeholder site for datumai.xyz - Datum brand"
        dir = "datumai-xyz"
    },
    @{
        name = "oceandatum-ai"
        description = "Placeholder site for oceandatum.ai - Datum brand"
        dir = "oceandatum-ai"
    },
    @{
        name = "takoradi-xyz"
        description = "Placeholder site for takoradi.xyz - Takoradi brand"
        dir = "takoradi-xyz"
    }
)

foreach ($repo in $repos) {
    Write-Host "📦 Processing $($repo.name)..." -ForegroundColor Green

    # Create GitHub repository
    Write-Host "  → Creating GitHub repository..."
    $body = @{
        name = $repo.name
        description = $repo.description
        private = $false
        auto_init = $false
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
            -Method Post `
            -Headers @{
                "Authorization" = "token $env:GITHUB_TOKEN"
                "Accept" = "application/vnd.github.v3+json"
            } `
            -Body $body `
            -ContentType "application/json"

        Write-Host "  ✅ Repository created: $($response.html_url)" -ForegroundColor Green
    }
    catch {
        Write-Host "  ⚠️  Repository might already exist or error occurred" -ForegroundColor Yellow
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Yellow
    }

    # Push to GitHub
    Write-Host "  → Pushing code to GitHub..."
    Set-Location $repo.dir

    git branch -M main 2>$null
    git remote remove origin 2>$null
    git remote add origin "https://github.com/$GITHUB_USERNAME/$($repo.name).git"
    git push -u origin main --force

    Set-Location ..

    Write-Host "  ✅ $($repo.name) deployed!" -ForegroundColor Green
    Write-Host ""
}

Write-Host "✅ All repositories created and deployed!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Repository URLs:" -ForegroundColor Cyan
foreach ($repo in $repos) {
    Write-Host "  - https://github.com/$GITHUB_USERNAME/$($repo.name)" -ForegroundColor White
}
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure DNS for each domain in GoDaddy"
Write-Host "2. Enable GitHub Pages with custom domains"
Write-Host "3. Wait for DNS propagation"
Write-Host "4. Enable HTTPS"
Write-Host ""
Write-Host "📖 See MULTI_DOMAIN_IMPLEMENTATION_SUMMARY.md for detailed instructions"
