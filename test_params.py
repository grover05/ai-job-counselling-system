#!/usr/bin/env python
"""Identify the exact parameter causing the 400 error"""

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

print("="*80)
print("TESTING DIFFERENT PARAMETER COMBINATIONS")
print("="*80)
print()

# Test from adzuna_client.py that was failing
params_failing = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python",
    "results_per_page": 30,
    "sort_by": "date",
    "sort_direction": "desc",  # This might be the culprit
    "where": "India",
}

print("TEST 1: All parameters from failing request")
print("-" * 80)
url = f"{BASE_URL}/in/search/3"
print(f"URL: {url}")
print(f"Params: {params_failing}")
try:
    response = requests.get(url, params=params_failing, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"❌ FAILED with status {response.status_code}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*80)
print("TEST 2: WITHOUT sort_direction parameter")
print("-" * 80)
params_no_sort_dir = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python",
    "results_per_page": 30,
    "sort_by": "date",
    "where": "India",
}
try:
    response = requests.get(url, params=params_no_sort_dir, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS! Found {len(data.get('results', []))} jobs")
    else:
        print(f"❌ FAILED with status {response.status_code}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*80)
print("TEST 3: WITHOUT sort_direction, with sort_direction=asc")
print("-" * 80)
params_asc = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python",
    "results_per_page": 30,
    "sort_by": "date",
    "sort_direction": "asc",
    "where": "India",
}
try:
    response = requests.get(url, params=params_asc, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS with asc! Found {len(data.get('results', []))} jobs")
    else:
        print(f"❌ FAILED with status {response.status_code}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*80)
print("TEST 4: Check if it's the 'where' parameter")
print("-" * 80)
params_where_test = {
    "app_id": app_id,
    "app_key": api_key,
    "what": "Python",
    "results_per_page": 30,
    "sort_by": "date",
    "sort_direction": "desc",
}
try:
    response = requests.get(url, params=params_where_test, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS without 'where'! Found {len(data.get('results', []))} jobs")
    else:
        print(f"❌ FAILED with status {response.status_code}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*80)
print("TEST 5: Check if it's random page number causing issues")
print("-" * 80)
# Try page 5
url_page5 = f"{BASE_URL}/in/search/5"
try:
    response = requests.get(url_page5, params=params_failing, timeout=10)
    print(f"Status: {response.status_code} (page 5)")
    print(f"URL: {response.request.url}")
except Exception as e:
    print(f"Exception: {e}")

# Try page 1
url_page1 = f"{BASE_URL}/in/search/1"
try:
    response = requests.get(url_page1, params=params_failing, timeout=10)
    print(f"Status: {response.status_code} (page 1)")
except Exception as e:
    print(f"Exception: {e}")
