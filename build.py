#!/usr/bin/env python3
# build.py - Inject environment variables into HTML files at build time.

import os
import sys

REQUIRED_VARS = ["XANO_BASE_URL", "XANO_API_KEY", "MEMBERSTACK_PUBLIC_KEY", "AIRTABLE_BASE_ID", "AIRTABLE_API_KEY"]
FILES = ["index.html", "match.html", "dashboard.html"]

def check_env():
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        print("ERROR: Missing " + ", ".join(missing))
        sys.exit(1)
    print("OK: All env vars present")

def process(fpath):
    print("Processing " + fpath + "...")
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    
    xb = os.getenv("XANO_BASE_URL", "")
    xk = os.getenv("XANO_API_KEY", "")
    mk = os.getenv("MEMBERSTACK_PUBLIC_KEY", "")
    ab = os.getenv("AIRTABLE_BASE_ID", "")
    ak = os.getenv("AIRTABLE_API_KEY", "")
    
    xb_q = "'" + xb + "'"
    xk_q = "'" + xk + "'"
    mk_q = "'" + mk + "'"
    ab_q = "'" + ab + "'"
    ak_q = "'" + ak + "'"
    
    # Build replacements manually to avoid dict syntax issues
    c = c.replace("window.ENV?.XANO_BASE_URL || 'https://your-workspace.xano.io/api:your-group'", xb_q)
    c = c.replace("window.ENV?.XANO_API_KEY || ''", xk_q)
    c = c.replace("window.ENV?.MEMBERSTACK_PUBLIC_KEY || ''", mk_q)
    c = c.replace("window.ENV?.AIRTABLE_BASE_ID || ''", ab_q)
    c = c.replace("window.ENV?.AIRTABLE_API_KEY || ''", ak_q)
    c = c.replace("YOUR_MEMBERSTACK_PUBLIC_KEY", mk_q)
    c = c.replace("YOUR_API_KEY_HERE", xb_q)
    c = c.replace("const AIRTABLE_TOKEN='***';", ak_q)
    c = c.replace("const AIRTABLE_TOKEN=***", ak_q)
    
    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print("OK: " + fpath + " updated")
    else:
        print("INFO: " + fpath + " no changes")

def verify():
    patterns = ["YOUR_MEMBERSTACK_PUBLIC_KEY", "YOUR_API_KEY_HERE", "window.ENV?.XANO_BASE_URL",
                "window.ENV?.XANO_API_KEY", "window.ENV?.MEMBERSTACK_PUBLIC_KEY",
                "window.ENV?.AIRTABLE_BASE_ID", "window.ENV?.AIRTABLE_API_KEY",
                "const AIRTABLE_TOKEN='***';"]
    ok = True
    for fpath in FILES:
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                c = f.read()
            found = [p for p in patterns if p in c]
            if found:
                print("WARNING: " + fpath + " has: " + ", ".join(found))
                ok = False
            else:
                print("OK: " + fpath + " clean")
    return ok

def main():
    FILES = ["index.html", "match.html", "dashboard.html"]
    print("Injecting env vars...")
    print("=" * 50)
    
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        print("ERROR: Missing " + ", ".join(missing))
        sys.exit(1)
    print("OK: All env vars present")
    print()
    
    for f in FILES:
        if os.path.exists(f):
            process(f)
        else:
            print("WARNING: " + f + " not found")
    
    print()
    print("=" * 50)
    print("Verifying...")
    clean = verify()
    
    if clean:
        print()
        print("SUCCESS!")
        sys.exit(0)
    else:
        print()
        print("ERROR: Some placeholders remain")
        sys.exit(1)

if __name__ == "__main__":
    main()