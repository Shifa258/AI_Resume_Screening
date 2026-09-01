"""
============================================================
ranker.py
AI Resume Screening System
Production ATS Ranking Engine
============================================================

SCORING

    Required / Core Skills       40%
    Preferred Skills             10%
    ATS Keywords                 10%
    TF-IDF Similarity             10%
    Relevant Experience          20%
    Education                    10%

TOTAL                           100%

MATCHING

    1. Exact canonical match      = 100%
    2. Alias/canonical match      = 100%
    3. Related skill match        = partial credit
    4. No match                   = 0%

Compatible with:
    skills.py
    skill_extractor.py
    keyword_extractor.py
    app.py
============================================================
"""

import re
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skill_extractor import extract_skills, canonicalize_skill

from keyword_extractor import (
    calculate_keyword_score,
    get_matched_keywords,
    get_missing_keywords,
)


# ============================================================
# WEIGHTS
# ============================================================

REQUIRED_WEIGHT = 0.40
PREFERRED_WEIGHT = 0.10
KEYWORD_WEIGHT = 0.10
TFIDF_WEIGHT = 0.10
EXPERIENCE_WEIGHT = 0.20
EDUCATION_WEIGHT = 0.10


# ============================================================
# RELATED SKILLS
# ============================================================

RELATED_SKILLS = {
    # DATABASE
    "mysql": {
        "sql": 0.65,
        "postgresql": 0.65,
        "sqlite": 0.55,
        "database": 0.45,
    },
    "postgresql": {
        "sql": 0.65,
        "mysql": 0.65,
        "sqlite": 0.55,
        "database": 0.45,
    },
    "sql": {
        "mysql": 0.70,
        "postgresql": 0.70,
        "sqlite": 0.60,
        "database": 0.45,
    },
    "mongodb": {
        "database": 0.45,
        "nosql": 0.70,
    },
    "nosql": {
        "mongodb": 0.70,
        "database": 0.45,
    },

    # PROGRAMMING
    "python": {
        "pandas": 0.55,
        "numpy": 0.55,
        "scikit-learn": 0.55,
        "machine learning": 0.45,
    },
    "javascript": {
        "typescript": 0.75,
        "node.js": 0.65,
        "react": 0.45,
    },
    "typescript": {
        "javascript": 0.80,
        "node.js": 0.55,
        "react": 0.45,
    },
    "java": {
        "spring": 0.55,
        "spring boot": 0.55,
    },
    "c++": {
        "c": 0.55,
    },

    # WEB
    "node.js": {
        "javascript": 0.70,
        "express.js": 0.60,
        "typescript": 0.55,
    },
    "express.js": {
        "node.js": 0.65,
        "javascript": 0.60,
    },
    "react": {
        "javascript": 0.60,
        "typescript": 0.55,
        "next.js": 0.60,
    },
    "next.js": {
        "react": 0.70,
        "javascript": 0.55,
        "typescript": 0.50,
    },

    # DATA SCIENCE / AI
    "machine learning": {
        "scikit-learn": 0.65,
        "pandas": 0.45,
        "numpy": 0.45,
        "statistics": 0.55,
        "artificial intelligence": 0.60,
    },
    "artificial intelligence": {
        "machine learning": 0.65,
        "deep learning": 0.70,
        "computer vision": 0.55,
        "generative ai": 0.55,
        "large language model": 0.55,
    },
    "deep learning": {
        "machine learning": 0.75,
        "artificial intelligence": 0.65,
        "tensorflow": 0.60,
        "pytorch": 0.60,
    },
    "pandas": {
        "python": 0.55,
        "numpy": 0.60,
        "data analysis": 0.55,
        "data analytics": 0.55,
    },
    "numpy": {
        "python": 0.55,
        "pandas": 0.60,
    },
    "scikit-learn": {
        "python": 0.65,
        "machine learning": 0.75,
    },
    "tensorflow": {
        "deep learning": 0.65,
        "machine learning": 0.60,
    },
    "pytorch": {
        "deep learning": 0.65,
        "machine learning": 0.60,
    },

    # BI / VISUALIZATION
    "power bi": {
        "tableau": 0.45,
        "data visualization": 0.60,
        "data analysis": 0.40,
    },
    "tableau": {
        "power bi": 0.45,
        "data visualization": 0.60,
        "data analysis": 0.40,
    },
    "data visualization": {
        "power bi": 0.65,
        "tableau": 0.65,
    },

    # CLOUD
    "aws": {
        "azure": 0.55,
        "google cloud": 0.50,
        "cloud computing": 0.70,
    },
    "azure": {
        "aws": 0.55,
        "google cloud": 0.50,
        "cloud computing": 0.70,
    },
    "google cloud": {
        "aws": 0.50,
        "azure": 0.50,
        "cloud computing": 0.70,
    },

    # DEVOPS
    "docker": {
        "kubernetes": 0.65,
        "containerization": 0.75,
    },
    "kubernetes": {
        "docker": 0.65,
        "containerization": 0.75,
    },
    "jenkins": {
        "github actions": 0.65,
        "ci/cd": 0.70,
    },
    "github actions": {
        "jenkins": 0.65,
        "ci/cd": 0.70,
    },

    # TESTING
    "selenium": {
        "automation testing": 0.70,
        "test automation": 0.70,
    },
    "manual testing": {
        "software testing": 0.70,
        "quality assurance": 0.55,
    },
    "quality assurance": {
        "quality control": 0.65,
        "software testing": 0.55,
        "manual testing": 0.50,
    },
    "quality control": {
        "quality assurance": 0.65,
        "data quality": 0.55,
    },
    "software testing": {
        "quality assurance": 0.55,
        "manual testing": 0.70,
        "automation testing": 0.65,
    },

    # AI / LLM
    "large language model": {
        "generative ai": 0.75,
        "artificial intelligence": 0.55,
        "machine learning": 0.45,
    },
    "generative ai": {
        "large language model": 0.80,
        "artificial intelligence": 0.60,
        "machine learning": 0.45,
    },
    "computer vision": {
        "deep learning": 0.60,
        "machine learning": 0.55,
        "artificial intelligence": 0.50,
    },

    # DATA OPERATIONS
    "data analysis": {
        "data analytics": 0.85,
        "statistics": 0.45,
        "data visualization": 0.50,
    },
    "data analytics": {
        "data analysis": 0.85,
        "statistics": 0.50,
        "data visualization": 0.50,
    },
    "data cleaning": {
        "data preprocessing": 0.75,
        "data preparation": 0.75,
        "data quality": 0.55,
    },
    "data preprocessing": {
        "data cleaning": 0.75,
        "data preparation": 0.75,
    },
    "data validation": {
        "data quality": 0.70,
        "quality assurance": 0.45,
    },
    "data quality": {
        "data validation": 0.70,
        "quality assurance": 0.45,
        "quality control": 0.45,
    },
}


