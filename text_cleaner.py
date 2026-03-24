"""
Text cleaning module for preprocessing resume and job description text.

Provides utilities for normalizing and cleaning text data before processing
with NLP models or skill extraction algorithms.
"""

import re
import string
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing noise and standardizing format.
    
    This function performs the following operations:
    1. Convert to lowercase
    2. Remove extra whitespace and newlines
    3. Remove punctuation and special characters (except hyphens and spaces)
    4. Normalize multiple spaces to single space
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned and normalized text
        
    Example:
        >>> clean_text("  Hello, World!  How are YOU?  ")
        "hello world how are you"
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Replace newlines and tabs with spaces
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    
    # Step 3: Remove punctuation and special characters (keep hyphens for compound words)
    # Keep letters, numbers, spaces, and hyphens
    text = re.sub(r'[^a-z0-9\s\-]', '', text)
    
    # Step 4: Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Step 5: Strip leading and trailing whitespace
    text = text.strip()
    
    return text


def remove_punctuation(text: str) -> str:
    """
    Remove all punctuation from text.
    
    Args:
        text: Input text
        
    Returns:
        Text without punctuation
        
    Example:
        >>> remove_punctuation("Hello, World!")
        "Hello World"
    """
    if not text:
        return ""
    
    return text.translate(str.maketrans('', '', string.punctuation))


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace by replacing multiple spaces with single space
    and removing leading/trailing whitespace.
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized whitespace
        
    Example:
        >>> normalize_whitespace("Hello    World  ")
        "Hello World"
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Replace multiple whitespace characters with single space
    text = re.sub(r'\s+', ' ', text)
    
    return text


def remove_extra_characters(text: str, keep_chars: Optional[str] = None) -> str:
    """
    Remove special characters while optionally keeping specified characters.
    
    Args:
        text: Input text
        keep_chars: Additional characters to keep (e.g., "+-/." for keeping math symbols)
        
    Returns:
        Text with special characters removed
        
    Example:
        >>> remove_extra_characters("Price: $99.99", keep_chars=".")
        "Price: $9999"
    """
    if not text:
        return ""
    
    # Define what to keep: letters, numbers, spaces, and hyphens
    pattern = r'[^a-zA-Z0-9\s\-'
    
    # Add custom characters to keep if provided
    if keep_chars:
        # Escape special regex characters in keep_chars
        keep_chars_escaped = re.escape(keep_chars)
        pattern = r'[^a-zA-Z0-9\s\-' + keep_chars_escaped
    
    pattern += ']'
    
    return re.sub(pattern, '', text)


def expand_contractions(text: str) -> str:
    """
    Expand common English contractions.
    
    Args:
        text: Input text with contractions
        
    Returns:
        Text with contractions expanded
        
    Example:
        >>> expand_contractions("don't can't we'll")
        "do not can not we will"
    """
    if not text:
        return ""
    
    # Common contractions dictionary
    contractions_dict = {
        r"\bdon't\b": "do not",
        r"\bcan't\b": "can not",
        r"\bwon't\b": "will not",
        r"\bshouldn't\b": "should not",
        r"\bwe'll\b": "we will",
        r"\bi've\b": "i have",
        r"\byou've\b": "you have",
        r"\bthey've\b": "they have",
        r"\bwe've\b": "we have",
        r"\bi'm\b": "i am",
        r"\byou're\b": "you are",
        r"\bhe's\b": "he is",
        r"\bshe's\b": "she is",
        r"\bit's\b": "it is",
        r"\bthat's\b": "that is",
        r"\bthere's\b": "there is",
        r"\bi'll\b": "i will",
        r"\byou'll\b": "you will",
        r"\bhe'll\b": "he will",
        r"\bshe'll\b": "she will",
        r"\bit'll\b": "it will",
    }
    
    for contraction, expansion in contractions_dict.items():
        text = re.sub(contraction, expansion, text, flags=re.IGNORECASE)
    
    return text


def remove_numbers(text: str) -> str:
    """
    Remove all numbers from text.
    
    Args:
        text: Input text
        
    Returns:
        Text without numbers
        
    Example:
        >>> remove_numbers("Python 3.9 and Java 11")
        "Python  and Java "
    """
    if not text:
        return ""
    
    return re.sub(r'\d+', '', text)


def clean_resume_text(text: str) -> str:
    """
    Specialized cleaning for resume text.
    
    This applies multiple cleaning steps optimized for resume data:
    1. Clean basic text
    2. Expand contractions
    3. Normalize whitespace
    
    Args:
        text: Raw resume text
        
    Returns:
        Cleaned resume text
        
    Example:
        >>> clean_resume_text("  John's Resume\\n\\nSkills: Python, Machine Learning")
        "johns resume skills python machine learning"
    """
    if not text:
        return ""
    
    # Apply basic cleaning
    text = clean_text(text)
    
    # Expand contractions before removing punctuation
    text = expand_contractions(text)
    
    # Final whitespace normalization
    text = normalize_whitespace(text)
    
    return text


def tokenize_text(text: str, remove_stopwords: bool = False) -> list:
    """
    Split text into tokens (words).
    
    Args:
        text: Input text to tokenize
        remove_stopwords: If True, remove common English stopwords
        
    Returns:
        List of tokens (words)
        
    Example:
        >>> tokenize_text("Hello world from Python")
        ["hello", "world", "from", "python"]
    """
    if not text:
        return []
    
    # Clean text first
    text = clean_text(text)
    
    # Split into tokens
    tokens = text.split()
    
    # Optionally remove stopwords
    if remove_stopwords:
        stopwords = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'please', 'be', 'is', 'are', 'am', 'was', 'were', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
            'who', 'when', 'where', 'why', 'how'
        }
        tokens = [token for token in tokens if token not in stopwords]
    
    return tokens


# Example usage and testing
if __name__ == "__main__":
    # Test the cleaning functions
    test_text = """
    Senior Software Engineer with 5+ years of experience.
    Skills: Python, JavaScript, Machine Learning & AI.
    Email: john@example.com | Phone: (123) 456-7890
    """
    
    print("Original text:")
    print(test_text)
    print("\n" + "="*50 + "\n")
    
    print("Clean text:")
    print(clean_text(test_text))
    print("\n" + "="*50 + "\n")
    
    print("Clean resume text:")
    print(clean_resume_text(test_text))
    print("\n" + "="*50 + "\n")
    
    print("Tokenized (with stopwords):")
    print(tokenize_text(test_text, remove_stopwords=False))
    print("\n" + "="*50 + "\n")
    
    print("Tokenized (without stopwords):")
    print(tokenize_text(test_text, remove_stopwords=True))
