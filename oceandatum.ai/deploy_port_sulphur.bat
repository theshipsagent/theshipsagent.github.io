@echo off
REM Port Sulphur Report Deployment Script
REM This script adds only the Port Sulphur project files and pushes to GitHub

echo ========================================
echo Port Sulphur Report Deployment
echo ========================================
echo.

REM Navigate to repository
cd /d "G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai"

echo Step 1: Adding Port Sulphur project files...
git add projects/port-sulphur-report/
git add projects/port-sulphur-midstream.html

echo.
echo Step 2: Checking status...
git status

echo.
echo Step 3: Ready to commit. Press any key to continue or Ctrl+C to cancel...
pause > nul

git commit -m "Add Port Sulphur Terminal comprehensive report

- Interactive report with 17 sections (environmental, navigation, infrastructure, weather, property, images, market, midstream, history, econometrics, CAPEX, permitting, due diligence, engineering, geospatial, permits, executive summary)
- ESRI ArcGIS maps with bathymetry, navigation channels, property boundaries, and environmental zones
- 60+ Chart.js visualizations for data presentation
- Standalone midstream operations page with detailed cost analysis
- Responsive design matching oceandatum.ai brand
- 601 source documents synthesized into 593 KB interactive report
- Mobile-optimized with touch-friendly navigation
- Fixed JavaScript visibility issue on history tab"

echo.
echo Step 4: Pushing to GitHub (this will trigger automatic deployment)...
echo Press any key to push or Ctrl+C to cancel...
pause > nul

git push origin main

echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo.
echo Your report will be live in 1-2 minutes at:
echo https://oceandatum.ai/projects/port-sulphur-report/port-sulphur-report.html
echo.
echo Midstream page:
echo https://oceandatum.ai/projects/port-sulphur-midstream.html
echo.
echo Check deployment status:
echo https://github.com/theshipsagent/oceandatum-ai/actions
echo.
pause
