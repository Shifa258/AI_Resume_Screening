# ============================================================
# skill_extractor.py
# Robust ATS Skill Extraction Engine
#
# Works with:
#   - skills.py
#   - ranker.py
#
# Features:
#   - Canonical skill matching
#   - Alias support
#   - Longest-first phrase matching
#   - Prevents fragmented skills
#   - Handles C++ / C#
#   - Handles short skills such as C / R safely
#   - Handles hyphenated skills
#   - Handles explicit Required / Preferred sections
#   - Handles inline section headings
#   - Does NOT reject legitimate canonical skills
# ============================================================

import re

from skills import (
    SKILLS,
    SKILL_ALIASES,
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text for reliable skill matching.

    Examples:

        Microsoft Excel -> microsoft excel
        Power-BI        -> power bi
        Data-Analysis   -> data analysis
        C++             -> c++
        C#              -> c#

    Important:
    This function is only for skill matching.
    It does not calculate experience dates.
    """

    if not text:
        return ""

    text = str(text).lower()

    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2022": " ",
        "\u25cf": " ",
        "\u25aa": " ",
        "\u25e6": " ",
        "\u00a0": " ",
        "/": " ",
        "&": " and ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Keep:
    # letters
    # numbers
    # +
    # #
    # .
    # -
    # spaces

    text = re.sub(
        r"[^a-z0-9+#.\s-]",
        " ",
        text,
    )

    # Treat hyphen as a separator.
    #
    # data-analysis -> data analysis
    # quality-control -> quality control

    text = text.replace(
        "-",
        " ",
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# NORMALIZED SKILL MAP
# ============================================================

def _build_alias_map():
    """
    Build a normalized alias -> canonical skill map.

    This is created dynamically so skills.py remains
    the single source of truth.
    """

    alias_map = {}

    for alias, canonical in SKILL_ALIASES.items():

        alias_normalized = normalize_text(
            alias
        )

        canonical_normalized = normalize_text(
            canonical
        )

        if not alias_normalized:
            continue

        if not canonical_normalized:
            continue

        alias_map[
            alias_normalized
        ] = canonical_normalized

    return alias_map


# ============================================================
# CANONICALIZATION
# ============================================================

def canonicalize_skill(skill):
    """
    Convert any supported skill/alias into its canonical form.

    Examples:

        MS Excel
            -> excel

        PowerBI
            -> power bi

        ML
            -> machine learning

        Data Cleansing
            -> data cleaning
    """

    normalized = normalize_text(
        skill
    )

    if not normalized:
        return ""

    alias_map = _build_alias_map()

    # Exact alias match.
    if normalized in alias_map:

        return alias_map[
            normalized
        ]

    # Exact canonical skill.
    canonical_skills = {
        normalize_text(skill)
        for skill in SKILLS
        if skill
    }

    if normalized in canonical_skills:

        return normalized

    # No known alias.
    #
    # Returning the normalized value allows ranker.py
    # to perform final validation.
    return normalized


# ============================================================
# BUILD SKILL PATTERNS
# ============================================================

def build_skill_patterns():
    """
    Build searchable patterns for:

        1. Canonical skills
        2. Skill aliases

    Every pattern maps to exactly one canonical skill.
    """

    patterns = {}

    # --------------------------------------------------------
    # Canonical skills
    # --------------------------------------------------------

    for skill in SKILLS:

        if not skill:
            continue

        normalized = normalize_text(
            skill
        )

        if not normalized:
            continue

        canonical = canonicalize_skill(
            skill
        )

        if not canonical:
            continue

        patterns[
            normalized
        ] = canonical

    # --------------------------------------------------------
    # Aliases
    # --------------------------------------------------------

    for alias, canonical in SKILL_ALIASES.items():

        alias_normalized = normalize_text(
            alias
        )

        canonical_normalized = canonicalize_skill(
            canonical
        )

        if not alias_normalized:
            continue

        if not canonical_normalized:
            continue

        patterns[
            alias_normalized
        ] = canonical_normalized

    return patterns


# ============================================================
# VALID SEARCH PHRASE
# ============================================================

def _is_valid_skill_phrase(
    phrase,
    canonical,
):
    """
    Prevent obviously dangerous fragments from becoming
    standalone skills.

    Important:
    A word is NOT rejected merely because it appears in the
    generic-fragment list if that word is itself a legitimate
    canonical skill.

    Examples:

        analysis       -> rejected
        validation     -> rejected
        cleaning       -> rejected
        communication  -> accepted
        database       -> accepted
        dataset        -> accepted
        documentation  -> accepted
    """

    if not phrase or not canonical:
        return False

    generic_fragments = {
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
        "project",
        "projects",
        "task",
        "tasks",
        "model",
        "models",
        "image",
        "images",
        "text",
        "texts",
        "databases",
        "datasets",
    }

    # --------------------------------------------------------
    # Legitimate canonical skills are allowed.
    # --------------------------------------------------------

    canonical_skills = {
        normalize_text(skill)
        for skill in SKILLS
        if skill
    }

    if phrase in canonical_skills:
        return True

    if canonical in canonical_skills:
        return True

    # --------------------------------------------------------
    # Reject dangerous generic fragments.
    # --------------------------------------------------------

    if phrase in generic_fragments:
        return False

    if canonical in generic_fragments:
        return False

    return True


# ============================================================
# PHRASE MATCH
# ============================================================

def _phrase_exists(
    text,
    phrase,
):
    """
    Boundary-safe phrase matching.

    Handles normal skills and special programming-language
    skills such as:

        C
        C++
        C#

    Examples:

        java       -> does not match javascript
        sql        -> does not match mysql
        c          -> does not match c++
        c          -> does not match c#
        r          -> only matches standalone R
    """

    if not text or not phrase:
        return False

    # --------------------------------------------------------
    # Special handling for C
    #
    # C++ and C# must not also produce C.
    # --------------------------------------------------------

    if phrase == "c":

        pattern = (
            r"(?<![\w+#])"
            r"c"
            r"(?![\w+#])"
        )

    # --------------------------------------------------------
    # Special handling for C++
    # --------------------------------------------------------

    elif phrase == "c++":

        pattern = (
            r"(?<![\w+#])"
            r"c\+\+"
            r"(?![\w+#])"
        )

    # --------------------------------------------------------
    # Special handling for C#
    # --------------------------------------------------------

    elif phrase == "c#":

        pattern = (
            r"(?<![\w+#])"
            r"c\#"
            r"(?![\w+#])"
        )

    # --------------------------------------------------------
    # Special handling for R
    #
    # Prevent matching inside normal words.
    # --------------------------------------------------------

    elif phrase == "r":

        pattern = (
            r"(?<!\w)"
            r"r"
            r"(?!\w)"
        )

    # --------------------------------------------------------
    # Normal phrase matching.
    # --------------------------------------------------------

    else:

        pattern = (
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)"
        )

    return bool(
        re.search(
            pattern,
            text,
        )
    )


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    """
    Extract canonical skills from text.

    Longest phrases are checked first.

    Example:

        "data analysis and data visualization"

    becomes:

        [
            "data analysis",
            "data visualization"
        ]

    rather than:

        analysis
        visualization
    """

    normalized = normalize_text(
        text
    )

    if not normalized:
        return []

    skill_patterns = (
        build_skill_patterns()
    )

    found = set()

    # --------------------------------------------------------
    # Longest phrases first.
    #
    # Multi-word skills are checked before shorter fragments.
    # --------------------------------------------------------

    ordered_patterns = sorted(
        skill_patterns.items(),
        key=lambda item: (
            -len(item[0].split()),
            -len(item[0]),
        ),
    )

    for phrase, canonical in ordered_patterns:

        if not _is_valid_skill_phrase(
            phrase,
            canonical,
        ):
            continue

        if _phrase_exists(
            normalized,
            phrase,
        ):

            found.add(
                canonical
            )

    return sorted(
        found
    )


# ============================================================
# SKILL MATCH DETAILS
# ============================================================

def get_skill_match_details(
    resume_text,
    job_skills,
):
    """
    Compare resume skills against supplied job skills.

    Returns:

        {
            "exact": [...],
            "missing": [...]
        }
    """

    resume_skills = {
        canonicalize_skill(skill)
        for skill in extract_skills(
            resume_text
        )
    }

    resume_skills.discard("")

    exact = set()
    missing = set()

    for skill in job_skills or []:

        canonical = canonicalize_skill(
            skill
        )

        if not canonical:
            continue

        if canonical in resume_skills:

            exact.add(
                canonical
            )

        else:

            missing.add(
                canonical
            )

    return {
        "exact": sorted(exact),
        "missing": sorted(missing),
    }


# ============================================================
# HEADER NORMALIZATION
# ============================================================

def _normalize_header(line):
    """
    Normalize a possible JD section heading.

    This function is intended for checking whether the entire
    line is a section heading.

    Examples:

        Required Skills
            -> required skills

        Required Skills:
            -> required skills
    """

    line = normalize_text(
        line
    )

    line = line.lstrip(
        "-*• "
    )

    line = line.rstrip(
        ":"
    )

    return line.strip()


# ============================================================
# INLINE HEADER DETECTION
# ============================================================

def _extract_inline_section(
    line,
    headers,
):
    """
    Detect an inline section heading.

    Examples:

        Required Skills: Python, SQL
        Preferred Skills: Power BI, Tableau

    Returns:

        content

    or:

        None
    """

    if not line:
        return None

    # --------------------------------------------------------
    # Normalize the line while deliberately preserving the
    # colon needed to detect the heading/content boundary.
    # --------------------------------------------------------

    text = str(line).lower()

    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2022": " ",
        "\u25cf": " ",
        "\u25aa": " ",
        "\u25e6": " ",
        "\u00a0": " ",
        "/": " ",
        "&": " and ",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new,
        )

    text = re.sub(
        r"[^a-z0-9+#.\s:-]",
        " ",
        text,
    )

    text = text.replace(
        "-",
        " ",
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    # --------------------------------------------------------
    # Check longest headers first.
    # --------------------------------------------------------

    ordered_headers = sorted(
        headers,
        key=lambda value: (
            -len(value.split()),
            -len(value),
        ),
    )

    for section_header in ordered_headers:

        header_normalized = normalize_text(
            section_header
        )

        if not header_normalized:
            continue

        pattern = (
            r"^"
            + re.escape(header_normalized)
            + r"\s*:\s*"
        )

        match = re.match(
            pattern,
            text,
        )

        if match:

            content = text[
                match.end():
            ].strip()

            return content

    return None


# ============================================================
# JOB SECTION PARSER
# ============================================================

def extract_job_sections(
    job_description
):
    """
    Extract required and preferred portions of a job
    description.

    Supports headings such as:

        Required Skills
        Requirements
        Must Have
        Essential Skills

        Preferred Skills
        Nice to Have
        Good to Have
        Desirable Skills

    Also supports inline headings such as:

        Required Skills: Python, SQL
        Preferred Skills: Power BI, Tableau

    The parser intentionally stops at major sections such as:

        Responsibilities
        Education
        Experience
        Benefits
        Location
    """

    if not job_description:

        return {
            "required_skills": [],
            "preferred_skills": [],
        }

    lines = str(
        job_description
    ).splitlines()

    required_lines = []
    preferred_lines = []

    current_section = None

    # --------------------------------------------------------
    # Required headers
    # --------------------------------------------------------

    required_headers = {
        "required skills",
        "required qualifications",
        "requirements",
        "job requirements",
        "required",
        "must have",
        "mandatory skills",
        "essential skills",
        "essential qualifications",
        "technical requirements",
        "core skills",
    }

    # --------------------------------------------------------
    # Preferred headers
    # --------------------------------------------------------

    preferred_headers = {
        "preferred skills",
        "preferred qualifications",
        "preferred",
        "nice to have",
        "good to have",
        "desirable skills",
        "desired skills",
        "bonus skills",
        "additional skills",
    }

    # --------------------------------------------------------
    # Stop headers
    # --------------------------------------------------------

    stop_headers = {
        "responsibilities",
        "responsibility",
        "key responsibilities",
        "roles and responsibilities",
        "duties",

        "education",
        "education requirements",
        "educational qualifications",
        "academic qualifications",

        "experience",
        "experience requirements",
        "work experience",
        "professional experience",

        "benefits",
        "salary",
        "location",

        "about the role",
        "about the company",
        "company overview",

        "job description",
        "job summary",
        "summary",
        "overview",

        "what you will do",
        "what you'll do",
        "what you will bring",
    }

    # --------------------------------------------------------
    # Process lines
    # --------------------------------------------------------

    for original_line in lines:

        line = (
            original_line
            .strip()
        )

        if not line:
            continue

        # ----------------------------------------------------
        # Inline Preferred header
        #
        # Example:
        #
        # Preferred Skills: Python, SQL
        # ----------------------------------------------------

        inline_preferred = (
            _extract_inline_section(
                line,
                preferred_headers,
            )
        )

        if inline_preferred is not None:

            if inline_preferred:

                preferred_lines.append(
                    inline_preferred
                )

            current_section = "preferred"

            continue

        # ----------------------------------------------------
        # Inline Required header
        #
        # Example:
        #
        # Required Skills: Python, SQL
        # ----------------------------------------------------

        inline_required = (
            _extract_inline_section(
                line,
                required_headers,
            )
        )

        if inline_required is not None:

            if inline_required:

                required_lines.append(
                    inline_required
                )

            current_section = "required"

            continue

        # ----------------------------------------------------
        # Normalize possible full-line header.
        # ----------------------------------------------------

        header = _normalize_header(
            line
        )

        # ----------------------------------------------------
        # Preferred full-line header.
        #
        # Preferred is checked before required so that
        # specific preferred headings are handled correctly.
        # ----------------------------------------------------

        if header in preferred_headers:

            current_section = "preferred"
            continue

        # ----------------------------------------------------
        # Required full-line header.
        # ----------------------------------------------------

        if header in required_headers:

            current_section = "required"
            continue

        # ----------------------------------------------------
        # Major section stop.
        # ----------------------------------------------------

        if header in stop_headers:

            current_section = None
            continue

        # ----------------------------------------------------
        # Collect current section.
        # ----------------------------------------------------

        if current_section == "required":

            required_lines.append(
                line
            )

        elif current_section == "preferred":

            preferred_lines.append(
                line
            )

    # --------------------------------------------------------
    # Extract skills.
    # --------------------------------------------------------

    required_text = " ".join(
        required_lines
    )

    preferred_text = " ".join(
        preferred_lines
    )

    required_skills = extract_skills(
        required_text
    )

    preferred_skills = extract_skills(
        preferred_text
    )

    # --------------------------------------------------------
    # Required always wins.
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
        "required_skills": sorted(
            set(required_skills)
        ),

        "preferred_skills": sorted(
            set(preferred_skills)
        ),
    }


# ============================================================
# JOB SKILL ANALYSIS
# ============================================================

def analyze_job_description(
    job_description
):
    """
    Analyze a complete JD.

    If explicit Required / Preferred sections exist,
    use them.

    If they do not exist, all detected skills are treated
    as required.
    """

    sections = extract_job_sections(
        job_description
    )

    required_skills = sections[
        "required_skills"
    ]

    preferred_skills = sections[
        "preferred_skills"
    ]

    # --------------------------------------------------------
    # No explicit sections detected.
    #
    # Treat skills found throughout the JD as required.
    # --------------------------------------------------------

    if (
        not required_skills
        and not preferred_skills
    ):

        all_skills = extract_skills(
            job_description
        )

        required_skills = all_skills

    # --------------------------------------------------------
    # If preferred exists but required doesn't,
    # recover other skills from the complete JD as required.
    # --------------------------------------------------------

    elif (
        not required_skills
        and preferred_skills
    ):

        all_skills = extract_skills(
            job_description
        )

        preferred_set = set(
            preferred_skills
        )

        required_skills = [
            skill
            for skill in all_skills
            if skill not in preferred_set
        ]

    # --------------------------------------------------------
    # Required always wins.
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
        "required_skills": sorted(
            set(required_skills)
        ),

        "preferred_skills": sorted(
            set(preferred_skills)
        ),
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    sample = """
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

    result = analyze_job_description(
        sample
    )

    print()
    print("=" * 60)
    print("SKILL EXTRACTOR TEST")
    print("=" * 60)

    print()
    print("REQUIRED SKILLS:")

    for skill in result[
        "required_skills"
    ]:

        print(
            "✓",
            skill,
        )

    print()
    print("PREFERRED SKILLS:")

    for skill in result[
        "preferred_skills"
    ]:

        print(
            "✓",
            skill,
        )

    print()
    print("DIRECT EXTRACTION TEST:")

    test_text = """
    Experience with Microsoft Excel,
    Power BI, Python, SQL, Data Analysis,
    Data Cleaning, Data Validation,
    Data Visualization and AI.
    """

    detected = extract_skills(
        test_text
    )

    for skill in detected:

        print(
            "✓",
            skill,
        )

    print()
    print("INLINE SECTION TEST:")

    inline_test = """
    Required Skills: Python, SQL, Excel, Data Analysis
    Preferred Skills: Power BI, Tableau, Pandas
    Responsibilities:
    Prepare reports and coordinate with teams.
    """

    inline_result = analyze_job_description(
        inline_test
    )

    print(
        "Required:",
        inline_result["required_skills"],
    )

    print(
        "Preferred:",
        inline_result["preferred_skills"],
    )

    print()
    print("C / C++ / C# TEST:")

    programming_tests = [
        "C",
        "C++",
        "C#",
        "C and C++",
        "C and C#",
        "C++ and C#",
    ]

    for test in programming_tests:

        print(
            test,
            "->",
            extract_skills(test),
        )

    print()
    print("R LANGUAGE TEST:")

    r_tests = [
        "R",
        "R programming",
        "Python and R",
        "reporting and research",
    ]

    for test in r_tests:

        print(
            test,
            "->",
            extract_skills(test),
        )

    print()
    print("CANONICAL SKILL TEST:")

    canonical_tests = [
        "Communication",
        "Database",
        "Dataset",
        "Documentation",
        "Quality",
        "Analysis",
        "Validation",
        "Cleaning",
        "Annotation",
    ]

    for test in canonical_tests:

        print(
            test,
            "->",
            extract_skills(test),
        )

    print()
    print("ALIAS TEST:")

    aliases_to_test = [
        "MS Excel",
        "PowerBI",
        "ML",
        "AI",
        "Sklearn",
        "My SQL",
        "Data Cleansing",
        "Quality Checking",
        "Team Work",
        "Problem-Solving",
    ]

    for alias in aliases_to_test:

        print(
            alias,
            "->",
            canonicalize_skill(alias),
        )

    print()
    print("=" * 60)