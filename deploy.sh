#!/bin/bash

# Deploy script for Nashville Dog Training website
# Usage: ./deploy.sh "Your commit message"

set -e

# Default commit message if none provided
MESSAGE="${1:-Update site}"

# Add all files
git add -A

# Commit with message
git commit -m "$MESSAGE"

# Push to origin main
git push origin main

echo "Deployed successfully!"
