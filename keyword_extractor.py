# ============================================================
# keyword_extractor.py
# Robust ATS keyword extraction and weighted matching
#
# Designed to work with:
#   - skills.py
#   - skill_extractor.py
#   - ranker.py
#
# Responsibilities:
#   1. Normalize aliases
#   2. Extract known ATS phrases
#   3. Extract meaningful keywords
#   4. Calculate weighted exact keyword score
#   5. Report matched and missing keywords
#
# IMPORTANT:
# This module performs EXACT / canonical keyword matching.
# Related-skill similarity belongs in ranker.py.
# ============================================================

import re

from skills import (
    SKILLS,
    SKILL_ALIASES,
    ATS_KEYWORDS,
)


# ============================================================
# EXTRA ALIASES
#
# Only aliases that are NOT already present in skills.py.
# ============================================================

EXTRA_ALIASES = {

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    "a i": "artificial intelligence",
    "a.i": "artificial intelligence",
    "a.i.": "artificial intelligence",

    "m l": "machine learning",
    "m.l": "machine learning",
    "m.l.": "machine learning",

    "gen ai": "generative ai",
    "genai": "generative ai",
    "generative artificial intelligence": "generative ai",

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    "llm": "large language model",
    "llms": "large language model",
    "large-language-model": "large language model",
    "large-language-models": "large language model",

    # --------------------------------------------------------
    # TECHNICAL VARIANTS
    # --------------------------------------------------------

    "my sql": "mysql",
    "postgre sql": "postgresql",
    "mongo db": "mongodb",

    "nodejs": "node.js",
    "node js": "node.js",

    "expressjs": "express.js",
    "express js": "express.js",

    "nextjs": "next.js",
    "next js": "next.js",

    "restful api": "rest api",
    "restful apis": "rest api",
    "rest apis": "rest api",

    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    "data quality check": "data quality",
    "data quality checks": "data quality",
    "data quality checking": "data quality",

    # --------------------------------------------------------
    # QUALITY
    # --------------------------------------------------------

    "quality check": "quality assurance",
    "quality checks": "quality assurance",
    "quality checking": "quality assurance",

    "qa": "quality assurance",
    "q a": "quality assurance",

    "qc": "quality control",
    "q c": "quality control",

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    "statistical analysis": "statistics",
    "statistical analytics": "statistics",

}


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {

    "the", "and", "or", "but", "for", "with",
    "from", "this", "that", "are", "was", "were",
    "will", "have", "has", "had", "been", "being",

    "you", "your", "our", "their", "they", "them",

    "who", "what", "when", "where", "how", "why",

    "a", "an", "to", "of", "in", "on", "at", "by",
    "as", "is", "it", "be", "we", "can", "should",
    "must", "may", "not", "all", "any", "such",

    "candidate", "candidates",
    "job", "jobs",
    "role", "roles",
    "position", "positions",

    "experience",
    "experiences",

    "skill", "skills",

    "required",
    "preferred",

    "looking",

    "years",
    "year",

    "team",
    "teams",

    "responsibilities",
    "responsibility",

    "knowledge",

    "ability",
    "abilities",

    "company",
    "organization",
    "organizations",

    "department",
    "departments",

    "environment",

    "professional",
    "professionals",

    "also",

    "work",
    "working",
    "works",

    # --------------------------------------------------------
    # Common verbs
    # --------------------------------------------------------

    "able",
    "effectively",

    "maintain",
    "maintained",
    "maintaining",

    "follow",
    "following",

    "meet",
    "meets",
    "meeting",

    "perform",
    "performed",
    "performing",

    "provide",
    "provided",
    "providing",

    "ensure",
    "ensured",
    "ensuring",

    "using",
    "used",
    "use",

    "include",
    "including",

    "develop",
    "developed",
    "developing",

    "manage",
    "managed",
    "managing",

    "responsible",
    "responsibly",

}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Normalize text for ATS matching.

    Does NOT calculate experience.
    Does NOT perform semantic matching.
    """

    if not text:
        return ""

    text = str(text).lower()

    replacements = {
        "–": "-",
        "—": "-",
        "−": "-",
        "•": " ",
        "&": " and ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # --------------------------------------------------------
    # Preserve slash when it is part of a known technical term
    # such as CI/CD.
    # --------------------------------------------------------

    text = re.sub(
        r"[^a-z0-9+#./\s-]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


# ============================================================
# BUILD ALIAS MAP
# ============================================================

def get_alias_map():
    """
    Build normalized alias -> canonical mapping.

    SKILL_ALIASES from skills.py is the primary source.
    EXTRA_ALIASES adds only missing robust forms.
    """

    aliases = {}

    for alias, canonical in SKILL_ALIASES.items():

        alias_clean = clean_text(alias)
        canonical_clean = clean_text(canonical)

        if alias_clean and canonical_clean:
            aliases[alias_clean] = canonical_clean

    for alias, canonical in EXTRA_ALIASES.items():

        alias_clean = clean_text(alias)
        canonical_clean = clean_text(canonical)

        if alias_clean and canonical_clean:
            aliases[alias_clean] = canonical_clean

    return aliases


# ============================================================
# CANONICALIZE SINGLE TERM
# ============================================================

def canonicalize_term(term):
    """
    Convert one term/alias into canonical form.

    No recursive alias chaining.
    """

    term = clean_text(term)

    if not term:
        return ""

    aliases = get_alias_map()

    return aliases.get(
        term,
        term,
    )


# ============================================================
# APPLY ALIASES
# ============================================================

def apply_aliases(text):
    """
    Replace aliases with canonical forms.

    Longest aliases are processed first.

    Canonical terms already present in the text are protected,
    preventing alias collisions.

    Examples:

        Microsoft Excel -> excel
        PowerBI -> power bi
        My SQL -> mysql
        ML -> machine learning

    SQL does NOT match inside MySQL.
    """

    text = clean_text(text)

    if not text:
        return ""

    aliases = get_alias_map()

    sorted_aliases = sorted(
        aliases.items(),
        key=lambda item: (
            -len(item[0].split()),
            -len(item[0]),
        ),
    )

    # --------------------------------------------------------
    # Protect canonical terms already present.
    # --------------------------------------------------------

    canonical_terms = set()

    for skill in SKILLS:

        normalized = clean_text(skill)

        if normalized:
            canonical_terms.add(normalized)

    for keyword in ATS_KEYWORDS:

        normalized = clean_text(keyword)

        if normalized:
            canonical_terms.add(normalized)

    # --------------------------------------------------------
    # Protect longer phrases first.
    # --------------------------------------------------------

    canonical_terms = sorted(
        canonical_terms,
        key=lambda value: (
            -len(value.split()),
            -len(value),
        ),
    )

    protected = {}
    counter = 0

    for canonical in canonical_terms:

        pattern = (
            r"(?<!\w)"
            + re.escape(canonical)
            + r"(?!\w)"
        )

        if not re.search(
            pattern,
            text,
        ):
            continue

        placeholder = (
            f"__ATS_CANONICAL_{counter}__"
        )

        counter += 1

        protected[placeholder] = canonical

        text = re.sub(
            pattern,
            placeholder,
            text,
        )

    # --------------------------------------------------------
    # Apply aliases.
    # --------------------------------------------------------

    for alias, canonical in sorted_aliases:

        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if not re.search(
            pattern,
            text,
        ):
            continue

        placeholder = (
            f"__ATS_ALIAS_{counter}__"
        )

        counter += 1

        protected[placeholder] = canonical

        text = re.sub(
            pattern,
            placeholder,
            text,
        )

    # --------------------------------------------------------
    # Restore.
    # --------------------------------------------------------

    for placeholder, canonical in protected.items():

        text = text.replace(
            placeholder,
            canonical,
        )

    return text


# ============================================================
# NORMALIZE WORD
# ============================================================

def normalize_word(word):
    """
    Normalize common plural forms.

    Short technical terms such as:
        C
        R
        Go

    are intentionally NOT handled here.
    They are handled separately by known technical terms.
    """

    word = str(word).lower().strip()

    if not word:
        return ""

    word = word.strip(
        ".,;:!?()[]{}\"'"
    )

    if not word:
        return ""

    irregular = {

        "datasets": "dataset",
        "projects": "project",
        "tasks": "task",
        "targets": "target",
        "guidelines": "guideline",
        "requirements": "requirement",
        "models": "model",
        "annotations": "annotation",
        "benchmarks": "benchmark",
        "images": "image",
        "texts": "text",
        "reports": "report",
        "dashboards": "dashboard",
        "databases": "database",

        "issues": "issue",
        "procedures": "procedure",
        "processes": "process",

    }

    if word in irregular:
        return irregular[word]

    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"

    if len(word) > 4 and word.endswith("sses"):
        return word[:-2]

    if len(word) > 4 and word.endswith("es"):
        return word[:-2]

    if len(word) > 3 and word.endswith("s"):
        return word[:-1]

    return word


# ============================================================
# KNOWN PHRASES
# ============================================================

def get_known_phrases():
    """
    Return known multi-word ATS phrases.

    Longest phrases are returned first.
    """

    phrases = set()

    for skill in SKILLS:

        normalized = clean_text(skill)

        if " " in normalized:
            phrases.add(normalized)

    for alias, canonical in SKILL_ALIASES.items():

        alias_clean = clean_text(alias)
        canonical_clean = clean_text(canonical)

        if " " in alias_clean:
            phrases.add(canonical_clean)

    for alias, canonical in EXTRA_ALIASES.items():

        alias_clean = clean_text(alias)
        canonical_clean = clean_text(canonical)

        if " " in alias_clean:
            phrases.add(canonical_clean)

    for keyword in ATS_KEYWORDS:

        normalized = clean_text(keyword)

        if " " in normalized:
            phrases.add(normalized)

    return sorted(
        phrases,
        key=lambda phrase: (
            -len(phrase.split()),
            -len(phrase),
        ),
    )


# ============================================================
# KNOWN SINGLE-WORD TECHNICAL TERMS
# ============================================================

def get_known_single_terms():
    """
    Return single-word canonical skills/ATS keywords.

    This is important for:
        C
        R
        Go

    which must not be removed simply because they are short.
    """

    terms = set()

    for skill in SKILLS:

        normalized = clean_text(skill)

        if (
            normalized
            and " " not in normalized
        ):
            terms.add(normalized)

    for keyword in ATS_KEYWORDS:

        normalized = clean_text(keyword)

        if (
            normalized
            and " " not in normalized
        ):
            terms.add(normalized)

    return terms


# ============================================================
# EXTRACT KEYWORDS
# ============================================================

def extract_keywords(text):
    """
    Extract meaningful ATS keywords.

    Returns:
        set[str]

    Strategy:
        1. Normalize aliases
        2. Extract known phrases
        3. Extract known technical single terms
        4. Extract useful remaining words
    """

    text = apply_aliases(text)

    if not text:
        return set()

    keywords = set()

    remaining_text = text

    # ========================================================
    # PHRASES FIRST
    # ========================================================

    phrases = get_known_phrases()

    for index, phrase in enumerate(phrases):

        pattern = (
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)"
        )

        if not re.search(
            pattern,
            remaining_text,
        ):
            continue

        keywords.add(phrase)

        placeholder = (
            f"__ATS_PHRASE_{index}__"
        )

        remaining_text = re.sub(
            pattern,
            f" {placeholder} ",
            remaining_text,
        )

    # ========================================================
    # KNOWN SINGLE-WORD TERMS
    # ========================================================

    known_terms = get_known_single_terms()

    for term in sorted(
        known_terms,
        key=lambda value: (
            -len(value),
            value,
        ),
    ):

        pattern = (
            r"(?<!\w)"
            + re.escape(term)
            + r"(?!\w)"
        )

        if not re.search(
            pattern,
            remaining_text,
        ):
            continue

        keywords.add(term)

        remaining_text = re.sub(
            pattern,
            " ",
            remaining_text,
        )

    # ========================================================
    # REMAINING WORDS
    # ========================================================

    for word in remaining_text.split():

        if word.startswith("__ATS_PHRASE_"):
            continue

        word = normalize_word(word)

        if not word:
            continue

        # Ignore very short ordinary words.
        if len(word) <= 2:
            continue

        if word in STOP_WORDS:
            continue

        keywords.add(word)

    return keywords


# ============================================================
# CANONICALIZE KEYWORD SET
# ============================================================

def _canonicalize_keywords(keywords):
    """
    Convert extracted keywords into canonical forms.
    """

    canonical_keywords = set()

    for keyword in keywords:

        if not keyword:
            continue

        canonical = canonicalize_term(
            keyword
        )

        if canonical:
            canonical_keywords.add(
                canonical
            )

    return canonical_keywords


# ============================================================
# NORMALIZED ATS KEYWORDS
# ============================================================

def _get_normalized_ats_keywords():
    """
    Return ATS weights using canonical keyword names.
    """

    normalized = {}

    for keyword, weight in ATS_KEYWORDS.items():

        canonical = canonicalize_term(
            keyword
        )

        if not canonical:
            continue

        # Keep highest weight if aliases
        # collapse into same canonical term.
        normalized[canonical] = max(
            normalized.get(canonical, 0.0),
            float(weight),
        )

    return normalized


# ============================================================
# KEYWORD WEIGHT
# ============================================================

def get_keyword_weight(keyword):
    """
    Return ATS weight.

    Priority:

        1. ATS keyword
        2. Canonical ATS keyword
        3. Known skill
        4. Ordinary keyword
    """

    normalized = clean_text(
        keyword
    )

    if not normalized:
        return 0.0

    ats_keywords = (
        _get_normalized_ats_keywords()
    )

    # Direct ATS keyword.
    if normalized in ATS_KEYWORDS:

        return float(
            ATS_KEYWORDS[normalized]
        )

    canonical = canonicalize_term(
        normalized
    )

    # Canonical ATS keyword.
    if canonical in ats_keywords:

        return float(
            ats_keywords[canonical]
        )

    # Known canonical skill.
    canonical_skills = {
        clean_text(skill)
        for skill in SKILLS
        if skill
    }

    if canonical in canonical_skills:

        return 3.0

    # Ordinary extracted word.
    return 1.0


# ============================================================
# CALCULATE WEIGHTED KEYWORD SCORE
# ============================================================

def calculate_keyword_score(
    resume_text,
    job_description,
):
    """
    Calculate weighted exact keyword similarity.

    Returns:
        float from 0 to 100.

    Important:
        This does NOT use RELATED_SKILLS.

    Example:

        JD: MySQL
        Resume: SQL

        Result:
            MySQL is NOT an exact match.

    ranker.py can later give partial credit
    through RELATED_SKILLS.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    if not job_keywords:
        return 0.0

    resume_canonical = (
        _canonicalize_keywords(
            resume_keywords
        )
    )

    total_weight = 0.0
    matched_weight = 0.0

    for keyword in job_keywords:

        weight = get_keyword_weight(
            keyword
        )

        if weight <= 0:
            continue

        total_weight += weight

        canonical = canonicalize_term(
            keyword
        )

        if (
            keyword in resume_keywords
            or canonical in resume_canonical
        ):
            matched_weight += weight

    if total_weight <= 0:
        return 0.0

    score = (
        matched_weight
        / total_weight
    ) * 100.0

    return round(
        min(
            max(score, 0.0),
            100.0
        ),
        2,
    )


