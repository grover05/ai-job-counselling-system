"""
Text similarity and matching module for comparing resumes with job descriptions
and calculating skill match scores.

Provides utilities for TF-IDF vectorization, cosine similarity, and Jaccard similarity
for matching job seekers with job opportunities.
"""

import re
import math
from typing import List, Dict, Tuple, Set
from collections import Counter


class SimilarityMatcher:
    """Calculate similarity between text documents and skills matching."""
    
    def __init__(self):
        """Initialize the similarity matcher."""
        self.epsilon = 1e-10  # Small value to prevent division by zero
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Split text into lowercase tokens.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of tokens (words)
        """
        if not text:
            return []
        
        # Convert to lowercase
        text = text.lower()
        
        # Split on word boundaries
        tokens = re.findall(r'\b\w+\b', text)
        
        return tokens
    
    def _calculate_tf(self, tokens: List[str]) -> Dict[str, float]:
        """
        Calculate Term Frequency (TF) for tokens.
        
        TF = (count of term) / (total number of terms)
        
        Args:
            tokens: List of tokens
            
        Returns:
            Dictionary with token -> TF score
        """
        if not tokens:
            return {}
        
        token_counts = Counter(tokens)
        total_tokens = len(tokens)
        
        tf = {}
        for token, count in token_counts.items():
            tf[token] = count / total_tokens
        
        return tf
    
    def _calculate_idf(self, documents: List[List[str]]) -> Dict[str, float]:
        """
        Calculate Inverse Document Frequency (IDF) across documents.
        
        IDF = log(total documents / documents containing term)
        
        Args:
            documents: List of token lists (documents)
            
        Returns:
            Dictionary with token -> IDF score
        """
        if not documents:
            return {}
        
        num_docs = len(documents)
        token_doc_count = Counter()
        
        # Count how many documents contain each token
        for doc in documents:
            unique_tokens = set(doc)
            token_doc_count.update(unique_tokens)
        
        idf = {}
        for token, doc_count in token_doc_count.items():
            # Add 1 to avoid division by zero
            idf[token] = math.log(num_docs / (1 + doc_count))
        
        return idf
    
    def compute_tfidf_vector(self, text: str, idf_dict: Dict[str, float] = None) -> Dict[str, float]:
        """
        Compute TF-IDF vector for a single document.
        
        TF-IDF = TF * IDF
        
        Args:
            text: Input text
            idf_dict: Pre-computed IDF dictionary (optional)
            
        Returns:
            Dictionary with token -> TF-IDF score
        """
        if not text or not isinstance(text, str):
            return {}
        
        tokens = self.tokenize(text)
        if not tokens:
            return {}
        
        # Calculate TF
        tf = self._calculate_tf(tokens)
        
        # Use provided IDF or calculate simple IDF
        if idf_dict is None:
            # Simple IDF: log of unique tokens
            idf_dict = {}
            unique_tokens = set(tokens)
            for token in unique_tokens:
                idf_dict[token] = math.log(1 + len(unique_tokens) / (1 + tokens.count(token)))
        
        # Calculate TF-IDF
        tfidf = {}
        for token, tf_score in tf.items():
            idf_score = idf_dict.get(token, 0)
            tfidf[token] = tf_score * idf_score
        
        return tfidf
    
    def cosine_similarity_tfidf(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity using TF-IDF vectors.
        
        Cosine Similarity = (dot product) / (magnitude1 * magnitude2)
        
        Args:
            text1: First text document
            text2: Second text document
            
        Returns:
            Similarity score between 0 and 1
            
        Example:
            >>> matcher = SimilarityMatcher()
            >>> score = matcher.cosine_similarity_tfidf(
            ...     "Python and Django",
            ...     "Python Django and Flask"
            ... )
            >>> print(f"{score:.3f}")
            0.547
        """
        if not text1 or not text2:
            return 0.0
        
        # Tokenize both texts
        tokens1 = self.tokenize(text1)
        tokens2 = self.tokenize(text2)
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Get all unique tokens
        all_tokens = set(tokens1 + tokens2)
        
        # Calculate IDF from both documents combined
        combined_docs = [tokens1, tokens2]
        idf_dict = self._calculate_idf(combined_docs)
        
        # Calculate TF-IDF vectors
        tfidf1 = self.compute_tfidf_vector(text1, idf_dict)
        tfidf2 = self.compute_tfidf_vector(text2, idf_dict)
        
        # Calculate dot product
        dot_product = 0.0
        for token in all_tokens:
            dot_product += tfidf1.get(token, 0) * tfidf2.get(token, 0)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(score ** 2 for score in tfidf1.values()))
        magnitude2 = math.sqrt(sum(score ** 2 for score in tfidf2.values()))
        
        # Handle division by zero
        if magnitude1 < self.epsilon or magnitude2 < self.epsilon:
            return 0.0
        
        # Return cosine similarity
        return dot_product / (magnitude1 * magnitude2)
    
    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate Jaccard similarity between two texts.
        
        Jaccard similarity = (intersection of sets) / (union of sets)
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
            
        Example:
            >>> matcher = SimilarityMatcher()
            >>> matcher.jaccard_similarity("Hello world", "Hello there")
            0.33  # 1 common word / 3 unique words
        """
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        if not tokens1 and not tokens2:
            return 1.0
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        
        return intersection / union if union > 0 else 0.0
    
    def cosine_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts using token counts.
        
        Cosine similarity = (dot product) / (magnitude1 * magnitude2)
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
            
        Example:
            >>> matcher = SimilarityMatcher()
            >>> matcher.cosine_similarity("Python Java", "Python JavaScript")
            0.5  # 1 common token vector similarity
        """
        tokens1 = self.tokenize(text1)
        tokens2 = self.tokenize(text2)
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Create frequency vectors
        counter1 = Counter(tokens1)
        counter2 = Counter(tokens2)
        
        # Get all unique tokens
        all_tokens = set(counter1.keys()) | set(counter2.keys())
        
        # Calculate dot product
        dot_product = sum(counter1.get(token, 0) * counter2.get(token, 0) for token in all_tokens)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(count ** 2 for count in counter1.values()))
        magnitude2 = math.sqrt(sum(count ** 2 for count in counter2.values()))
        
        if magnitude1 < self.epsilon or magnitude2 < self.epsilon:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def common_tokens(self, text1: str, text2: str) -> Set[str]:
        """
        Get common tokens between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Set of common tokens
        """
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        return tokens1 & tokens2
    
    def token_overlap_ratio(self, text1: str, text2: str) -> float:
        """
        Calculate what percentage of text1's tokens are in text2.
        
        Useful for checking if job keywords are in resume.
        
        Args:
            text1: Reference text (e.g., job requirements)
            text2: Comparison text (e.g., resume)
            
        Returns:
            Overlap percentage (0 to 1)
        """
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        if not tokens1:
            return 1.0 if not tokens2 else 0.0
        
        overlap = len(tokens1 & tokens2)
        return overlap / len(tokens1)
    
    def skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """
        Calculate skill match score between resume and job.
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of required skills for job
            
        Returns:
            Match score (0 to 1)
        """
        if not job_skills:
            return 1.0
        
        if not resume_skills:
            return 0.0
        
        resume_skills_lower = set(s.lower() for s in resume_skills)
        job_skills_lower = set(s.lower() for s in job_skills)
        
        matched = len(resume_skills_lower & job_skills_lower)
        
        return matched / len(job_skills_lower)
    
    def skill_match_details(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """
        Get detailed skill matching information.
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of required skills for job
            
        Returns:
            Dictionary with matching details
            
        Example output:
            {
                'matched_skills': ['Python', 'Django'],
                'missing_skills': ['Kubernetes'],
                'extra_skills': ['React'],
                'match_percentage': 66.7
            }
        """
        resume_skills_lower = set(s.lower() for s in resume_skills)
        job_skills_lower = set(s.lower() for s in job_skills)
        
        matched = resume_skills_lower & job_skills_lower
        missing = job_skills_lower - resume_skills_lower
        extra = resume_skills_lower - job_skills_lower
        
        match_percentage = (len(matched) / len(job_skills_lower) * 100) if job_skills_lower else 0
        
        return {
            'matched_skills': sorted(list(matched)),
            'missing_skills': sorted(list(missing)),
            'extra_skills': sorted(list(extra)),
            'matched_count': len(matched),
            'required_count': len(job_skills_lower),
            'match_percentage': round(match_percentage, 1),
        }
    
    def text_similarity_score(self, text1: str, text2: str, 
                             method: str = "cosine") -> float:
        """
        Calculate combined similarity score between two texts.
        
        Args:
            text1: First text
            text2: Second text
            method: Similarity method ('cosine', 'jaccard', or 'average')
            
        Returns:
            Similarity score (0 to 1)
        """
        if method == "jaccard":
            return self.jaccard_similarity(text1, text2)
        elif method == "cosine":
            return self.cosine_similarity(text1, text2)
        elif method == "average":
            return (self.cosine_similarity(text1, text2) + 
                   self.jaccard_similarity(text1, text2)) / 2
        else:
            raise ValueError(f"Unknown similarity method: {method}")
    
    def match_resume_to_jobs(self, resume_text: str, job_descriptions: List[Dict]) -> List[Dict]:
        """
        Match a resume against multiple job descriptions.
        
        Args:
            resume_text: Resume text content
            job_descriptions: List of dicts with 'id', 'title', and 'description'
            
        Returns:
            Sorted list of matches with scores
            
        Example input:
            job_descriptions = [
                {'id': 1, 'title': 'Python Dev', 'description': '...'},
                {'id': 2, 'title': 'Java Dev', 'description': '...'},
            ]
            
        Example output:
            [
                {'job_id': 1, 'job_title': 'Python Dev', 'match_score': 0.78},
                {'job_id': 2, 'job_title': 'Java Dev', 'match_score': 0.45},
            ]
        """
        matches = []
        
        for job in job_descriptions:
            similarity = self.text_similarity_score(
                resume_text,
                job.get('description', ''),
                method='average'
            )
            
            matches.append({
                'job_id': job.get('id'),
                'job_title': job.get('title'),
                'match_score': round(similarity, 3),
            })
        
        # Sort by match score descending
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches


# Convenience functions for simple usage
def compute_similarity(resume_text: str, job_description: str) -> float:
    """
    Compute TF-IDF based cosine similarity between resume and job description.
    
    This is the main function for comparing a resume with a job description.
    Uses TF-IDF vectorization to create weighted term vectors, then computes
    cosine similarity between them.
    
    Algorithm:
    1. Tokenize both texts into words
    2. Calculate Term Frequency (TF) for each word
    3. Calculate Inverse Document Frequency (IDF) across documents
    4. Compute TF-IDF scores (TF * IDF)
    5. Calculate cosine similarity of TF-IDF vectors
    
    Args:
        resume_text: Resume content as string
        job_description: Job description as string
        
    Returns:
        Similarity score between 0.0 and 1.0
        - 0.0 = completely different
        - 0.5 = moderate match
        - 1.0 = identical
        
    Example:
        >>> resume = "Senior Python Developer with Django experience"
        >>> job = "Need Python Django backend developer"
        >>> score = compute_similarity(resume, job)
        >>> print(f"Match: {score:.2%}")
        Match: 72.5%
    """
    # Handle null or empty inputs safely
    if not resume_text or not isinstance(resume_text, str):
        resume_text = ""
    if not job_description or not isinstance(job_description, str):
        job_description = ""
    
    # If both are empty, return 0
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    
    # Create matcher and compute TF-IDF cosine similarity
    matcher = SimilarityMatcher()
    similarity = matcher.cosine_similarity_tfidf(resume_text, job_description)
    
    # Ensure result is in valid range [0, 1]
    return max(0.0, min(1.0, similarity))


def match_skills(resume_skills: List[str], job_skills: List[str]) -> Dict:
    """
    Quick function to match skills between resume and job.
    
    Args:
        resume_skills: List of resume skills
        job_skills: List of required job skills
        
    Returns:
        Dictionary with match details
    """
    matcher = SimilarityMatcher()
    return matcher.skill_match_details(resume_skills, job_skills)


# Example usage and testing
if __name__ == "__main__":
    matcher = SimilarityMatcher()
    
    # Test data
    resume = """
    Senior Software Engineer with 5+ years experience.
    Skills: Python, Django, PostgreSQL, AWS, Docker, Kubernetes.
    Expertise in building scalable backend systems and microservices.
    """
    
    job_description = """
    We are looking for a Backend Engineer.
    Required Skills: Python, FastAPI, PostgreSQL, Docker, Kubernetes.
    Should have experience with cloud platforms and microservices architecture.
    """
    
    print("="*70)
    print("SIMILARITY COMPUTATION MODULE - TF-IDF BASED COSINE SIMILARITY")
    print("="*70)
    print("\nResume:")
    print(resume)
    print("\nJob Description:")
    print(job_description)
    print("\n" + "="*70 + "\n")
    
    # Main compute_similarity function
    print("PRIMARY FUNCTION: compute_similarity()")
    print("-" * 70)
    score = compute_similarity(resume, job_description)
    print(f"TF-IDF Cosine Similarity: {score:.4f}")
    print(f"Match Percentage: {score*100:.2f}%")
    print(f"Match Level: ", end="")
    if score >= 0.75:
        print("EXCELLENT")
    elif score >= 0.5:
        print("GOOD")
    elif score >= 0.25:
        print("FAIR")
    else:
        print("POOR")
    print("\n" + "="*70 + "\n")
    
    # TF-IDF Vector visualization
    print("TF-IDF VECTOR ANALYSIS")
    print("-" * 70)
    tfidf_resume = matcher.compute_tfidf_vector(resume)
    tfidf_job = matcher.compute_tfidf_vector(job_description)
    
    print("\nTop 5 Terms in Resume (by TF-IDF):")
    top_resume = sorted(tfidf_resume.items(), key=lambda x: x[1], reverse=True)[:5]
    for term, score_val in top_resume:
        print(f"  {term:20s} : {score_val:.4f}")
    
    print("\nTop 5 Terms in Job (by TF-IDF):")
    top_job = sorted(tfidf_job.items(), key=lambda x: x[1], reverse=True)[:5]
    for term, score_val in top_job:
        print(f"  {term:20s} : {score_val:.4f}")
    
    print("\n" + "="*70 + "\n")
    
    # Other similarity methods
    print("ALTERNATIVE SIMILARITY METHODS (for comparison)")
    print("-" * 70)
    cosine_basic = matcher.cosine_similarity(resume, job_description)
    jaccard = matcher.jaccard_similarity(resume, job_description)
    
    print(f"Cosine Similarity (Token-based): {cosine_basic:.4f}")
    print(f"Jaccard Similarity:              {jaccard:.4f}")
    print(f"TF-IDF Cosine Similarity:        {score:.4f}")
    
    print("\n" + "="*70 + "\n")
    
    # Edge cases
    print("EDGE CASE HANDLING")
    print("-" * 70)
    print(f"Empty resume & job:       {compute_similarity('', ''):.4f}")
    print(f"Empty resume, valid job:  {compute_similarity('', job_description):.4f}")
    print(f"Valid resume, empty job:  {compute_similarity(resume, ''):.4f}")
    print(f"None values handled:      {compute_similarity(None, None):.4f}")
    
    print("\n" + "="*70)
