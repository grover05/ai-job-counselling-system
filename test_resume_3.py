import requests

resume_path = r'c:\Users\SAMBHAV SHARMA\OneDrive\Desktop\resume folder\3.pdf'

print(f'Testing with resume: {resume_path}')
print('-' * 60)

with open(resume_path, 'rb') as f:
    files = {'file': (resume_path.split('\\')[-1], f, 'application/pdf')}
    response = requests.post('http://127.0.0.1:8000/api/resume/upload', files=files, timeout=30)

if response.status_code == 200:
    data = response.json()
    print(f'✓ Upload successful')
    print(f'Skills extracted: {len(data.get("skills", []))}')
    
    skills = data.get('skills', [])
    if skills:
        print(f'Skills: {", ".join(skills)}')
        print()
        
        # Now test job matching
        print('-' * 60)
        print('Testing job matching with extracted skills...')
        
        job_payload = {
            'skills': skills,
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
            print(f'✓ Jobs matching successful')
            print(f'Total matches: {job_data.get("total_matches", 0)}')
            
            if job_data.get('matched_jobs'):
                print('\nMatched jobs:')
                for i, job in enumerate(job_data['matched_jobs'][:5], 1):
                    print(f"  {i}. {job.get('title')} at {job.get('company')}")
                    print(f"     Location: {job.get('location')}")
                    print(f"     Match Score: {job.get('match_score'):.2%}")
                    print()
        else:
            print(f'Error: {job_response.status_code}')
    else:
        print('No skills found in resume text')
        resume_text = data.get('resume_text', '')
        print(f'Resume text length: {len(resume_text)} chars')
        print(f'Resume text preview:\n{resume_text[:500]}')
else:
    print(f'Error: {response.status_code}')
    print(response.text)
