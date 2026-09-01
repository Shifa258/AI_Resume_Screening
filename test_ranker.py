from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from ranker import calculate_final_score
from candidate_evaluator import evaluate_candidate


# ============================================================
# RESUME FILE
# ============================================================

resume_file = "SHIFA_SAREEN_CV_4 (3).pdf"


# ============================================================
# JOB DESCRIPTION
# ============================================================

job_description = """
We are looking for a Data Annotation Associate.

Required Skills:
Data Annotation
Quality Assurance
Communication
MS Excel

Preferred Skills:
Problem-solving
Leadership
MS Word
MS PowerPoint
Artificial Intelligence

The candidate should have experience working with
image, text, or LiDAR annotation projects.

The candidate should be able to follow project
guidelines, maintain high accuracy, meet productivity
targets, and work effectively with a team.
"""


# ============================================================
# EXTRACT RESUME
# ============================================================

print("\nReading resume...")

resume_text = extract_resume_text(resume_file)

if not resume_text:
    print("ERROR: Resume text could not be extracted.")
    exit()

print("Resume extracted successfully.")


# ============================================================
# EXTRACT SKILLS
# ============================================================

resume_skills = extract_skills(resume_text)

print("Resume skills extracted successfully.")


# ============================================================
# CALCULATE SCORE
# ============================================================

result = calculate_final_score(
    resume_text,
    job_description,
    resume_skills
)


# ============================================================
# EVALUATION
# ============================================================

evaluation = evaluate_candidate(result)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n==============================")
print("AUTOMATIC RESUME SCREENING")
print("==============================")


print("\nREQUIRED SKILLS:")

for skill in result["required_skills"]:
    print("✓", skill)


print("\nPREFERRED SKILLS:")

for skill in result["preferred_skills"]:
    print("✓", skill)


print("\nMATCHED SKILLS:")

if result["matched_skills"]:
    for skill in result["matched_skills"]:
        print("✓", skill)
else:
    print("None")


print("\nMISSING REQUIRED SKILLS:")

if result["missing_skills"]:
    for skill in result["missing_skills"]:
        print("✗", skill)
else:
    print("None")


print("\nMATCHED KEYWORDS:")

if result["matched_keywords"]:
    for keyword in result["matched_keywords"]:
        print("✓", keyword)
else:
    print("None")


print("\nMISSING KEYWORDS:")

if result["missing_keywords"]:
    for keyword in result["missing_keywords"]:
        print("✗", keyword)
else:
    print("None")


# ============================================================
# EXPERIENCE & EDUCATION
# ============================================================

print("\n==============================")
print("EXPERIENCE & EDUCATION")
print("==============================")

print(
    "Experience:",
    result["experience_years"],
    "years"
)

print(
    "Required Experience:",
    result["required_years"],
    "years"
)

print(
    "Education:",
    result["education_level"]
)

print(
    "Required Education:",
    result["required_education_level"]
)


# ============================================================
# SCORING
# ============================================================

print("\n==============================")
print("SCORING")
print("==============================")

print(
    "Required Skill Score:",
    result["required_score"],
    "%"
)

print(
    "Preferred Skill Score:",
    result["preferred_score"],
    "%"
)

print(
    "Keyword Match Score:",
    result["keyword_score"],
    "%"
)

print(
    "TF-IDF Match:",
    result["tfidf_score"],
    "%"
)

print(
    "Experience Score:",
    result["experience_score"],
    "%"
)

print(
    "Education Score:",
    result["education_score"],
    "%"
)

print(
    "FINAL SCORE:",
    result["final_score"],
    "%"
)

print("==============================")


# ============================================================
# CANDIDATE EVALUATION
# ============================================================

print("\n==============================")
print("CANDIDATE EVALUATION")
print("==============================")

print(
    "\nFinal Score:",
    result["final_score"],
    "%"
)

print(
    "Recommendation:",
    evaluation["recommendation"]
)


print("\nStrengths:")

for strength in evaluation["strengths"]:
    print("✓", strength)


print("\nAreas to Improve:")

for area in evaluation["areas_to_improve"]:
    print("•", area)


print("\n==============================")
print("SCREENING COMPLETE")
print("==============================")