import re

from skill_extractor import extract_skills


# ============================================================
# SECTION DETECTION
# ============================================================

REQUIRED_HEADERS = {

    "required skills",
    "required skill",
    "requirements",
    "required qualifications",
    "required qualification",
    "must have",
    "must-have",
    "essential skills",
    "essential qualifications",
    "core skills",
    "mandatory skills",
    "mandatory qualifications"
}


PREFERRED_HEADERS = {

    "preferred skills",
    "preferred skill",
    "preferred qualifications",
    "preferred qualification",
    "nice to have",
    "nice-to-have",
    "desired skills",
    "desired qualifications",
    "bonus skills",
    "additional skills"
}


# ============================================================
# NORMALIZE HEADER
# ============================================================

def normalize_header(text):

    text = text.lower().strip()

    text = re.sub(
        r"^[#*\-\d\.\)\s]+",
        "",
        text
    )

    text = re.sub(
        r"[:]+$",
        "",
        text
    )

    return text.strip()


# ============================================================
# DETECT HEADER
# ============================================================

def detect_section(line):

    normalized = normalize_header(
        line
    )

    if normalized in REQUIRED_HEADERS:

        return "required"

    if normalized in PREFERRED_HEADERS:

        return "preferred"

    # Flexible matching for headings such as:
    #
    # Required Skills:
    # Required Skills
    # REQUIRED SKILLS
    #
    if (
        "required skills" in normalized
        or
        "required qualifications" in normalized
    ):

        return "required"

    if (
        "preferred skills" in normalized
        or
        "preferred qualifications" in normalized
    ):

        return "preferred"

    return None


# ============================================================
# ANALYZE JOB DESCRIPTION
# ============================================================

def analyze_job_description(
    job_description
):

    if not job_description:

        return {
            "required_skills": [],
            "preferred_skills": []
        }

    lines = job_description.splitlines()

    required_text = []
    preferred_text = []

    section = None

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        detected_section = detect_section(
            stripped
        )

        if detected_section:

            section = detected_section

            continue

        # ----------------------------------------------------
        # Detect when a new major section starts.
        # ----------------------------------------------------

        lower = stripped.lower()

        major_sections = (
            "about the role",
            "key responsibilities",
            "responsibilities",
            "performance expectations",
            "experience requirements",
            "experience",
            "education",
            "benefits",
            "salary",
            "location"
        )

        if any(
            lower.startswith(section_name)
            for section_name in major_sections
        ):

            section = None

        # ----------------------------------------------------
        # Store content
        # ----------------------------------------------------

        if section == "required":

            required_text.append(
                stripped
            )

        elif section == "preferred":

            preferred_text.append(
                stripped
            )

    # ========================================================
    # EXTRACT SKILLS
    # ========================================================

    required_skills = extract_skills(
        " ".join(required_text)
    )

    preferred_skills = extract_skills(
        " ".join(preferred_text)
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    required_skills = list(
        dict.fromkeys(
            required_skills
        )
    )

    preferred_skills = list(
        dict.fromkeys(
            preferred_skills
        )
    )

    # --------------------------------------------------------
    # A skill should not be both required and preferred.
    # Required takes priority.
    # --------------------------------------------------------

    required_set = set(
        required_skills
    )

    preferred_skills = [
        skill
        for skill in preferred_skills
        if skill not in required_set
    ]

    return {

        "required_skills":
            sorted(required_skills),

        "preferred_skills":
            sorted(preferred_skills)
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_jd = """

    Job Title: Junior Data Analyst

    Required Skills:
    Data Analysis
    Microsoft Excel
    SQL
    Data Cleaning
    Data Validation
    Reporting
    Communication
    Attention to Detail
    Analytical Thinking
    Problem Solving

    Preferred Skills:
    Python
    Power BI
    Tableau
    Data Visualization
    Statistics
    MySQL
    Microsoft PowerPoint

    """

    result = analyze_job_description(
        sample_jd
    )

    print(
        "Required Skills:"
    )

    for skill in result[
        "required_skills"
    ]:

        print(
            "✓",
            skill
        )

    print(
        "\nPreferred Skills:"
    )

    for skill in result[
        "preferred_skills"
    ]:

        print(
            "✓",
            skill
        )