# ============================================================
# MATCHED KEYWORDS
# ============================================================

def get_matched_keywords(
    resume_text,
    job_description,
):
    """
    Return exact/canonical keywords appearing
    in both resume and JD.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    resume_canonical = (
        _canonicalize_keywords(
            resume_keywords
        )
    )

    matched = []

    for keyword in job_keywords:

        canonical = canonicalize_term(
            keyword
        )

        if (
            keyword in resume_keywords
            or canonical in resume_canonical
        ):
            matched.append(keyword)

    return sorted(
        set(matched),
        key=lambda keyword: (
            -get_keyword_weight(keyword),
            keyword,
        ),
    )


# ============================================================
# MISSING KEYWORDS
# ============================================================

def get_missing_keywords(
    resume_text,
    job_description,
):
    """
    Return important JD keywords missing
    from the resume.

    Only keywords with weight >= 2.0
    are reported.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    resume_canonical = (
        _canonicalize_keywords(
            resume_keywords
        )
    )

    missing = []

    for keyword in job_keywords:

        canonical = canonicalize_term(
            keyword
        )

        if (
            keyword in resume_keywords
            or canonical in resume_canonical
        ):
            continue

        weight = get_keyword_weight(
            keyword
        )

        if weight >= 2.0:
            missing.append(keyword)

    return sorted(
        set(missing),
        key=lambda keyword: (
            -get_keyword_weight(keyword),
            keyword,
        ),
    )