# ============================================================
# GENERIC TERMS
# ============================================================

GENERIC_TERMS = {
    "application",
    "applications",
    "computer",
    "education",
    "degree",
    "bachelor",
    "bachelors",
    "master",
    "masters",
    "requirement",
    "requirements",
    "qualification",
    "qualifications",
    "experience",
    "year",
    "years",
    "job",
    "role",
    "position",
    "candidate",
    "candidates",
    "associate",
    "project",
    "projects",
    "work",
    "team",
    "teams",
    "responsibility",
    "responsibilities",
    "preferred",
    "required",
    "skill",
    "skills",
    "related",
    "field",
    "organization",
    "company",
    "business",
    "professional",
    "environment",
    "ability",
    "abilities",
    "knowledge",
    "looking",
    "support",
    "using",
    "used",
    "use",
    "include",
    "including",
    "maintain",
    "maintaining",
    "perform",
    "performing",
    "provide",
    "provided",
    "ensure",
    "ensuring",
    "follow",
    "following",
    "collaborate",
    "collaboration",
    "responsible",
}


# ============================================================
# EDUCATION TERMS
# ============================================================

EDUCATION_TERMS = {
    "bca",
    "bsc",
    "b.sc",
    "btech",
    "b.tech",
    "be",
    "b.e",
    "bba",
    "bcom",
    "b.com",
    "ba",
    "mca",
    "msc",
    "m.sc",
    "mba",
    "mcom",
    "m.com",
    "phd",
    "ph.d",
    "bachelor",
    "bachelors",
    "master",
    "masters",
    "doctorate",
    "computer applications",
    "computer science",
    "information technology",
    "data science",
    "data analytics",
}


# ============================================================
# INVALID SKILL FRAGMENTS
# ============================================================

INVALID_SKILL_FRAGMENTS = {
    "analysis",
    "analytics",
    "annotation",
    "cleaning",
    "validation",
    "visualization",
    "visualisation",
    "preprocessing",
    "report",
    "reports",
    "labeling",
    "labelling",
    "quality",
    "checking",
    "verification",
    "interpretation",
    "management",
    "thinking",
    "solving",
    "communication",
    "documentation",
}


# ============================================================
# MONTHS
# ============================================================

MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    replacements = {
        "–": "-",
        "—": "-",
        "−": "-",
        "•": " ",
        "●": " ",
        "▪": " ",
        "◦": " ",
        "\u00a0": " ",
        "&": " and ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9+#./\s:-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SAFE PERCENTAGE
# ============================================================

def safe_percentage(value):
    try:
        value = float(value)
    except Exception:
        return 0.0

    return round(max(0.0, min(100.0, value)), 2)


# ============================================================
# PHRASE PRESENT
# ============================================================

def phrase_present(text, phrase):
    text = normalize_text(text)
    phrase = normalize_text(phrase)

    if not text or not phrase:
        return False

    return bool(
        re.search(
            r"(?<!\w)" + re.escape(phrase) + r"(?!\w)",
            text,
        )
    )


# ============================================================
# CANONICAL SKILL
# ============================================================

def canonical_skill(skill):
    if not skill:
        return ""

    original = normalize_text(skill)

    if not original:
        return ""

    if original in INVALID_SKILL_FRAGMENTS:
        return ""

    try:
        canonical = canonicalize_skill(original)
        canonical = normalize_text(canonical)

        if canonical in INVALID_SKILL_FRAGMENTS:
            return ""

        return canonical or original

    except Exception:
        return original


# ============================================================
# REAL SKILL
# ============================================================

def is_real_skill(skill):
    normalized = normalize_text(skill)

    if not normalized:
        return False

    if normalized in GENERIC_TERMS:
        return False

    if normalized in EDUCATION_TERMS:
        return False

    if normalized in INVALID_SKILL_FRAGMENTS:
        return False

    return True


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills_from_text(text):
    if not text:
        return set()

    found = set()

    try:
        detected = extract_skills(text)
    except Exception:
        detected = []

    for skill in detected or []:
        canonical = canonical_skill(skill)

        if not canonical:
            continue

        if not is_real_skill(canonical):
            continue

        found.add(canonical)

    return found


# ============================================================
# RECOVER KNOWN MULTI-WORD SKILLS
# ============================================================

def recover_known_skills(text, current_skills=None):
    current_skills = set(current_skills or [])

    normalized_text = normalize_text(text)

    if not normalized_text:
        return current_skills

    try:
        from skills import SKILLS
    except Exception:
        SKILLS = []

    for skill in SKILLS:
        canonical = canonical_skill(skill)

        if not canonical:
            continue

        if not is_real_skill(canonical):
            continue

        if len(canonical.split()) < 2:
            continue

        if phrase_present(normalized_text, canonical):
            current_skills.add(canonical)

    return current_skills


# ============================================================
# FINAL SKILLS
# ============================================================

def get_clean_skills(text):
    skills = extract_skills_from_text(text)

    skills = recover_known_skills(
        text,
        skills,
    )

    cleaned = set()

    for skill in skills:
        canonical = canonical_skill(skill)

        if canonical and is_real_skill(canonical):
            cleaned.add(canonical)

    return cleaned


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(text, section_names):
    if not text:
        return ""

    lines = str(text).splitlines()

    targets = {
        normalize_text(name).rstrip(":").strip()
        for name in section_names
    }

    headers = {
        "required skills",
        "required",
        "requirements",
        "job requirements",
        "required qualifications",
        "preferred skills",
        "preferred",
        "nice to have",
        "good to have",
        "desirable skills",
        "technical skills",
        "technical requirements",
        "experience",
        "experience requirements",
        "work experience",
        "professional experience",
        "education",
        "education requirements",
        "educational qualifications",
        "academic qualifications",
        "qualifications",
        "responsibilities",
        "key responsibilities",
        "roles and responsibilities",
        "duties",
        "benefits",
        "location",
        "salary",
        "job description",
    }

    collecting = False
    result = []

    for line in lines:
        clean = normalize_text(line)

        if not clean:
            if collecting:
                result.append(line)
            continue

        clean = re.sub(
            r"^[•●▪◦\-*]+\s*",
            "",
            clean,
        )

        clean = clean.rstrip(":").strip()

        if clean in targets:
            collecting = True
            continue

        if collecting and clean in headers:
            break

        if collecting:
            result.append(line)

    return "\n".join(result).strip()


# ============================================================
# JOB SKILLS
# ============================================================

def parse_job_skills(job_description):
    if not job_description:
        return [], []

    required_text = extract_section(
        job_description,
        [
            "required skills",
            "required",
            "requirements",
            "job requirements",
            "required qualifications",
            "technical requirements",
        ],
    )

    preferred_text = extract_section(
        job_description,
        [
            "preferred skills",
            "preferred",
            "nice to have",
            "good to have",
            "desirable skills",
        ],
    )

    required_skills = get_clean_skills(required_text)
    preferred_skills = get_clean_skills(preferred_text)

    # If no explicit sections exist, use the complete JD.
    if not required_skills and not preferred_skills:
        required_skills = get_clean_skills(job_description)

    # If only preferred skills were detected, treat other skills
    # in the JD as required.
    elif not required_skills:
        all_skills = get_clean_skills(job_description)
        required_skills = all_skills - preferred_skills

    preferred_skills -= required_skills

    return (
        sorted(required_skills),
        sorted(preferred_skills),
    )


# ============================================================
# RELATED SKILL SCORE
# ============================================================

def get_related_skill_score(required_skill, resume_skills):
    required = canonical_skill(required_skill)

    if not required:
        return 0.0

    resume_set = {
        canonical_skill(skill)
        for skill in resume_skills
        if canonical_skill(skill)
    }

    if required in resume_set:
        return 1.0

    related = RELATED_SKILLS.get(required, {})
    best_score = 0.0

    for resume_skill in resume_set:
        score = related.get(resume_skill, 0.0)

        if score > best_score:
            best_score = score

    return best_score


# ============================================================
# MATCH SKILLS WITH PARTIAL CREDIT
# ============================================================

def match_skills(resume_skills, job_skills):
    resume_set = {
        canonical_skill(skill)
        for skill in resume_skills
        if canonical_skill(skill)
        and is_real_skill(skill)
    }

    job_set = {
        canonical_skill(skill)
        for skill in job_skills
        if canonical_skill(skill)
        and is_real_skill(skill)
    }

    results = []

    for required in sorted(job_set):
        if required in resume_set:
            results.append({
                "required_skill": required,
                "matched_skill": required,
                "score": 1.0,
                "match_type": "exact",
            })
            continue

        related = RELATED_SKILLS.get(required, {})

        best_skill = None
        best_score = 0.0

        for resume_skill in resume_set:
            partial = related.get(resume_skill, 0.0)

            if partial > best_score:
                best_score = partial
                best_skill = resume_skill

        if best_score > 0:
            results.append({
                "required_skill": required,
                "matched_skill": best_skill,
                "score": best_score,
                "match_type": "related",
            })
        else:
            results.append({
                "required_skill": required,
                "matched_skill": None,
                "score": 0.0,
                "match_type": "missing",
            })

    return results


# ============================================================
# SKILL SCORE
# ============================================================

def calculate_skill_score(resume_skills, job_skills):
    if not job_skills:
        return 100.0

    matches = match_skills(
        resume_skills,
        job_skills,
    )

    if not matches:
        return 0.0

    total = sum(
        item["score"]
        for item in matches
    )

    return safe_percentage(
        (total / len(matches)) * 100.0
    )


# ============================================================
# EXPERIENCE REQUIREMENT
# ============================================================

def extract_required_experience(job_description):
    text = normalize_text(job_description)

    if not text:
        return {
            "minimum": 0.0,
            "maximum": None,
        }

    range_patterns = [
        r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*years?",
        r"(\d+(?:\.\d+)?)\s+to\s+(\d+(?:\.\d+)?)\s*years?",
    ]

    for pattern in range_patterns:
        match = re.search(pattern, text)

        if match:
            return {
                "minimum": float(match.group(1)),
                "maximum": float(match.group(2)),
            }

    minimum_patterns = [
        r"(\d+(?:\.\d+)?)\s*\+\s*years?",
        r"(\d+(?:\.\d+)?)\s+or\s+more\s+years?",
        r"at\s+least\s+(\d+(?:\.\d+)?)\s*years?",
        r"minimum\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*years?",
        r"(\d+(?:\.\d+)?)\s*years?\s+(?:of\s+)?experience",
        r"experience\s+of\s+(\d+(?:\.\d+)?)\s*years?",
    ]

    for pattern in minimum_patterns:
        match = re.search(pattern, text)

        if match:
            return {
                "minimum": float(match.group(1)),
                "maximum": None,
            }

    return {
        "minimum": 0.0,
        "maximum": None,
    }


# ============================================================
# DATE PARSING
# ============================================================

def parse_date_part(value):
    if not value:
        return None

    value = normalize_text(value).strip()

    if value in {
        "present",
        "current",
        "now",
        "till date",
        "till now",
        "currently",
    }:
        today = datetime.now()
        return today.year, today.month

    match = re.search(
        r"\b(0?[1-9]|1[0-2])\s*[./-]\s*(20\d{2})\b",
        value,
    )

    if match:
        return (
            int(match.group(2)),
            int(match.group(1)),
        )

    match = re.search(
        r"\b(20\d{2})\s*[./-]\s*(0?[1-9]|1[0-2])\b",
        value,
    )

    if match:
        return (
            int(match.group(1)),
            int(match.group(2)),
        )

    month_pattern = (
        r"(jan(?:uary)?|"
        r"feb(?:ruary)?|"
        r"mar(?:ch)?|"
        r"apr(?:il)?|"
        r"may|"
        r"jun(?:e)?|"
        r"jul(?:y)?|"
        r"aug(?:ust)?|"
        r"sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|"
        r"nov(?:ember)?|"
        r"dec(?:ember)?)"
        r"\s*,?\s*(20\d{2})"
    )

    match = re.search(
        month_pattern,
        value,
    )

    if match:
        month_name = match.group(1)

        return (
            int(match.group(2)),
            MONTHS.get(month_name[:3], 1),
        )

    match = re.search(
        r"\b(20\d{2})\b",
        value,
    )

    if match:
        return (
            int(match.group(1)),
            1,
        )

    return None


# ============================================================
# EXPERIENCE DATE RANGES
# ============================================================

def extract_resume_date_ranges(resume_text):
    if not resume_text:
        return []

    text = normalize_text(resume_text)
    ranges = []

    numeric_date = (
        r"(?:0?[1-9]|1[0-2])"
        r"\s*[./-]\s*20\d{2}"
    )

    numeric_pattern = re.compile(
        r"("
        + numeric_date
        + r")"
        r"\s*(?:-|to)\s*"
        r"("
        + numeric_date
        + r"|present|current|now|currently"
        + r")"
    )

    for match in numeric_pattern.finditer(text):
        ranges.append(
            (
                match.group(1),
                match.group(2),
            )
        )

    month_date = (
        r"(?:jan(?:uary)?|"
        r"feb(?:ruary)?|"
        r"mar(?:ch)?|"
        r"apr(?:il)?|"
        r"may|"
        r"jun(?:e)?|"
        r"jul(?:y)?|"
        r"aug(?:ust)?|"
        r"sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|"
        r"nov(?:ember)?|"
        r"dec(?:ember)?)"
        r"\s*,?\s*20\d{2}"
    )

    month_pattern = re.compile(
        r"("
        + month_date
        + r")"
        r"\s*(?:-|to)\s*"
        r"("
        + month_date
        + r"|present|current|now|currently"
        + r")"
    )

    for match in month_pattern.finditer(text):
        ranges.append(
            (
                match.group(1),
                match.group(2),
            )
        )

    year_pattern = re.compile(
        r"\b(20\d{2})\b"
        r"\s*(?:-|to)\s*"
        r"\b(20\d{2})\b"
    )

    for match in year_pattern.finditer(text):
        ranges.append(
            (
                match.group(1),
                match.group(2),
            )
        )

    year_present_pattern = re.compile(
        r"\b(20\d{2})\b"
        r"\s*(?:-|to)\s*"
        r"(present|current|now|currently)"
    )

    for match in year_present_pattern.finditer(text):
        ranges.append(
            (
                match.group(1),
                match.group(2),
            )
        )

    return ranges


# ============================================================
# MERGE PERIODS
# ============================================================

def merge_experience_periods(periods):
    if not periods:
        return []

    valid = []

    for start, end in periods:
        start_date = parse_date_part(start)
        end_date = parse_date_part(end)

        if not start_date or not end_date:
            continue

        start_index = (
            start_date[0] * 12
            + start_date[1]
        )

        end_index = (
            end_date[0] * 12
            + end_date[1]
        )

        if end_index <= start_index:
            continue

        valid.append(
            (
                start_index,
                end_index,
            )
        )

    if not valid:
        return []

    valid.sort()

    merged = [valid[0]]

    for current in valid[1:]:
        previous = merged[-1]

        if current[0] <= previous[1]:
            merged[-1] = (
                previous[0],
                max(
                    previous[1],
                    current[1],
                ),
            )
        else:
            merged.append(current)

    return merged


# ============================================================
# RESUME EXPERIENCE
# ============================================================

def extract_resume_experience(resume_text):
    if not resume_text:
        return 0.0

    text = normalize_text(resume_text)

    explicit_years = []

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+"
        r"(?:of\s+)?experience",
        text,
    )

    for value in matches:
        try:
            explicit_years.append(float(value))
        except Exception:
            pass

    ranges = extract_resume_date_ranges(resume_text)
    merged = merge_experience_periods(ranges)

    total_months = sum(
        end - start
        for start, end in merged
    )

    date_years = (
        total_months / 12.0
        if total_months > 0
        else 0.0
    )

    if date_years > 0:
        if explicit_years:
            explicit_max = max(explicit_years)

            if explicit_max <= date_years + 1.0:
                return round(
                    max(
                        date_years,
                        explicit_max,
                    ),
                    1,
                )

        return round(date_years, 1)

    if explicit_years:
        return round(max(explicit_years), 1)

    return 0.0


# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(
    candidate_years,
    required_minimum,
    required_maximum=None,
):
    try:
        candidate_years = float(candidate_years)
    except Exception:
        candidate_years = 0.0

    try:
        required_minimum = float(required_minimum)
    except Exception:
        required_minimum = 0.0

    if required_maximum is not None:
        try:
            required_maximum = float(required_maximum)
        except Exception:
            required_maximum = None

    if required_minimum <= 0:
        return 100.0

    if candidate_years < required_minimum:
        return safe_percentage(
            (candidate_years / required_minimum) * 100
        )

    return 100.0


# ============================================================
# EDUCATION LEVEL
# ============================================================

def detect_education_level(resume_text):
    text = normalize_text(resume_text)

    if not text:
        return "Not Detected"

    if re.search(
        r"\bphd\b|\bph\.d\b|\bdoctorate\b|\bdoctoral\b",
        text,
    ):
        return "PhD"

    if re.search(
        r"\bmca\b|\bmsc\b|\bm\.sc\b|\bmba\b|"
        r"\bmcom\b|\bm\.com\b|\bmaster(?:'s)?\b",
        text,
    ):
        return "Master's Degree"

    if re.search(
        r"\bbca\b|\bbsc\b|\bb\.sc\b|\bbtech\b|"
        r"\bb\.tech\b|\bbe\b|\bb\.e\b|\bbba\b|"
        r"\bbcom\b|\bb\.com\b|\bba\b|"
        r"\bbachelor(?:'s)?\b",
        text,
    ):
        return "Bachelor's Degree"

    if re.search(
        r"\bdiploma\b|\bpolytechnic\b",
        text,
    ):
        return "Diploma"

    return "Not Detected"


