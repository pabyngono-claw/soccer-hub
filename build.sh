#!/bin/bash
# build.sh - Inject environment variables into HTML files at build time
# Run this script in GitHub Actions before wrangler deploy

set -e

echo "🔧 Injecting environment variables into HTML files..."

# Required env vars (set in GitHub Actions secrets)
# XANO_BASE_URL, XANO_API_KEY, MEMBERSTACK_PUBLIC_KEY, AIRTABLE_BASE_ID, AIRTABLE_API_KEY

# List of HTML files to process
FILES=("index.html" "match.html" "dashboard.html")

# Check required env vars
for var in XANO_BASE_URL XANO_API_KEY MEMBERSTACK_PUBLIC_KEY AIRTABLE_BASE_ID AIRTABLE_API_KEY; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing required environment variable: $var"
        exit 1
    fi
done

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        
        # Replace placeholder patterns with actual secret values
        sed -i \
            -e "s|window\\.ENV\\?\\.XANO_BASE_URL || 'https://your-workspace.xano.io/api:your-group'|$XANO_BASE_URL|g" \
            -e "s|window\\.ENV\\?\\.XANO_API_KEY || ''|$XANO_API_KEY|g" \
            -e "s|window\\.ENV\\?\\.MEMBERSTACK_PUBLIC_KEY || ''|$MEMBERSTACK_PUBLIC_KEY|g" \
            -e "s|window\\.ENV\\?\\.AIRTABLE_BASE_ID || ''|$AIRTABLE_BASE_ID|g" \
            -e "s|window\\.ENV\\?\\.AIRTABLE_API_KEY || ''|$AIRTABLE_API_KEY|g" \
            -e "s|YOUR_MEMBERSTACK_PUBLIC_KEY|$MEMBERSTACK_PUBLIC_KEY|g" \
            -e "s|YOUR_API_KEY_HERE|$XANO_BASE_URL|g" \
            "$file"
        
        echo "  ✅ $file processed"
    else
        echo "  ⚠️  $file not found"
    fi
done

echo "✅ Build complete - environment variables injected"

# Verify no placeholders remain
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "YOUR_MEMBERSTACK_PUBLIC_KEY\|YOUR_API_KEY_HERE\|window.ENV" "$file"; then
            echo "⚠️  $file still contains placeholders:"
            grep -n "YOUR_MEMBERSTACK_PUBLIC_KEY\|YOUR_API_KEY_HERE\|window.ENV" "$file"
        else
            echo "  ✅ $file clean"
        fi
    fi
done