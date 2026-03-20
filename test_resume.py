import requests
import json

resume_path = r'c:\Users\SAMBHAV SHARMA\OneDrive\Desktop\resume folder\1.pdf'

print(f'Testing resume upload: {resume_path}')
print('-' * 50)

try:
    with open(resume_path, 'rb') as f:
        files = {'file': (resume_path.split('\\')[-1], f, 'application/pdf')}
        response = requests.post('http://127.0.0.1:8000/api/resume/upload', files=files, timeout=30)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Upload successful")
        print(f"Status: {data.get('status')}")
        print(f"Skills extracted: {len(data.get('skills', []))}")
        resume_text = data.get('resume_text', '')
        print(f"Resume text length: {len(resume_text)} chars")
        print(f"Resume text preview:\n{resume_text[:500]}\n")
        if data.get('skills'):
            print(f"Skills: {', '.join(data.get('skills', []))}")
            
            # Now test job matching with these skills
            print('\n' + '-' * 50)
            print('Testing job matching with extracted skills...')
            
            job_payload = {
                'skills': data.get('skills', []),
                'location': '',
                'limit': 5
            }
            
            job_response = requests.post(
                'http://127.0.0.1:8000/api/jobs/match',
                json=job_payload,
                timeout=30
            )
            
            if job_response.status_code == 200:
                job_data = job_response.json()
                print(f"✓ Jobs matching successful")
                print(f"Total matches: {job_data.get('total_matches', 0)}")
                print(f"Matched jobs: {len(job_data.get('matched_jobs', []))}")
                
                if job_data.get('matched_jobs'):
                    print("\nTop matched jobs:")
                    for i, job in enumerate(job_data['matched_jobs'][:3], 1):
                        print(f"  {i}. {job.get('title')} at {job.get('company')} (Match: {job.get('match_score'):.2f})")
            else:
                print(f"✗ Job matching failed: {job_response.status_code}")
                print(job_response.text)
        else:
            print("✗ No skills extracted")
    else:
        print(f"✗ Upload failed: {response.status_code}")
        print(response.text)
        
except FileNotFoundError:
    print(f"✗ Resume file not found: {resume_path}")
except Exception as e:
    print(f"✗ Error: {str(e)}")
