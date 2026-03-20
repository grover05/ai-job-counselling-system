import os
from dotenv import load_dotenv
from pathlib import Path

backend_dir = Path(__file__).parent / "Backend"
env_file = backend_dir / ".env"

load_dotenv(dotenv_path=str(env_file), override=True)

app_id = os.getenv("ADZUNA_APP_ID")
api_key = os.getenv("ADZUNA_API_KEY")

print(f"APP_ID: {app_id}")
print(f"APP_ID starts with: {app_id[:5] if app_id else 'None'}")
print(f"API_KEY: {api_key}")
print(f"API_KEY starts with: {api_key[:5] if api_key else 'None'}")
