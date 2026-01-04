#!/bin/bash
# Deploy placeholder sites to GitHub
# Run this script to create repos and push code

set -e  # Exit on error

echo "🚀 Deploying placeholder sites to GitHub..."
echo ""

# GitHub username (update this!)
GITHUB_USERNAME="theshipsagent"

# Repository names
REPOS=("datumai-xyz" "oceandatum-ai" "takoradi-xyz")

# Function to create repo and push
deploy_repo() {
    local repo_name=$1
    local dir_name=$2

    echo "📦 Processing $repo_name..."

    # Create GitHub repository using API
    echo "  → Creating GitHub repository..."
    curl -X POST \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"${repo_name}\",\"description\":\"Placeholder site for ${repo_name//-/.}\",\"private\":false,\"auto_init\":false}"

    echo "  → Adding remote and pushing..."
    cd "$dir_name"
    git branch -M main
    git remote add origin "https://github.com/${GITHUB_USERNAME}/${repo_name}.git"
    git push -u origin main
    cd ..

    echo "  ✅ $repo_name deployed!"
    echo ""
}

# Deploy each repository
for repo in "${REPOS[@]}"; do
    deploy_repo "$repo" "$repo"
done

echo "✅ All repositories deployed!"
echo ""
echo "🌐 Next steps:"
echo "1. Configure DNS for each domain in GoDaddy"
echo "2. Enable GitHub Pages with custom domains"
echo "3. Wait for DNS propagation"
echo "4. Enable HTTPS"
echo ""
echo "📖 See MULTI_DOMAIN_IMPLEMENTATION_SUMMARY.md for detailed instructions"
