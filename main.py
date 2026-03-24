from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
# Ensure .env is loaded from the Backend directory
backend_dir = Path(__file__).parent
env_file = backend_dir / ".env"
load_dotenv(dotenv_path=str(env_file), override=True)

# Debug: Verify environment variables are loaded
print(f"[DEBUG] Loading .env file from: {env_file}")
print(f"[DEBUG] .env file exists: {env_file.exists()}")
print(f"[DEBUG] ADZUNA_APP_ID: {'[OK] Set' if os.getenv('ADZUNA_APP_ID') else '[MISSING] Not set'}")
print(f"[DEBUG] ADZUNA_API_KEY: {'[OK] Set' if os.getenv('ADZUNA_API_KEY') else '[MISSING] Not set'}")

from api import resume, jobs, chatbot


# Response Models
class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status", example="healthy")
    message: str = Field(..., description="Status message", example="AI Job Counselling System backend is running successfully")


# Initialize FastAPI app
app = FastAPI(
    title="AI Job Counselling System",
    description="An AI-powered job counselling and career guidance system with resume analysis, job matching, and AI chatbot guidance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,  # Disable ReDoc due to rendering issues
    openapi_url="/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": 1},
)

# Configure CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])


# Health check endpoint
@app.get(
    "/",
    response_model=HealthCheckResponse,
    tags=["Health"],
    summary="Health Check",
    response_description="Service status confirmation",
    status_code=200,
)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        HealthCheckResponse: Service status and message.
    """
    return HealthCheckResponse(
        status="healthy",
        message="AI Job Counselling System backend is running successfully",
    )


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
