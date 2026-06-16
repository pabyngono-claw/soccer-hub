#!/bin/bash
# build.sh - Inject environment variables into HTML files at build time
# Usage: ./build.sh
# Run this script in Cloudflare Pages build step or GitHub Actions

set -e

echo "🔧 Injecting environment variables into HTML files..."

# List of HTML files to process
FILES=("index.html" "match.html" "dashboard.html")

# Environment variables to inject (must be set in Cloudflare Pages or GitHub Actions)
# XANO_BASE_URL, XANO_API_KEY, MEMBERSTACK_PUBLIC_KEY, AIRTABLE_BASE_ID, AIRTABLE_API_KEY

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        
        # Create a temporary file with replacements
        sed -i \
            -e "s|window\.ENV\?\.XANO_BASE_URL|$XANO_BASE_URL|g" \
            -e "s|window\.ENV\?\.XANO_API_KEY|$XANO_API_KEY|g" \
            -e "s|window\.ENV\?\.MEMBERSTACK_PUBLIC_KEY|$MEMBERSTACK_PUBLIC_KEY|g" \
            -e "s|window\.ENV\?\.AIRTABLE_BASE_ID|$AIRTABLE_BASE_ID|g" \
            -e "s|window\.ENV\?\.AIRTABLE_API_KEY|$AIRTABLE_API_KEY|g" \
            "$file"
        
        echo "  ✅ $file processed"
    else
        echo "  ⚠️  $file not found"
    fi
done

echo "✅ Build complete - environment variables injected"