# ============================================================
# KEYWORD MATCH DETAILS
# ============================================================

def get_keyword_match_details(
    resume_text,
    job_description,
):
    """
    Return detailed keyword matching information.
    """

    matched = get_matched_keywords(
        resume_text,
        job_description,
    )

    missing = get_missing_keywords(
        resume_text,
        job_description,
    )

    return {

        "matched": [
            {
                "keyword": keyword,
                "weight": get_keyword_weight(
                    keyword
                ),
            }
            for keyword in matched
        ],

        "missing": [
            {
                "keyword": keyword,
                "weight": get_keyword_weight(
                    keyword
                ),
            }
            for keyword in missing
        ],
    }


# ============================================================
# CHECK KEYWORD PRESENCE
# ============================================================

def check_keyword_presence(
    resume_text,
    keyword,
):
    """
    Check whether a keyword or alias exists
    in the resume.
    """

    normalized_keyword = canonicalize_term(
        keyword
    )

    if not normalized_keyword:
        return False

    resume_keywords = extract_keywords(
        resume_text
    )

    resume_canonical = (
        _canonicalize_keywords(
            resume_keywords
        )
    )

    return (
        normalized_keyword
        in resume_canonical
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    resume = """
    Python SQL Excel Pandas

    Worked on data analysis,
    data cleaning and data validation.

    Performed data quality checks.

    Prepared reports and documentation.

    Strong communication,
    problem solving,
    attention to detail
    and analytical thinking.

    Power BI Tableau MySQL Statistics.
    """

    jd = """
    Required Skills:

    Data Analysis
    Microsoft Excel
    SQL
    Data Cleaning
    Data Validation
    Data Quality
    Reporting
    Documentation
    Communication
    Attention to Detail
    Analytical Thinking
    Problem Solving

    Preferred Skills:

    Python
    Pandas
    Power BI
    Tableau
    MySQL
    Statistics
    """

    print()
    print("=" * 60)
    print("KEYWORD EXTRACTOR TEST")
    print("=" * 60)

    print(
        "Keyword Score:",
        calculate_keyword_score(
            resume,
            jd,
        ),
        "%",
    )

    print()
    print("Matched:")

    for keyword in get_matched_keywords(
        resume,
        jd,
    ):

        print(
            "✓",
            keyword,
            "weight=",
            get_keyword_weight(
                keyword
            ),
        )

    print()
    print("Missing:")

    for keyword in get_missing_keywords(
        resume,
        jd,
    ):

        print(
            "✗",
            keyword,
            "weight=",
            get_keyword_weight(
                keyword
            ),
        )

    print("=" * 60)