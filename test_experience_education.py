from resume_parser import extract_resume_text

from experience_education import (
    analyze_experience_and_education
)


# ============================================================
# RESUME
# ============================================================

resume_file = "SHIFA_SAREEN_CV_4 (3).pdf"


# ============================================================
# EXTRACT RESUME TEXT
# ============================================================

resume_text = extract_resume_text(
    resume_file
)


# ============================================================
# ANALYZE EXPERIENCE + EDUCATION
# ============================================================

result = analyze_experience_and_education(
    resume_text,
    required_years=1,
    required_education_level=3
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n==============================")
print("EXPERIENCE & EDUCATION ANALYSIS")
print("==============================")


print(
    "\nExperience:",
    result["experience_years"],
    "years"
)


print(
    "Education:",
    result["education"]
)


print(
    "Education Level:",
    result["education_level"]
)


print(
    "\nExperience Score:",
    result["experience_score"],
    "%"
)


print(
    "Education Score:",
    result["education_score"],
    "%"
)


print("==============================")