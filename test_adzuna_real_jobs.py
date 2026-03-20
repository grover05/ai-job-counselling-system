"""
Test script to verify if Adzuna API is returning real jobs
"""

import os
import sys
from pathlib import Path

# Add Backend to path
backend_path = Path(__file__).parent / "Backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
from services.adzuna_client import AdzunaClient

# Load environment variables
env_path = backend_path / ".env"
load_dotenv(env_path)

def test_adzuna_api():
    """Test Adzuna API with various queries"""
    
    print("=" * 80)
    print("ADZUNA API REAL JOBS TEST")
    print("=" * 80)
    
    # Initialize client
    client = AdzunaClient()
    
    # Test searches
    test_cases = [
        ("Python", "India", 5),
        ("Java Developer", "India", 5),
        ("Data Science", "UK", 3),
        ("Web Developer React", "USA", 3),
    ]
    
    for keywords, location, limit in test_cases:
        print(f"\n\n{'='*80}")
        print(f"TEST: Searching for '{keywords}' in {location} (limit: {limit})")
        print('='*80)
        
        try:
            jobs = client.fetch_jobs(keywords, location=location, limit=limit)
            
            if not jobs:
                print(f"❌ NO JOBS RETURNED")
                continue
            
            print(f"✅ FOUND {len(jobs)} JOBS\n")
            
            for i, job in enumerate(jobs, 1):
                print(f"\n--- Job {i} ---")
                print(f"Title: {job.get('title', 'N/A')}")
                print(f"Company: {job.get('company', 'N/A')}")
                print(f"Location: {job.get('location', 'N/A')}")
                print(f"Job ID: {job.get('job_id', 'N/A')}")
                print(f"URL: {job.get('url', 'N/A')}")
                print(f"Posted: {job.get('posted_date', 'N/A')}")
                print(f"Salary Min: {job.get('salary_min', 'N/A')}")
                print(f"Salary Max: {job.get('salary_max', 'N/A')}")
                desc = job.get('description', 'N/A')
                if desc and len(desc) > 200:
                    print(f"Description: {desc[:200]}...")
                else:
                    print(f"Description: {desc}")
            
        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_adzuna_api()
