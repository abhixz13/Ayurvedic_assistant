#!/bin/bash

# Ayurvedic Diagnostic Assistant - GitHub Setup Script

echo "🚀 Setting up GitHub repository for Ayurvedic Diagnostic Assistant"
echo "================================================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Check if we have commits
if ! git log --oneline -1 > /dev/null 2>&1; then
    echo "❌ No commits found. Please make an initial commit first."
    exit 1
fi

echo "✅ Git repository is ready"
echo ""

echo "📋 Next Steps:"
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'Ayurvedic_Diagnostic_Assistant'"
echo "3. Make it Public or Private (your choice)"
echo "4. DO NOT initialize with README, .gitignore, or license"
echo "5. Click 'Create repository'"
echo ""

echo "🔗 After creating the repository, you'll see a URL like:"
echo "   https://github.com/YOUR_USERNAME/Ayurvedic_Diagnostic_Assistant.git"
echo ""

read -p "Enter your GitHub repository URL: " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

echo ""
echo "🔧 Adding remote origin..."
git remote add origin "$repo_url"

echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Success! Your code has been pushed to GitHub."
echo "🌐 Visit your repository at: $repo_url"
echo ""
echo "📝 Repository includes:"
echo "   - Complete Ayurvedic Diagnostic Assistant"
echo "   - Interactive display system"
echo "   - RAG (Retrieval-Augmented Generation) system"
echo "   - Jupyter notebook interface"
echo "   - Comprehensive documentation"
echo "   - Example usage scripts"
echo ""
echo "🎉 Your project is now live on GitHub!" 