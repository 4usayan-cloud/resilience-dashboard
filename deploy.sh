#!/bin/bash

# 🚀 Quick Deploy Script for Resilience Dashboard
# This script helps you deploy to GitHub Pages in one command

echo "🌍 Resilience Dashboard - Quick Deploy Script"
echo "=============================================="
echo ""

# Check if Git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo "📝 Setting up GitHub repository..."
    echo ""
    echo "Please enter your GitHub username:"
    read github_username
    
    echo ""
    echo "Please enter your repository name (default: resilience-dashboard):"
    read repo_name
    repo_name=${repo_name:-resilience-dashboard}
    
    git remote add origin "https://github.com/${github_username}/${repo_name}.git"
    echo "✅ Remote added: https://github.com/${github_username}/${repo_name}"
else
    echo "✅ Git remote already configured"
fi

# Stage and commit changes
echo ""
echo "📦 Staging changes..."
git add -A

echo ""
echo "Please enter commit message (default: Update dashboard):"
read commit_msg
commit_msg=${commit_msg:-Update dashboard}

git commit -m "$commit_msg"

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=============================================="
echo "✨ Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Click Settings → Pages"
echo "3. Set Source to 'GitHub Actions'"
echo "4. Wait 2-3 minutes for deployment"
echo ""
echo "Your dashboard will be live at:"
echo "https://${github_username}.github.io/${repo_name}/"
echo ""
echo "🎉 Happy deploying!"
