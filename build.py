#!/usr/bin/env python3
# build.py - Generate config.js with environment variables at build time.

import os
import sys

REQUIRED_VARS = [
    "XANO_BASE_URL",
    "XANO_API_KEY",
    "MEMBERSTACK_PUBLIC_KEY",
    "AIRTABLE_BASE_ID",
    "AIRTABLE_API_KEY"
]

def check_env():
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        print("ERROR: Missing " + ", ".join(missing))
        sys.exit(1)
    print("OK: All env vars present")

def generate_config_js():
    xb = os.getenv("XANO_BASE_URL", "")
    xk = os.getenv("XANO_API_KEY", "")
    mk = os.getenv("MEMBERSTACK_PUBLIC_KEY", "")
    ab = os.getenv("AIRTABLE_BASE_ID", "")
    ak = os.getenv("AIRTABLE_API_KEY", "")

    # Escape values for JavaScript (handle quotes, backslashes, newlines)
    def js_escape(s):
        return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")

    xb = js_escape(xb)
    xk = js_escape(xk)
    mk = js_escape(mk)
    ab = js_escape(ab)
    ak = js_escape(ak)

    config = f"""// Auto-generated at build time - DO NOT EDIT MANUALLY
// Config values injected from environment variables
window.APP_CONFIG = {{
  XANO_BASE_URL: '{xb}',
  XANO_API_KEY: '{xk}',
  MEMBERSTACK_PUBLIC_KEY: '{mk}',
  AIRTABLE_BASE_ID: '{ab}',
  AIRTABLE_API_KEY: '{ak}'
}};
"""
    with open("config.js", "w", encoding="utf-8") as f:
        f.write(config)
    print("OK: config.js generated")

def verify_config():
    if not os.path.exists("config.js"):
        print("ERROR: config.js not found")
        return False
    with open("config.js", "r", encoding="utf-8") as f:
        content = f.read()
    # Check that no placeholder patterns remain
    patterns = ["your-workspace.xano.io/api:your-group", "YOUR_", "window.ENV?"]
    found = [p for p in patterns if p in content]
    if found:
        print("WARNING: config.js has placeholders: " + ", ".join(found))
        return False
    print("OK: config.js clean")
    return True

def main():
    print("Generating config.js...")
    print("=" * 50)

    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        print("ERROR: Missing " + ", ".join(missing))
        sys.exit(1)
    print("OK: All env vars present")
    print()

    generate_config_js()

    print()
    print("=" * 50)
    print("Verifying...")
    clean = verify_config()

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