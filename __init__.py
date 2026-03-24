"""
ML Module for AI Job Counselling System

This package provides machine learning utilities for:
- Text preprocessing and cleaning
- Skill extraction from resumes
- Text similarity and matching
- Job-resume matching and ranking

All modules are standalone and don't require external ML libraries like scikit-learn,
making them lightweight and easy to integrate with FastAPI backend.

Usage:
    from ml import clean_text, extract_skills, compute_similarity
    
    resume = "I have Python and Django experience"
    cleaned = clean_text(resume)
    skills = extract_skills(cleaned)
    similarity = compute_similarity(resume, job_description)
"""

from ml.text_cleaner import (
    clean_text,
    normalize_whitespace,
    remove_punctuation,
    expand_contractions,
    tokenize_text,
    clean_resume_text,
)

from ml.skill_extractor import (
    extract_skills,
    SkillExtractor,
)

from ml.similarity import (
    compute_similarity,
    match_skills,
    SimilarityMatcher,
)

__version__ = "1.0.0"
__author__ = "AI Job Counselling Team"

__all__ = [
    # Text Cleaning Functions
    "clean_text",
    "normalize_whitespace",
    "remove_punctuation",
    "expand_contractions",
    "tokenize_text",
    "clean_resume_text",
    
    # Skill Extraction
    "extract_skills",
    "SkillExtractor",
    
    # Similarity & Matching
    "compute_similarity",
    "match_skills",
    "SimilarityMatcher",
]
