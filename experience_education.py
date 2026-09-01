import re
from datetime import datetime


# ============================================================
# EDUCATION LEVELS
# ============================================================

EDUCATION_LEVELS = {
    "phd": 5,
    "doctorate": 5,
    "m.tech": 4,
    "mtech": 4,
    "mca": 4,
    "mba": 4,
    "m.sc": 4,
    "msc": 4,
    "master": 4,
    "b.tech": 3,
    "btech": 3,
    "b.e": 3,
    "be": 3,
    "bca": 3,
    "b.sc": 3,
    "bsc": 3,
    "bachelor": 3,
    "degree": 2,
    "diploma": 2,
    "puc": 1,
    "12th": 1,
    "higher secondary": 1,
    "sslc": 1,
    "10th": 1
}


# ============================================================
# EDUCATION
# ============================================================

def extract_education(resume_text):

    text = resume_text.lower()

    found = []

    for education, level in EDUCATION_LEVELS.items():

        pattern = r"(?<!\w)" + re.escape(education) + r"(?!\w)"

        if re.search(pattern, text):
            found.append((education, level))

    if not found:
        return {
            "education": "Not detected",
            "education_level": 0
        }

    highest = max(found, key=lambda x: x[1])

    return {
        "education": highest[0],
        "education_level": highest[1]
    }


# ============================================================
# DATE RANGES
# ============================================================

def extract_date_ranges(resume_text):

    text = resume_text.lower()

    current_year = datetime.now().year
    current_month = datetime.now().month

    pattern = (
        r"(\d{1,2})[/-](\d{4})"
        r"\s*[-–]\s*"
        r"(\d{1,2})[/-](\d{4}|current)"
    )

    matches = re.findall(pattern, text)

    ranges = []

    for match in matches:

        start_month = int(match[0])
        start_year = int(match[1])

        if match[3] == "current":
            end_month = current_month
            end_year = current_year
        else:
            end_month = int(match[2])
            end_year = int(match[3])

        start = start_year * 12 + start_month
        end = end_year * 12 + end_month

        if end > start:
            ranges.append((start, end))

    return ranges


# ============================================================
# MERGE OVERLAPPING PERIODS
# ============================================================

def merge_date_ranges(ranges):

    if not ranges:
        return []

    ranges = sorted(ranges)

    merged = [ranges[0]]

    for start, end in ranges[1:]:

        previous_start, previous_end = merged[-1]

        if start <= previous_end:

            merged[-1] = (
                previous_start,
                max(previous_end, end)
            )

        else:

            merged.append((start, end))

    return merged


# ============================================================
# DATE BASED EXPERIENCE
# ============================================================

def calculate_date_range_experience(resume_text):

    ranges = extract_date_ranges(resume_text)

    merged = merge_date_ranges(ranges)

    total_months = 0

    for start, end in merged:
        total_months += end - start

    return round(total_months / 12, 1)


# ============================================================
# EXPLICIT EXPERIENCE
# ============================================================

def extract_explicit_experience(resume_text):

    text = resume_text.lower()

    years = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*"
        r"(?:years?|yrs?)"
        r"(?:\s+of)?\s+(?:relevant\s+)?experience",
        text
    )

    months = re.findall(
        r"(\d+)\s*(?:months?|mos?)"
        r"(?:\s+of)?\s+(?:relevant\s+)?experience",
        text
    )

    total_months = 0

    for value in years:
        total_months += int(float(value) * 12)

    for value in months:
        total_months += int(value)

    return round(total_months / 12, 1)


# ============================================================
# TOTAL EXPERIENCE
# ============================================================

def calculate_experience(resume_text):

    date_experience = calculate_date_range_experience(
        resume_text
    )

    explicit_experience = extract_explicit_experience(
        resume_text
    )

    if date_experience > 0:
        return date_experience

    return explicit_experience


# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(
    resume_years,
    required_years
):

    if required_years <= 0:
        return 100.0

    score = (resume_years / required_years) * 100

    return round(min(score, 100), 2)


# ============================================================
# EDUCATION SCORE
# ============================================================

def calculate_education_score(
    resume_education_level,
    required_education_level
):

    if required_education_level <= 0:
        return 100.0

    if resume_education_level >= required_education_level:
        return 100.0

    if resume_education_level == 0:
        return 0.0

    score = (
        resume_education_level /
        required_education_level
    ) * 100

    return round(score, 2)


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def analyze_experience_and_education(
    resume_text,
    required_years=0,
    required_education_level=0
):

    experience_years = calculate_experience(
        resume_text
    )

    education = extract_education(
        resume_text
    )

    experience_score = calculate_experience_score(
        experience_years,
        required_years
    )

    education_score = calculate_education_score(
        education["education_level"],
        required_education_level
    )

    result = {
        "experience_years": experience_years,
        "education": education["education"],
        "education_level": education["education_level"],
        "experience_score": experience_score,
        "education_score": education_score
    }

    return result