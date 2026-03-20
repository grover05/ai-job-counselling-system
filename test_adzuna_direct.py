#!/usr/bin/env python
"""Test to see if removing 'where' parameter helps"""

import os
import sys
import requests
from pathlib import Path

# Navigate to backend directory
backend_dir = Path(__file__).parent / "Backend"
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(".env")

# Load credentials
app_id = os.getenv("ADZUNA_APP_ID")
api_key = os.getenv("ADZUNA_API_KEY")

print("="*80)
print("ADZUNA API DIRECT TEST - WITHOUT 'where' PARAMETER")
print("="*80)
print()

BASE_URL = "https://api.adzuna.com/v1/api/jobs"

# Test 1: WITHOUT where parameter
print("TEST 1: Request WITHOUT 'where' parameter")
print("-" * 80)
url = f"{BASE_URL}/in/search/1"
params = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python",
    "results_per_page": 30,
    "sort_by": "date",
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS! Found {len(data.get('results', []))} jobs")
        if data.get('results'):
            job = data['results'][0]
            print(f"\nFirst job:")
            print(f"  Title: {job.get('title')}")
            print(f"  Company: {job.get('company', {}).get('display_name')}")
            print(f"  Location: {job.get('location', {}).get('display_name')}")
    else:
        print(f"❌ Error response: {response.text[:300]}")
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "="*80)
print("TEST 2: Request WITH 'where=India' parameter (original)")
print("-" * 80)
url = f"{BASE_URL}/in/search/1"
params = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python",
    "results_per_page": 30,
    "sort_by": "date",
    "where": "India",  # THIS might be the problem
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS! Found {len(data.get('results', []))} jobs")
    else:
        print(f"❌ Error response: {response.text[:300]}")
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "="*80)
print("TEST 3: Request WITH location parameter in URL")
print("-" * 80)
# Adzuna might expect location in a different format
# Let's try just the country code without additional location
url = f"{BASE_URL}/in/search/1"
params = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python developer",
    "results_per_page": 10,
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"URL: {response.request.url}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS! Found {len(data.get('results', []))} jobs")
        if data.get('results'):
            for i, job in enumerate(data['results'][:3], 1):
                print(f"\nJob {i}:")
                print(f"  Title: {job.get('title')}")
                print(f"  Company: {job.get('company', {}).get('display_name')}")
                print(f"  Location: {job.get('location', {}).get('display_name')}")
    else:
        print(f"❌ Error ({response.status_code})")
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "="*80)