# ============================================================
# EDUCATION FIELDS
# ============================================================

EDUCATION_FIELDS = {
    "computer science": {
        "computer science",
        "computer applications",
        "information technology",
        "software engineering",
        "data science",
    },
    "computer applications": {
        "computer applications",
        "computer science",
        "information technology",
        "software engineering",
        "data science",
    },
    "information technology": {
        "information technology",
        "computer science",
        "computer applications",
        "software engineering",
    },
    "data science": {
        "data science",
        "data analytics",
        "statistics",
        "computer science",
        "information technology",
        "computer applications",
    },
    "data analytics": {
        "data analytics",
        "data science",
        "statistics",
        "computer science",
        "information technology",
    },
    "business administration": {
        "business administration",
        "management",
        "commerce",
    },
}


# ============================================================
# EDUCATION REQUIREMENT
# ============================================================

def education_requirement_type(jd):
    jd = normalize_text(jd)

    if not jd:
        return None

    if re.search(
        r"\bphd\b|\bph\.d\b|\bdoctorate\b",
        jd,
    ):
        return "phd"

    if re.search(
        r"\bmaster(?:'s)?\b|\bmca\b|\bmba\b|\bmsc\b|"
        r"\bm\.sc\b|\bmcom\b|\bm\.com\b",
        jd,
    ):
        return "master"

    if re.search(
        r"\bbachelor(?:'s)?\b|\bbca\b|\bbsc\b|\bb\.sc\b|"
        r"\bbtech\b|\bb\.tech\b|\bbe\b|\bb\.e\b|\bbba\b|"
        r"\bbcom\b|\bb\.com\b",
        jd,
    ):
        return "bachelor"

    if re.search(r"\bdegree\b", jd):
        return "degree"

    return None


