"""
Test script for the chatbot API integration with improved CareerChatbotService.
"""

import sys
from pathlib import Path

# Add Backend to path
sys.path.insert(0, str(Path(__file__).parent / "Backend"))

from services.career_chatbot_service import get_career_guidance


def test_api_scenarios():
    """Test the chatbot with various scenarios."""
    
    print("=" * 80)
    print("🤖 Career Guidance Chatbot - API Integration Test")
    print("=" * 80)
    
    test_scenarios = [
        # Career guidance queries
        {
            "query": "How do I become a data scientist?",
            "description": "Data Scientist guidance"
        },
        {
            "query": "I'm interested in machine learning and AI engineering",
            "description": "AI/ML Engineer guidance"
        },
        {
            "query": "Tell me about backend and API development",
            "description": "Backend Developer guidance"
        },
        {
            "query": "I want to build web applications with React",
            "description": "Frontend Developer guidance"
        },
        {
            "query": "How do I learn cloud engineering and AWS?",
            "description": "Cloud Engineer guidance"
        },
        # Greetings
        {
            "query": "Hello! Can you help me?",
            "description": "Greeting with request"
        },
        # Gratitude
        {
            "query": "Thanks for the help!",
            "description": "Gratitude expression"
        },
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'─' * 80}")
        print(f"Test {i}: {scenario['description']}")
        print(f"Query: {scenario['query']}")
        print(f"{'─' * 80}")
        
        response = get_career_guidance(scenario['query'])
        
        # Show first 400 chars of response
        if len(response) > 400:
            print(response[:400] + "\n... [response continues]")
        else:
            print(response)
    
    print(f"\n{'=' * 80}")
    print("✅ API Integration Test Completed Successfully!")
    print("=" * 80)


if __name__ == "__main__":
    test_api_scenarios()
