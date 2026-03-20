#!/usr/bin/env python
"""Test the API endpoint"""

import requests
import json

url = "http://localhost:8000/api/jobs/match"
payload = {
    "skills": ["python", "data analysis"],
    "limit": 5
}

print("Testing API endpoint: POST http://localhost:8000/api/jobs/match")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print()
    
    data = response.json()
    print(f"Response:")
    print(json.dumps(data, indent=2))
    
    if data.get("matched_jobs"):
        print(f"\n✓ SUCCESS: Found {len(data['matched_jobs'])} jobs")
        for i, job in enumerate(data["matched_jobs"][:2], 1):
            print(f"\nJob {i}:")
            print(f"  Title: {job.get('title')}")
            print(f"  Company: {job.get('company')}")
            print(f"  Has description: {'description' in job and len(job['description']) > 0}")
            print(f"  Has URL: {'url' in job and len(job['url']) > 0}")
            print(f"  Match Score: {job.get('match_score', 0)}")
    else:
        print("\n✗ FAILED: No jobs returned")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