# ============================================================
# DETECT EDUCATION FIELDS
# ============================================================

def detect_education_fields(text):
    text = normalize_text(text)
    fields = set()

    for field in EDUCATION_FIELDS:
        if phrase_present(text, field):
            fields.add(field)

    if re.search(
        r"\bbca\b|\bbachelor of computer applications\b",
        text,
    ):
        fields.add("computer applications")

    if re.search(r"\bbsc\b|\bb\.sc\b", text):
        if phrase_present(text, "computer science"):
            fields.add("computer science")

        if phrase_present(text, "data science"):
            fields.add("data science")

        if phrase_present(text, "data analytics"):
            fields.add("data analytics")

        if phrase_present(text, "information technology"):
            fields.add("information technology")

    if re.search(
        r"\bbtech\b|\bb\.tech\b|\bbe\b|\bb\.e\b",
        text,
    ):
        if phrase_present(text, "computer science"):
            fields.add("computer science")

        if phrase_present(text, "information technology"):
            fields.add("information technology")

    if re.search(
        r"\bmca\b|\bmaster of computer applications\b",
        text,
    ):
        fields.add("computer applications")

    return fields


# ============================================================
# EDUCATION FIELD REQUIREMENT
# ============================================================

def detect_required_education_fields(jd):
    text = normalize_text(jd)
    fields = set()

    for field in EDUCATION_FIELDS:
        if phrase_present(text, field):
            fields.add(field)

    return fields


# ============================================================
# EDUCATION SCORE
# ============================================================

def calculate_education_score(
    resume_text,
    job_description,
):
    resume = normalize_text(resume_text)
    jd = normalize_text(job_description)

    if not resume or not jd:
        return 0.0

    requirement = education_requirement_type(jd)

    if requirement is None:
        return 100.0

    resume_level = detect_education_level(resume)

    if requirement == "phd":
        if resume_level != "PhD":
            return 0.0

    elif requirement == "master":
        if resume_level not in {
            "Master's Degree",
            "PhD",
        }:
            return 0.0

    elif requirement == "bachelor":
        if resume_level not in {
            "Bachelor's Degree",
            "Master's Degree",
            "PhD",
        }:
            return 0.0

    elif requirement == "degree":
        if resume_level == "Not Detected":
            return 0.0

    required_fields = detect_required_education_fields(jd)

    if not required_fields:
        return 100.0

    resume_fields = detect_education_fields(resume)

    if not resume_fields:
        return 50.0

    if resume_fields.intersection(required_fields):
        return 100.0

    for resume_field in resume_fields:
        related = EDUCATION_FIELDS.get(
            resume_field,
            set(),
        )

        if related.intersection(required_fields):
            return 85.0

    return 60.0


# ============================================================
# TF-IDF
# ============================================================

def calculate_tfidf_score(
    resume_text,
    job_description,
):
    resume = normalize_text(resume_text)
    jd = normalize_text(job_description)

    if not resume or not jd:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True,
        )

        matrix = vectorizer.fit_transform(
            [
                resume,
                jd,
            ]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2],
        )[0][0]

        return safe_percentage(
            similarity * 100
        )

    except Exception:
        return 0.0


# ============================================================
# CLEAN KEYWORDS
# ============================================================

def clean_keyword_list(keywords):
    cleaned = set()

    for keyword in keywords or []:
        normalized = normalize_text(keyword)

        if not normalized:
            continue

        if normalized in GENERIC_TERMS:
            continue

        if normalized in EDUCATION_TERMS:
            continue

        if normalized in INVALID_SKILL_FRAGMENTS:
            continue

        cleaned.add(normalized)

    return sorted(cleaned)


# ============================================================
# KEYWORD ANALYSIS
# ============================================================

