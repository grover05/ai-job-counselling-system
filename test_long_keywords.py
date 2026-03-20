#!/usr/bin/env python
"""Test with the long keyword string from the frontend"""

import os
import sys
import requests
from pathlib import Path

backend_dir = Path(__file__).parent / "Backend"
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(".env")

app_id = os.getenv("ADZUNA_APP_ID")
api_key = os.getenv("ADZUNA_API_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"

# The long keyword string from the debug output
long_keywords = "data analysis data visualization git numpy pandas power bi python sql tableau"

print("="*80)
print("TEST: Long keyword string from frontend")
print("="*80)
print()
print(f"Keywords: {long_keywords}")
print()

url = f"{BASE_URL}/in/search/1"
params = {
    "app_id": app_id,
    "app_key": api_key,
    "what": long_keywords,
    "results_per_page": 30,
    "sort_by": "date",
}

print(f"URL: {url}")
print()

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse keys: {list(data.keys())}")
        print(f"Number of results: {len(data.get('results', []))}")
        
        if "results" in data and len(data["results"]) > 0:
            print(f"\n✅ Found {len(data['results'])} jobs")
            print("\nFirst job:")
            job = data["results"][0]
            print(f"  Title: {job.get('title')}")
            print(f"  Company: {job.get('company', {}).get('display_name')}")
            print(f"  Location: {job.get('location', {}).get('display_name')}")
        else:
            print(f"\n❌ No results found!")
            print(f"\nFull response: {data}")
    else:
        print(f"❌ Error response ({response.status_code})")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("TEST 2: Try with fewer keywords (top 3)")
print("="*80)

keywords_short = " ".join(long_keywords.split()[:3])
print(f"Keywords: {keywords_short}")

params["what"] = keywords_short
try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Results: {len(data.get('results', []))}")
        if len(data.get('results', [])) > 0:
            print(f"✅ Found {len(data['results'])} jobs")
        else:
            print("❌ No results")
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")

print("="*80)
