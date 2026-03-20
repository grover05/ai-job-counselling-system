#!/usr/bin/env python
"""Quick test to check if Adzuna API is returning real jobs"""

import os
import sys
from pathlib import Path

# Navigate to backend directory
backend_dir = Path(__file__).parent / "Backend"
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(".env")

print("="*80)
print("ADZUNA API REAL JOBS TEST")
print("="*80)
print()

# Check credentials
print("Credential Status:")
print(f"  ADZUNA_APP_ID: {os.getenv('ADZUNA_APP_ID', 'NOT SET')}")
print(f"  ADZUNA_API_KEY: {os.getenv('ADZUNA_API_KEY', 'NOT SET')}")
print()

from services.adzuna_client import AdzunaClient

client = AdzunaClient()
print()

# Test 1: Python jobs in India
print("TEST 1: Python jobs in India")
print("-" * 80)
try:
    jobs = client.fetch_jobs("Python", location="India", limit=3)
    print(f"✅ Found {len(jobs)} jobs\n")
    for i, job in enumerate(jobs, 1):
        print(f"Job {i}:")
        print(f"  Title: {job.get('title')}")
        print(f"  Company: {job.get('company')}")
        print(f"  Location: {job.get('location')}")
        print(f"  Job ID: {job.get('job_id')}")
        print()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("TEST 2: Java Developer jobs in UK")
print("-" * 80)
try:
    jobs = client.fetch_jobs("Java Developer", location="UK", limit=2)
    print(f"✅ Found {len(jobs)} jobs\n")
    for i, job in enumerate(jobs, 1):
        print(f"Job {i}:")
        print(f"  Title: {job.get('title')}")
        print(f"  Company: {job.get('company')}")
        print(f"  Location: {job.get('location')}")
        print()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("="*80)
print("TEST COMPLETE")
print("="*80)
