"""
Test script for the improved rule-based career guidance chatbot service.

Demonstrates all features:
- Greeting detection
- Gratitude detection
- Role detection with multiple keywords
- Structured career guidance
- Unclear query handling
"""

import sys
from pathlib import Path

# Add Backend to path
sys.path.insert(0, str(Path(__file__).parent / "Backend"))

from services.career_chatbot_service import get_career_guidance, CareerChatbotService


def test_chatbot():
    """Test all features of the career chatbot."""
    
    print("=" * 80)
    print("🤖 Career Guidance Chatbot - Feature Test")
    print("=" * 80)
    
    test_cases = [
        # Greetings
        ("Hi there!", "Greeting - should respond politely"),
        ("Hello", "Greeting - should respond politely"),
        ("Good morning!", "Greeting - should respond politely"),
        
        # Gratitude
        ("Thanks for the help!", "Gratitude - should respond courteously"),
        ("Thank you so much!", "Gratitude - should respond courteously"),
        
        # Data Scientist Role
        ("How do I become a data scientist?", "Data Science - should show detailed roadmap"),
        ("I want to learn data science", "Data Science - should show detailed roadmap"),
        ("What skills do I need for data modeling?", "Data Science - keyword variation"),
        
        # AI/ML Engineer Role
        ("I'm interested in AI and machine learning", "AI/ML - should show AI/ML roadmap"),
        ("How to become an ML engineer?", "AI/ML - alternative keyword"),
        ("I want to learn deep learning and neural networks", "AI/ML - multiple keywords"),
        
        # Backend Developer Role
        ("Tell me about backend development", "Backend - should show backend roadmap"),
        ("I want to build APIs and microservices", "Backend - keyword variation"),
        ("How to become a Django developer?", "Backend - framework keyword"),
        
        # Frontend Developer Role
        ("I'm interested in React development", "Frontend - should show frontend roadmap"),
        ("How do I learn web development?", "Frontend - general web keyword"),
        ("Tell me about UI development", "Frontend - UI keyword"),
        
        # Full Stack Developer Role
        ("What's the path for full stack development?", "Full Stack - should show full stack roadmap"),
        ("I want to learn both frontend and backend", "Full Stack - explicit mention"),
        
        # Cloud Engineer Role
        ("How to become a cloud engineer?", "Cloud - should show cloud roadmap"),
        ("I'm interested in AWS and DevOps", "Cloud - keyword variation"),
        ("Tell me about Kubernetes and containerization", "Cloud - container keyword"),
        
        # Data Analyst Role
        ("I want to learn data analytics", "Data Analyst - should show analyst roadmap"),
        ("How to become a BI analyst?", "Data Analyst - BI keyword"),
        ("Tell me about Tableau and Power BI", "Data Analyst - tool keyword"),
        
        # Cyber Security Role
        ("How do I get into cybersecurity?", "Security - should show security roadmap"),
        ("I'm interested in penetration testing", "Security - penetration keyword"),
        ("Tell me about network security", "Security - network keyword"),
        
        # Unclear queries - should ask for clarification
        ("What should I do?", "Unclear - should ask for clarification"),
        ("Help me", "Too vague - should ask for clarification"),
        
        # Generic tech career
        ("Tell me about technology careers", "Generic - should show tech career overview"),
        ("What are the different IT roles?", "Generic - should suggest specific roles"),
    ]
    
    for query, description in test_cases:
        print(f"\n{'─' * 80}")
        print(f"📝 Test: {description}")
        print(f"❓ Query: {query}")
        print(f"{'─' * 80}")
        
        response = get_career_guidance(query)
        
        # Truncate long responses for readability in test output
        if len(response) > 500:
            print(response[:500] + "\n... [truncated for display]")
        else:
            print(response)
    
    print(f"\n{'=' * 80}")
    print("✅ All tests completed!")
    print("=" * 80)


def test_normalization():
    """Test input normalization."""
    print("\n" + "=" * 80)
    print("🔧 Input Normalization Test")
    print("=" * 80)
    
    service = CareerChatbotService()
    
    test_inputs = [
        "Hello, How R U???",
        "  I Want TO Learn  Python!!!  ",
        "What's the BEST way to become AI/ML Engineer???",
        "!!!###Machine Learning###!!!",
    ]
    
    for test_input in test_inputs:
        normalized = service._normalize_input(test_input)
        print(f"\nOriginal:   '{test_input}'")
        print(f"Normalized: '{normalized}'")


def test_role_detection():
    """Test role detection accuracy."""
    print("\n" + "=" * 80)
    print("🎯 Role Detection Test")
    print("=" * 80)
    
    service = CareerChatbotService()
    
    test_queries = [
        "I love Python, machine learning, and TensorFlow",
        "Building REST APIs with Django",
        "React and JavaScript frontend work",
        "AWS, Docker, and Kubernetes infrastructure",
        "SQL queries and data visualization with Tableau",
        "Ethical hacking and penetration testing",
    ]
    
    for query in test_queries:
        normalized = service._normalize_input(query)
        detected_role = service._detect_role(normalized)
        print(f"\nQuery:          '{query}'")
        print(f"Detected Role:  {detected_role if detected_role else 'No role detected'}")


def test_guardrails():
    """Test guardrails against empty/invalid inputs."""
    print("\n" + "=" * 80)
    print("🛡️ Input Validation & Guardrails Test")
    print("=" * 80)
    
    test_cases = [
        ("", "Empty string"),
        ("   ", "Only whitespace"),
        ("!!!", "Only punctuation"),
        ("...", "Only dots"),
    ]
    
    for query, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Input: '{query}'")
        response = get_career_guidance(query)
        print(f"Response: {response}")


if __name__ == "__main__":
    # Run all tests
    test_normalization()
    test_role_detection()
    test_guardrails()
    test_chatbot()
