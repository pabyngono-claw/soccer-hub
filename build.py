#!/usr/bin/env python3
"""
build.py - Inject environment variables into HTML files at build time.
Python version - handles special characters in URLs better than sed.
"""

import os
import sys
import re

# Required environment variables
REQUIRED_VARS = [
    "XANO_BASE_URL",
    "XANO_API_KEY", 
    "MEMBERSTACK_PUBLIC_KEY",
    "AIRTABLE_BASE_ID",
    "AIRTABLE_API_KEY"
]

FILES = ["index.html", "match.html", "dashboard.html"]

def check_env_vars():
    """Verify all required env vars are set."""
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)
    print("✅ All required environment variables present")

def process_file(filepath):
    """Process a single HTML file, replacing placeholders with env values."""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Get env values
    xano_base = os.getenv("XANO_BASE_URL", "")
    xano_key = os.getenv("XANO_API_KEY", "")
    ms_key = os.getenv("MEMBERSTACK_PUBLIC_KEY", "")
    airtable_base = os.getenv("AIRTABLE_BASE_ID", "")
    airtable_key = os.getenv("AIRTABLE_API_KEY", "")
    
    # Replacements - using string replace (no regex needed for simple patterns)
    replacements = {
        # window.ENV?.VAR || 'fallback' patterns
        "window.ENV?.XANO_BASE_URL || 'https://your-workspace.xano.io/api:your-group'": xano_base,
        "window.ENV?.XANO_API_KEY || ''": xano_key,
        "window.ENV?.MEMBERSTACK_PUBLIC_KEY || ''": ms_key,
        "window.ENV?.AIRTABLE_BASE_ID || ''": airtable_base,
        "window.ENV?.AIRTABLE_API_KEY || ''": airtable_key,
        
        # Direct placeholder patterns
        "YOUR_MEMBERSTACK_PUBLIC_KEY": ms_key,
        "YOUR_API_KEY_HERE": xano_base,  # Used in script tags
    }
    
    # Apply all replacements
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {filepath} updated")
    else:
        print(f"  ℹ️  {filepath} no changes needed")

def verify_clean():
    """Verify no placeholders remain in processed files."""
    patterns = [
        "YOUR_MEMBERSTACK_PUBLIC_KEY",
        "YOUR_API_KEY_HERE",
        "window.ENV?.XANO_BASE_URL",
        "window.ENV?.XANO_API_KEY", 
        "window.ENV?.MEMBERSTACK_PUBLIC_KEY",
        "window.ENV?.AIRTABLE_BASE_ID",
        "window.ENV?.AIRTABLE_API_KEY",
    ]
    
    all_clean = True
    for filepath in FILES:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found = [p for p in patterns if p in content]
            if found:
                print(f"⚠️  {filepath} still contains: {', '.join(found)}")
                all_clean = False
            else:
                print(f"  ✅ {filepath} clean")
    
    return all_clean

def main():
    print("🔧 Injecting environment variables into HTML files...")
    print("=" * 50)
    
    check_env_vars()
    print()
    
    for filepath in FILES:
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"  ⚠️  {filepath} not found")
    
    print()
    print("=" * 50)
    print("🔍 Verifying no placeholders remain...")
    clean = verify_clean()
    
    if clean:
        print()
        print("✅ Build complete - all environment variables injected successfully!")
        sys.exit(0)
    else:
        print()
        print("❌ Build failed - some placeholders remain")
        sys.exit(1)

if __name__ == "__main__":
    main()