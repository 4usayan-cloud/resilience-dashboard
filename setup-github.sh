#!/bin/bash

# 🚀 GitHub Deployment Steps for Resilience Dashboard

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🌍 Resilience Dashboard - GitHub Deployment Guide        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Follow these steps to deploy your dashboard online:"
echo ""

# Step 1
echo "📝 STEP 1: Create GitHub Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Open your browser and go to: https://github.com/new"
echo "2. Fill in the details:"
echo "   - Repository name: resilience-dashboard"
echo "   - Description: Live National Resilience Dashboard with Real-Time Data"
echo "   - Make it: PUBLIC (required for free GitHub Pages)"
echo "   - DON'T check 'Add README' (we already have one)"
echo "3. Click 'Create repository'"
echo ""
read -p "Press ENTER when you've created the repository..."
echo ""

# Step 2
echo "🔗 STEP 2: Get Your Repository URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "After creating the repository, copy the HTTPS URL that looks like:"
echo "   https://github.com/YOUR-USERNAME/resilience-dashboard.git"
echo ""
echo "Enter your GitHub repository URL:"
read repo_url

# Validate URL
if [[ ! $repo_url =~ ^https://github.com/.+/.+\.git$ ]]; then
    echo ""
    echo "⚠️  URL format seems incorrect. Make sure it ends with .git"
    echo "Example: https://github.com/username/resilience-dashboard.git"
    echo ""
    read -p "Enter the correct URL: " repo_url
fi

echo ""
echo "✅ Repository URL: $repo_url"
echo ""

# Step 3
echo "🔌 STEP 3: Connect Your Local Repository to GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git remote add origin "$repo_url"
echo "✅ Remote 'origin' added successfully!"
echo ""

# Step 4
echo "🚀 STEP 4: Push Your Code to GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git branch -M main
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
else
    echo ""
    echo "⚠️  Push failed. You may need to authenticate:"
    echo ""
    echo "If you see an authentication error, do one of these:"
    echo ""
    echo "Option A: Use GitHub CLI (recommended)"
    echo "  1. Install: brew install gh"
    echo "  2. Login: gh auth login"
    echo "  3. Retry: git push -u origin main"
    echo ""
    echo "Option B: Use Personal Access Token"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Generate new token (classic)"
    echo "  3. Select scopes: repo (all)"
    echo "  4. Copy the token"
    echo "  5. When prompted for password, paste the token"
    echo ""
    read -p "Press ENTER to try pushing again..." 
    git push -u origin main
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🎉 ALMOST DONE! Final Step: Enable GitHub Pages          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "STEP 5: Enable GitHub Pages"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Go to your repository on GitHub"
echo "2. Click 'Settings' (top right)"
echo "3. Click 'Pages' (left sidebar)"
echo "4. Under 'Build and deployment':"
echo "   - Source: Select 'GitHub Actions'"
echo "5. Wait 2-3 minutes for automatic deployment"
echo "6. Refresh the Pages settings page"
echo "7. You'll see: 'Your site is live at https://...'"
echo ""

# Extract username and repo name from URL
repo_path=$(echo "$repo_url" | sed 's/https:\/\/github.com\///' | sed 's/\.git$//')
username=$(echo "$repo_path" | cut -d'/' -f1)
reponame=$(echo "$repo_path" | cut -d'/' -f2)

echo "════════════════════════════════════════════════════════════"
echo ""
echo "🌐 Your dashboard will be live at:"
echo ""
echo "   https://${username}.github.io/${reponame}/"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "✨ Features available on your live dashboard:"
echo "   • Real-time data from 11 APIs"
echo "   • 8 timezone displays with DST"
echo "   • Interactive map with 253 countries"
echo "   • Auto-refresh every 5 minutes"
echo "   • Fully responsive (mobile, tablet, desktop)"
echo ""
echo "📖 For more details, see DEPLOYMENT.md"
echo ""
echo "🎊 Congratulations! Your dashboard is now online!"
echo ""
