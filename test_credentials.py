#!/usr/bin/env python3
"""Test script to verify Adzuna credentials are loaded correctly."""

from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file
backend_dir = Path(__file__).parent / "Backend"
env_file = backend_dir / ".env"

print(f"[TEST] Looking for .env at: {env_file}")
print(f"[TEST] .env exists: {env_file.exists()}")

if env_file.exists():
    load_dotenv(dotenv_path=str(env_file), override=True)
    
    app_id = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")
    
    print(f"\n[CREDENTIALS]")
    print(f"  APP_ID exists: {bool(app_id)}")
    print(f"  APP_ID length: {len(app_id) if app_id else 0}")
    print(f"  APP_ID first 10: {app_id[:10] if app_id else 'NONE'}")
    print(f"\n  API_KEY exists: {bool(api_key)}")
    print(f"  API_KEY length: {len(api_key) if api_key else 0}")
    print(f"  API_KEY first 10: {api_key[:10] if api_key else 'NONE'}")
    
    if app_id and api_key:
        print(f"\n[SUCCESS] Both credentials loaded successfully")
    else:
        print(f"\n[ERROR] Missing credentials:")
        if not app_id:
            print(f"  - ADZUNA_APP_ID is missing")
        if not api_key:
            print(f"  - ADZUNA_API_KEY is missing")
        
        # Show .env file contents (masked)
        print(f"\n[DEBUG] .env file contents:")
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, val = line.split('=', 1) if '=' in line else (line, '')
                    masked = val[:5] + '*' * (len(val) - 5) if len(val) > 5 else val
                    print(f"  {key}={masked}")
else:
    print(f"\n[ERROR] .env file not found at {env_file}")
    print(f"[ERROR] Current directory: {Path.cwd()}")