def calculate_keyword_analysis(
    resume_text,
    job_description,
):
    try:
        score = calculate_keyword_score(
            resume_text,
            job_description,
        )
    except Exception:
        score = 0.0

    try:
        matched = get_matched_keywords(
            resume_text,
            job_description,
        )
    except Exception:
        matched = []

    try:
        missing = get_missing_keywords(
            resume_text,
            job_description,
        )
    except Exception:
        missing = []

    matched = clean_keyword_list(matched)
    missing = clean_keyword_list(missing)

    resume_skills = get_clean_skills(resume_text)

    resume_skill_set = {
        canonical_skill(skill)
        for skill in resume_skills
        if canonical_skill(skill)
    }

    fixed_missing = []

    for keyword in missing:
        canonical = canonical_skill(keyword)

        if canonical in resume_skill_set:
            continue

        if phrase_present(resume_text, keyword):
            continue

        fixed_missing.append(keyword)

    missing = sorted(set(fixed_missing))

    return (
        safe_percentage(score),
        matched,
        missing,
    )


# ============================================================
# MAIN ATS CALCULATION
# ============================================================

def calculate_final_score(
    resume_text,
    job_description,
    resume_skills=None,
):
    resume_text = resume_text or ""
    job_description = job_description or ""

    # --------------------------------------------------------
    # RESUME SKILLS
    # --------------------------------------------------------

    detected_resume_skills = get_clean_skills(
        resume_text
    )

    if resume_skills:
        for skill in resume_skills:
            canonical = canonical_skill(skill)

            if (
                canonical
                and is_real_skill(canonical)
            ):
                detected_resume_skills.add(canonical)

    resume_skills = sorted(detected_resume_skills)

    # --------------------------------------------------------
    # JOB SKILLS
    # --------------------------------------------------------

    required_skills, preferred_skills = parse_job_skills(
        job_description
    )

    # --------------------------------------------------------
    # CANONICAL SETS
    # --------------------------------------------------------

    resume_set = {
        canonical_skill(skill)
        for skill in resume_skills
        if canonical_skill(skill)
        and is_real_skill(skill)
    }

    required_set = {
        canonical_skill(skill)
        for skill in required_skills
        if canonical_skill(skill)
        and is_real_skill(skill)
    }

    preferred_set = {
        canonical_skill(skill)
        for skill in preferred_skills
        if canonical_skill(skill)
        and is_real_skill(skill)
    }

    resume_set.discard("")
    required_set.discard("")
    preferred_set.discard("")

    preferred_set -= required_set

    # --------------------------------------------------------
    # REQUIRED MATCHING
    # --------------------------------------------------------

    required_matches = match_skills(
        resume_set,
        required_set,
    )

    matched_required = sorted(
        item["required_skill"]
        for item in required_matches
        if item["score"] >= 1.0
    )

    related_required = sorted(
        [
            {
                "required_skill": item["required_skill"],
                "matched_skill": item["matched_skill"],
                "score": round(
                    item["score"] * 100,
                    2,
                ),
            }
            for item in required_matches
            if item["match_type"] == "related"
        ],
        key=lambda x: x["required_skill"],
    )

    missing_required = sorted(
        item["required_skill"]
        for item in required_matches
        if item["score"] <= 0
    )

    # --------------------------------------------------------
    # PREFERRED MATCHING
    # --------------------------------------------------------

    preferred_matches = match_skills(
        resume_set,
        preferred_set,
    )

    matched_preferred = sorted(
        item["required_skill"]
        for item in preferred_matches
        if item["score"] >= 1.0
    )

    related_preferred = sorted(
        [
            {
                "preferred_skill": item["required_skill"],
                "matched_skill": item["matched_skill"],
                "score": round(
                    item["score"] * 100,
                    2,
                ),
            }
            for item in preferred_matches
            if item["match_type"] == "related"
        ],
        key=lambda x: x["preferred_skill"],
    )

    missing_preferred = sorted(
        item["required_skill"]
        for item in preferred_matches
        if item["score"] <= 0
    )

    # --------------------------------------------------------
    # SKILL SCORES
    # --------------------------------------------------------

    required_score = calculate_skill_score(
        resume_set,
        required_set,
    )

    preferred_score = calculate_skill_score(
        resume_set,
        preferred_set,
    )

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------

    (
        keyword_score,
        matched_keywords,
        missing_keywords,
    ) = calculate_keyword_analysis(
        resume_text,
        job_description,
    )

    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    tfidf_score = calculate_tfidf_score(
        resume_text,
        job_description,
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    experience_requirement = extract_required_experience(
        job_description
    )

    required_years = experience_requirement["minimum"]
    maximum_years = experience_requirement["maximum"]

    experience_years = extract_resume_experience(
        resume_text
    )

    experience_score = calculate_experience_score(
        experience_years,
        required_years,
        maximum_years,
    )

    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    education_score = calculate_education_score(
        resume_text,
        job_description,
    )

    education_level = detect_education_level(
        resume_text
    )

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    final_score = (
        required_score * REQUIRED_WEIGHT
        + preferred_score * PREFERRED_WEIGHT
        + keyword_score * KEYWORD_WEIGHT
        + tfidf_score * TFIDF_WEIGHT
        + experience_score * EXPERIENCE_WEIGHT
        + education_score * EDUCATION_WEIGHT
    )

    final_score = safe_percentage(final_score)

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {
        "final_score": final_score,

        "required_score": safe_percentage(
            required_score
        ),

        "preferred_score": safe_percentage(
            preferred_score
        ),

        "keyword_score": safe_percentage(
            keyword_score
        ),

        "tfidf_score": safe_percentage(
            tfidf_score
        ),

        "experience_score": safe_percentage(
            experience_score
        ),

        "education_score": safe_percentage(
            education_score
        ),

        "experience_years": round(
            experience_years,
            1,
        ),

        "required_years": round(
            required_years,
            1,
        ),

        "required_maximum_years": (
            round(
                maximum_years,
                1,
            )
            if maximum_years is not None
            else None
        ),

        "education_level": education_level,

        "detected_resume_skills": sorted(
            resume_set
        ),

        "required_skills": sorted(
            required_set
        ),

        "preferred_skills": sorted(
            preferred_set
        ),

        "matched_skills": sorted(
            set(
                matched_required
                + matched_preferred
            )
        ),

        "matched_required_skills": matched_required,

        "missing_required_skills": missing_required,

        "matched_preferred_skills": matched_preferred,

        "missing_preferred_skills": missing_preferred,

        "related_required_skills": related_required,

        "related_preferred_skills": related_preferred,

        "missing_skills": missing_required,

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,
    }


# ============================================================
# RECOMMENDATION
# ============================================================

def get_recommendation(score):
    score = safe_percentage(score)

    if score >= 85:
        return "STRONGLY RECOMMENDED"

    if score >= 70:
        return "RECOMMENDED"

    if score >= 55:
        return "CONDITIONALLY RECOMMENDED"

    if score >= 40:
        return "NEEDS REVIEW"

    return "NOT RECOMMENDED"


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    SHIFA SAREEN

    BCA graduate with experience in data annotation
    and AI-related projects.

    Skills:

    Data Annotation
    Data Analysis
    Data Cleaning
    Data Validation
    Data Quality
    Quality Assurance
    Excel
    PowerPoint
    Documentation
    Reporting
    Communication
    Attention to Detail
    Analytical Thinking
    Problem Solving
    Machine Learning
    Artificial Intelligence

    Work Experience:

    Data Annotation Associate
    08/2025 - Present

    Worked on data quality checking and AI projects.
    """

    sample_jd = """
    Job Title: Data Annotation / AI Operations Associate

    Requirements:

    Bachelor's degree in Computer Applications,
    Computer Science, Information Technology,
    Data Science or related field.

    1-3 years of experience.

    Data Annotation
    Data Analysis
    Data Cleaning
    Data Validation
    Data Quality
    Quality Assurance
    Quality Control
    Microsoft Excel
    PowerPoint
    Documentation
    Reporting
    Communication
    Attention to Detail
    Analytical Thinking
    Problem Solving
    Machine Learning
    Artificial Intelligence

    Preferred Skills:

    Python
    SQL
    Pandas
    Power BI
    Tableau
    MySQL
    Statistics
    Computer Vision
    """

    result = calculate_final_score(
        sample_resume,
        sample_jd,
    )

    print()
    print("=" * 70)
    print("ATS TEST RESULT")
    print("=" * 70)

    print(
        "Final Score:",
        result["final_score"],
        "%",
    )

    print(
        "Required Skills:",
        result["required_score"],
        "%",
    )

    print(
        "Preferred Skills:",
        result["preferred_score"],
        "%",
    )

    print(
        "Keywords:",
        result["keyword_score"],
        "%",
    )

    print(
        "TF-IDF:",
        result["tfidf_score"],
        "%",
    )

    print(
        "Experience:",
        result["experience_score"],
        "%",
    )

    print(
        "Education:",
        result["education_score"],
        "%",
    )

    print(
        "Experience Years:",
        result["experience_years"],
    )

    print(
        "Required Years:",
        result["required_years"],
    )

    print(
        "Education:",
        result["education_level"],
    )

    print()
    print("Detected Resume Skills:")

    for skill in result["detected_resume_skills"]:
        print("✓", skill)

    print()
    print("Matched Required Skills:")

    for skill in result["matched_required_skills"]:
        print("✓", skill)

    print()
    print("Related Required Skills:")

    for item in result["related_required_skills"]:
        print(
            "~",
            item["required_skill"],
            "<-",
            item["matched_skill"],
            "(",
            item["score"],
            "%)",
        )

    print()
    print("Missing Required Skills:")

    for skill in result["missing_required_skills"]:
        print("✗", skill)

    print()
    print("Matched Preferred Skills:")

    for skill in result["matched_preferred_skills"]:
        print("✓", skill)

    print()
    print("Related Preferred Skills:")

    for item in result["related_preferred_skills"]:
        print(
            "~",
            item["preferred_skill"],
            "<-",
            item["matched_skill"],
            "(",
            item["score"],
            "%)",
        )

    print()
    print("Missing Preferred Skills:")

    for skill in result["missing_preferred_skills"]:
        print("✗", skill)

    print()
    print("Matched Keywords:")

    for keyword in result["matched_keywords"]:
        print("✓", keyword)

    print()
    print("Missing Keywords:")

    for keyword in result["missing_keywords"]:
        print("✗", keyword)

    print()
    print(
        "Recommendation:",
        get_recommendation(
            result["final_score"]
        ),
    )

    print("=" * 70)