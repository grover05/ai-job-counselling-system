"""
Improved Skill Extraction Module
Identifies technical and professional skills from resume and job description text.

Features:
- Rule-based skill extraction without external NLP APIs
- Comprehensive skill database with aliases and variations
- Word boundary matching to avoid false positives
- Duplicate removal and sorting
- Organized by skill categories
"""

import re
from typing import List, Dict, Set



class SkillExtractor:
    """Extract and categorize professional skills from text using rule-based approach."""
    
    # Comprehensive skill database organized by categories
    SKILL_DATABASE = {
        "Programming Languages": {
            "python": [r"\bpython\b", r"\bpy\b"],
            "javascript": [r"\bjavascript\b", r"\bjs\b"],
            "java": [r"\bjava\b"],
            "c++": [r"\bc\+\+\b", r"\bcpp\b"],
            "csharp": [r"\bc#\b", r"\bcsharp\b"],
            "php": [r"\bphp\b"],
            "ruby": [r"\bruby\b"],
            "go": [r"\bgo\b", r"\bgolang\b"],
            "rust": [r"\brust\b"],
            "kotlin": [r"\bkotlin\b"],
            "swift": [r"\bswift\b"],
            "typescript": [r"\btypescript\b", r"\bts\b"],
            "r": [r"\br\b"],
            "matlab": [r"\bmatlab\b"],
            "scala": [r"\bscala\b"],
            "perl": [r"\bperl\b"],
        },
        
        "Web Development": {
            "react": [r"\breact\b", r"\breactjs\b"],
            "angular": [r"\bangular\b", r"\bangularjs\b"],
            "vue.js": [r"\bvue\b", r"\bvuejs\b"],
            "next.js": [r"\bnext\.js\b", r"\bnextjs\b"],
            "svelte": [r"\bsvelte\b"],
            "express": [r"\bexpress\b", r"\bexpress\.js\b"],
            "node.js": [r"\bnode\.js\b", r"\bnodejs\b"],
            "html": [r"\bhtml\b", r"\bhtml5\b"],
            "css": [r"\bcss\b", r"\bcss3\b"],
            "sass": [r"\bsass\b", r"\bscss\b"],
            "webpack": [r"\bwebpack\b"],
            "vite": [r"\bvite\b"],
            "bootstrap": [r"\bbootstrap\b"],
            "tailwind": [r"\btailwind\b"],
            "rest": [r"\brest\b", r"\brestful\b"],
            "graphql": [r"\bgraphql\b"],
        },
        
        "Backend Frameworks": {
            "django": [r"\bdjango\b"],
            "flask": [r"\bflask\b"],
            "fastapi": [r"\bfastapi\b"],
            "spring": [r"\bspring\b", r"\bspring boot\b"],
            "laravel": [r"\blaravel\b"],
            "asp.net": [r"\basp\.net\b"],
            "ruby on rails": [r"\brails\b", r"\bruby on rails\b"],
            "django rest framework": [r"\bdjango rest framework\b"],
            "nestjs": [r"\bnestjs\b", r"\bnest\.js\b"],
        },
        
        "Databases": {
            "sql": [r"\bsql\b"],
            "mysql": [r"\bmysql\b"],
            "postgresql": [r"\bpostgresql\b", r"\bpostgres\b"],
            "mongodb": [r"\bmongodb\b", r"\bmongo\b"],
            "oracle": [r"\boracle\b"],
            "sqlite": [r"\bsqlite\b"],
            "redis": [r"\bredis\b"],
            "cassandra": [r"\bcassandra\b"],
            "elasticsearch": [r"\belasticsearch\b"],
            "dynamodb": [r"\bdynamodb\b"],
            "firebase": [r"\bfirebase\b"],
        },
        
        "Data Science & ML": {
            "machine learning": [r"\bmachine learning\b", r"\bml\b"],
            "deep learning": [r"\bdeep learning\b", r"\bdl\b"],
            "numpy": [r"\bnumpy\b"],
            "pandas": [r"\bpandas\b"],
            "scikit-learn": [r"\bscikit-learn\b", r"\bscikit learn\b"],
            "tensorflow": [r"\btensorflow\b"],
            "pytorch": [r"\bpytorch\b"],
            "keras": [r"\bkeras\b"],
            "nlp": [r"\bnlp\b", r"\bnatural language processing\b"],
            "computer vision": [r"\bcomputer vision\b", r"\bcv\b"],
            "data analysis": [r"\bdata analysis\b"],
            "data visualization": [r"\bdata visualization\b"],
            "matplotlib": [r"\bmatplotlib\b"],
            "seaborn": [r"\bseaborn\b"],
            "jupyter": [r"\bjupyter\b"],
            "anaconda": [r"\banaconda\b"],
            "tableau": [r"\btableau\b"],
            "power bi": [r"\bpower bi\b", r"\bpowerbi\b"],
        },
        
        "Cloud & DevOps": {
            "aws": [r"\baws\b", r"\bamazon web services\b"],
            "azure": [r"\bazure\b"],
            "gcp": [r"\bgcp\b", r"\bgoogle cloud\b"],
            "docker": [r"\bdocker\b"],
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "jenkins": [r"\bjenkins\b"],
            "gitlab ci": [r"\bgitlab ci\b"],
            "github actions": [r"\bgithub actions\b"],
            "terraform": [r"\bterraform\b"],
            "ansible": [r"\bansible\b"],
            "prometheus": [r"\bprometheus\b"],
            "grafana": [r"\bgrafana\b"],
            "ci/cd": [r"\bci/cd\b", r"\bcicd\b"],
            "devops": [r"\bdevops\b"],
        },
        
        "Development Tools": {
            "git": [r"\bgit\b"],
            "github": [r"\bgithub\b"],
            "gitlab": [r"\bgitlab\b"],
            "bitbucket": [r"\bbitbucket\b"],
            "jira": [r"\bjira\b"],
            "confluence": [r"\bconfluence\b"],
            "slack": [r"\bslack\b"],
            "postman": [r"\bpostman\b"],
            "vim": [r"\bvim\b"],
            "vs code": [r"\bvs code\b", r"\bvisual studio code\b"],
            "intellij": [r"\bintellij\b"],
            "vscode": [r"\bvscode\b"],
            "sublime": [r"\bsublime\b"],
            "npm": [r"\bnpm\b"],
            "pip": [r"\bpip\b"],
            "maven": [r"\bmaven\b"],
            "gradle": [r"\bgradle\b"],
        },
        
        "Testing & QA": {
            "junit": [r"\bjunit\b"],
            "pytest": [r"\bpytest\b"],
            "mocha": [r"\bmocha\b"],
            "jest": [r"\bjest\b"],
            "selenium": [r"\bselenium\b"],
            "cypress": [r"\bcypress\b"],
            "unit testing": [r"\bunit testing\b"],
            "integration testing": [r"\bintegration testing\b"],
            "test automation": [r"\btest automation\b"],
        },
        
        "Other Skills": {
            "api": [r"\bapi\b", r"\brest api\b"],
            "microservices": [r"\bmicroservices\b"],
            "agile": [r"\bagile\b"],
            "scrum": [r"\bscrum\b"],
            "linux": [r"\blinux\b"],
            "unix": [r"\bunix\b"],
            "windows": [r"\bwindows\b"],
            "json": [r"\bjson\b"],
            "xml": [r"\bxml\b"],
            "yaml": [r"\byaml\b"],
        },
    }
    
    # Aliases mapping: maps abbreviated forms to full skill names
    ALIASES = {
        "ml": "machine learning",
        "dl": "deep learning",
        "js": "javascript",
        "ts": "typescript",
        "nlp": "nlp",
        "cv": "computer vision",
        "k8s": "kubernetes",
        "cicd": "ci/cd",
        "sql": "sql",
        "nosql": "nosql",
    }

    def __init__(self):
        """Initialize skill extractor with unified pattern dictionary."""
        self.skill_patterns = self._build_skill_patterns()
    
    def _build_skill_patterns(self) -> Dict[str, re.Pattern]:
        """
        Build a unified dictionary of skill names to their regex patterns.
        
        Returns:
            Dict mapping skill names to compiled regex patterns (case-insensitive)
        """
        patterns = {}
        
        for category, skills in self.SKILL_DATABASE.items():
            for skill_name, regex_list in skills.items():
                # Combine all regex patterns for a skill with OR operator
                combined_pattern = "|".join(regex_list)
                patterns[skill_name] = re.compile(combined_pattern, re.IGNORECASE)
        
        return patterns
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize input text:
        - Convert to lowercase
        - Remove extra whitespace
        - Keep alphanumeric, spaces, and some special chars (+ # - /)
        
        Args:
            text: Raw input text
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Keep only alphanumeric, spaces, and relevant special characters
        text = "".join(c if c in "abcdefghijklmnopqrstuvwxyz0123456789 +#-/." else "" for c in text)
        
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using rule-based pattern matching.
        
        Args:
            text: Input text (resume, job description, etc.)
            
        Returns:
            Sorted list of unique extracted skills
            
        Example:
            >>> extractor = SkillExtractor()
            >>> skills = extractor.extract_skills("I have 5 years experience with Python and JavaScript")
            >>> print(skills)
            ['javascript', 'python']
        """
        if not text:
            return []
        
        # Normalize input
        normalized_text = self._normalize_text(text)
        
        extracted_skills: Set[str] = set()
        
        # Try to match each skill pattern against the normalized text
        for skill_name, pattern in self.skill_patterns.items():
            if pattern.search(normalized_text):
                extracted_skills.add(skill_name.lower())
        
        # Remove duplicates and return sorted list
        unique_skills = sorted(list(extracted_skills))
        
        return unique_skills
    
    def extract_skills_with_categories(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills and organize them by category.
        
        Args:
            text: Input text (resume, job description, etc.)
            
        Returns:
            Dictionary with categories as keys and lists of skills as values
            
        Example:
            >>> extractor = SkillExtractor()
            >>> result = extractor.extract_skills_with_categories("Python Django React")
            >>> print(result['Programming Languages'])
            ['python']
        """
        if not text:
            return {}
        
        normalized_text = self._normalize_text(text)
        categorized_skills: Dict[str, Set[str]] = {}
        
        # Build category index: skill_name -> category
        skill_to_category: Dict[str, str] = {}
        for category, skills in self.SKILL_DATABASE.items():
            for skill_name in skills.keys():
                skill_to_category[skill_name] = category
        
        # Extract skills
        for skill_name, pattern in self.skill_patterns.items():
            if pattern.search(normalized_text):
                category = skill_to_category.get(skill_name, "Other")
                if category not in categorized_skills:
                    categorized_skills[category] = set()
                categorized_skills[category].add(skill_name.lower())
        
        # Convert sets to sorted lists
        result = {}
        for category in sorted(categorized_skills.keys()):
            result[category] = sorted(list(categorized_skills[category]))
        
        return result
    
    def get_all_skills(self) -> List[str]:
        """
        Get list of all known skills in the database.
        
        Returns:
            Sorted list of all skill names
        """
        all_skills = []
        for skills in self.SKILL_DATABASE.values():
            all_skills.extend(skills.keys())
        return sorted(list(set(all_skills)))
    
    def get_skills_by_category(self, category: str) -> List[str]:
        """
        Get all skills in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Sorted list of skills in that category
        """
        if category in self.SKILL_DATABASE:
            return sorted(list(self.SKILL_DATABASE[category].keys()))
        return []
    
    def get_categories(self) -> List[str]:
        """
        Get all available skill categories.
        
        Returns:
            Sorted list of category names
        """
        return sorted(list(self.SKILL_DATABASE.keys()))


# Module-level function for convenience
def extract_skills(text: str) -> List[str]:
    """
    Convenience function to extract skills from text.
    
    Args:
        text: Input text (resume, job description, etc.)
        
    Returns:
        Sorted list of unique extracted skills
        
    Example:
        >>> skills = extract_skills("I know Python, JavaScript, and React")
        >>> print(skills)
        ['javascript', 'python', 'react']
    """
    extractor = SkillExtractor()
    return extractor.extract_skills(text)


# For backward compatibility
class SkillMatcher:
    """Alias for SkillExtractor for backward compatibility."""
    
    def __init__(self):
        self.extractor = SkillExtractor()
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        return self.extractor.extract_skills(text)
    
    def extract_skills_with_categories(self, text: str) -> Dict[str, List[str]]:
        """Extract skills organized by category."""
        return self.extractor.extract_skills_with_categories(text)


if __name__ == "__main__":
    # Example usage
    extractor = SkillExtractor()
    
    # Test text
    sample_text = """
    Experienced software engineer with 5+ years in Python, JavaScript, and React.
    Strong background in Machine Learning, Deep Learning, and NLP.
    Knowledge of Django, FastAPI, Node.js, and Express.
    Proficient in SQL, MongoDB, PostgreSQL, and Redis.
    Skilled in AWS, Docker, Kubernetes, Git, and CI/CD pipelines.
    Familiar with TensorFlow, PyTorch, and scikit-learn.
    """
    
    # Extract all skills
    print("=" * 60)
    print("SKILL EXTRACTION DEMO")
    print("=" * 60)
    print(f"\nInput Text:\n{sample_text}\n")
    
    skills = extractor.extract_skills(sample_text)
    print(f"Extracted Skills ({len(skills)} total):")
    print(skills)
    
    # Extract skills with categories
    print("\n" + "=" * 60)
    print("SKILLS BY CATEGORY:")
    print("=" * 60)
    categorized = extractor.extract_skills_with_categories(sample_text)
    for category, category_skills in categorized.items():
        print(f"\n{category}:")
        for skill in category_skills:
            print(f"  - {skill}")
    
    # Get all available categories
    print("\n" + "=" * 60)
    print("AVAILABLE CATEGORIES:")
    print("=" * 60)
    categories = extractor.get_categories()
    for cat in categories:
        count = len(extractor.get_skills_by_category(cat))
        print(f"  - {cat}: {count} skills")

