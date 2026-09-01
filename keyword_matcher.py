import re

from skills import SKILLS, SKILL_ALIASES


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    # Common English words
    "the", "and", "or", "but", "for", "with", "from",
    "this", "that", "are", "was", "were", "will", "have",
    "has", "had", "been", "being", "you", "your", "our",
    "their", "they", "them", "who", "what", "when", "where",
    "how", "why",

    "a", "an", "to", "of", "in", "on", "at", "by",
    "as", "is", "it", "be", "we", "can", "should",
    "must", "may", "not", "all", "any", "such",

    # Recruitment words
    "candidate", "candidates",
    "job", "jobs",
    "role", "roles",
    "position", "positions",
    "work", "working",
    "experience", "experiences",
    "skills", "skill",
    "required", "preferred",
    "looking",
    "years", "year",
    "team", "teams",
    "responsibilities", "responsibility",
    "knowledge",
    "ability", "abilities",

    # Generic action words
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
    "support",
    "supported",
    "supporting",
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

    # Generic business words
    "company",
    "organization",
    "organizations",
    "business",
    "businesses",
    "department",
    "departments",
    "environment",
    "professional",
    "professionals"
}


# ============================================================
# EXTRA ALIASES
# ============================================================

EXTRA_ALIASES = {

    # AI / ML
    "ai": "artificial intelligence",
    "a i": "artificial intelligence",
    "ml": "machine learning",
    "m l": "machine learning",

    # Microsoft Office
    "ms excel": "excel",
    "microsoft excel": "excel",

    "ms word": "word",
    "microsoft word": "word",

    "ms powerpoint": "powerpoint",
    "microsoft powerpoint": "powerpoint",

    "ms power point": "powerpoint",
    "power point": "powerpoint",

    # Problem solving
    "problem-solving": "problem solving",

    # Annotation
    "data labeling": "data annotation",
    "data labelling": "data annotation",

    "image labeling": "image annotation",
    "image labelling": "image annotation",

    "text labeling": "text annotation",
    "text labelling": "text annotation",

    "lidar data": "lidar annotation",

    # Quality
    "quality checking": "quality assurance",
    "quality check": "quality assurance",
    "quality checks": "quality assurance",

    # Plurals
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

    # Professional skills
    "team work": "teamwork",
    "team-work": "teamwork",

    "time-management": "time management",

    "project-management": "project management",

    "data-analysis": "data analysis",

    "data-science": "data science",

    "deep-learning": "deep learning",

    "computer-vision": "computer vision",

    "attention-to-detail": "attention to detail",

    # Technical variations
    "node.js": "node js",
    "nodejs": "node js",

    "restful api": "rest api",
    "rest apis": "rest api",

    "scikit-learn": "scikit learn",

    "power-bi": "power bi",

    "postgre sql": "postgresql",

    # Verb variations
    "annotating": "annotation",
    "annotated": "annotation",
    "annotate": "annotation",

    "labeling": "label",
    "labelling": "label",
    "labeled": "label",
    "labelled": "label",

    "analyzing": "analysis",
    "analysing": "analysis",
    "analyzed": "analysis",
    "analysed": "analysis",

    "managing": "management",
    "managed": "management",

    "leading": "leadership",
    "led": "leadership",

    "communicating": "communication",
    "communicated": "communication",

    "improving": "improvement",
    "improved": "improvement",

    "checking": "check",
    "checked": "check"
}


# ============================================================
# KEYWORD WEIGHTS
# ============================================================

KEYWORD_WEIGHTS = {

    # High-value job-specific keywords
    "data annotation": 5.0,
    "image annotation": 5.0,
    "text annotation": 5.0,
    "lidar annotation": 5.0,

    "quality assurance": 5.0,
    "quality control": 4.0,

    "dataset": 4.0,
    "machine learning": 4.0,
    "artificial intelligence": 4.0,
    "computer vision": 4.0,
    "data analysis": 4.0,
    "data science": 4.0,

    # Programming / Technical
    "python": 4.0,
    "java": 4.0,
    "javascript": 4.0,
    "typescript": 4.0,
    "c++": 4.0,
    "c#": 4.0,

    "sql": 4.0,
    "mysql": 4.0,
    "postgresql": 4.0,
    "mongodb": 4.0,
    "oracle": 4.0,

    "tensorflow": 4.0,
    "pytorch": 4.0,
    "scikit learn": 4.0,

    "aws": 4.0,
    "azure": 4.0,
    "docker": 4.0,
    "kubernetes": 4.0,

    # Web
    "react": 4.0,
    "angular": 4.0,
    "vue": 4.0,
    "node js": 4.0,
    "django": 4.0,
    "flask": 4.0,
    "fastapi": 4.0,
    "rest api": 4.0,

    # Office / Analytics
    "excel": 3.0,
    "word": 3.0,
    "powerpoint": 3.0,
    "power bi": 3.0,
    "tableau": 3.0,

    # Professional skills
    "communication": 3.0,
    "leadership": 3.0,
    "teamwork": 3.0,
    "problem solving": 3.0,

    "project management": 3.0,
    "attention to detail": 3.0,
    "critical thinking": 3.0,
    "analytical thinking": 3.0,

    "process improvement": 3.0,
    "customer service": 3.0,
    "customer support": 3.0,

    # Job-performance keywords
    "accuracy": 2.0,
    "productivity": 2.0,
    "guideline": 2.0,
    "target": 2.0,
    "benchmark": 2.0,

    # Medium-value terms
    "project": 1.0,
    "task": 1.0,
    "requirement": 1.0,
    "model": 1.0,
    "image": 1.0,
    "text": 1.0,
    "associate": 1.0,
    "high": 1.0
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Normalize text.

    Example:
        Data-Annotation / Quality Assurance
        ->
        data annotation quality assurance
    """

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("−", "-")

    text = text.replace("/", " ")

    # Preserve + and # for C++ and C#
    text = re.sub(
        r"[^a-z0-9+#\s-]",
        " ",
        text
    )

    text = text.replace("-", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# BUILD ALIAS MAP
# ============================================================

def get_alias_map():
    """
    Build one normalized alias dictionary.

    The important difference from the previous version:
    aliases are NOT repeatedly applied to their own output.

    This prevents:

        lidar data
        ->
        lidar annotation
        ->
        lidar annotation annotation
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
# APPLY ALIASES SAFELY
# ============================================================

def apply_aliases(text):
    """
    Apply aliases safely in ONE normalization pass.

    This function deliberately avoids recursive alias
    replacement.

    Example:

        lidar data
        ->
        lidar annotation

    and stops there.

    It will NOT become:

        lidar annotation annotation
    """

    text = clean_text(text)

    if not text:
        return ""

    aliases = get_alias_map()

    # Longest aliases first
    sorted_aliases = sorted(
        aliases.items(),
        key=lambda item: (
            -len(item[0].split()),
            -len(item[0])
        )
    )

    # Protect already-normalized replacements
    placeholders = {}

    for index, (alias, canonical) in enumerate(
        sorted_aliases
    ):

        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if not re.search(
            pattern,
            text
        ):
            continue

        placeholder = (
            f"zzaliasplaceholder{index}zz"
        )

        placeholders[placeholder] = canonical

        text = re.sub(
            pattern,
            placeholder,
            text
        )

    # Restore replacements exactly once
    for placeholder, canonical in placeholders.items():

        text = text.replace(
            placeholder,
            canonical
        )

    return text


# ============================================================
# NORMALIZE WORD
# ============================================================

def normalize_word(word):
    """
    Normalize individual words.

    Conservative normalization prevents technical
    words from being damaged.
    """

    word = str(word).lower().strip()

    if not word:
        return ""

    irregular = {

        "targets": "target",
        "target": "target",

        "datasets": "dataset",
        "dataset": "dataset",

        "projects": "project",
        "project": "project",

        "annotations": "annotation",
        "annotation": "annotation",

        "guidelines": "guideline",
        "guideline": "guideline",

        "benchmarks": "benchmark",
        "benchmark": "benchmark",

        "models": "model",
        "model": "model",

        "tasks": "task",
        "task": "task",

        "requirements": "requirement",
        "requirement": "requirement",

        "images": "image",
        "image": "image",

        "texts": "text",
        "text": "text"
    }

    if word in irregular:
        return irregular[word]

    protected = {
        "aws",
        "css",
        "html",
        "sql",
        "numpy",
        "pandas",
        "excel",
        "python",
        "java",
        "react",
        "vue",
        "node",
        "linux",
        "unix",
        "api",
        "apis",
        "ai",
        "ml"
    }

    if word in protected:
        return word

    # ies -> y
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"

    # Avoid damaging words like "process"
    if len(word) > 4 and word.endswith("sses"):
        return word[:-2]

    # Common plural forms
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
    Build known multi-word phrases.

    Duplicate phrases are automatically removed.
    """

    phrases = set()

    # Skills
    for skill in SKILLS:

        normalized = apply_aliases(skill)

        if " " in normalized:
            phrases.add(normalized)

    # Skill aliases
    for alias, canonical in SKILL_ALIASES.items():

        alias_clean = clean_text(alias)
        canonical_clean = clean_text(canonical)

        if " " in alias_clean:
            phrases.add(canonical_clean)

    # Extra aliases
    for alias, canonical in EXTRA_ALIASES.items():

        alias_clean = clean_text(alias)
        canonical_clean = clean_text(canonical)

        if " " in alias_clean:
            phrases.add(canonical_clean)

    # Weighted keywords
    for keyword in KEYWORD_WEIGHTS:

        normalized = clean_text(keyword)

        if " " in normalized:
            phrases.add(normalized)

    return sorted(
        phrases,
        key=lambda phrase: (
            -len(phrase.split()),
            -len(phrase)
        )
    )


# ============================================================
# EXTRACT KEYWORDS
# ============================================================

def extract_keywords(text):
    """
    Extract normalized keywords.

    Multi-word skills stay together.

    Examples:

        AI
        ->
        artificial intelligence

        targets
        ->
        target

        lidar data
        ->
        lidar annotation

    Importantly, the function never produces:

        lidar annotation annotation
    """

    text = apply_aliases(text)

    if not text:
        return set()

    phrases = get_known_phrases()

    keywords = set()

    placeholder_text = text

    # --------------------------------------------------------
    # Detect phrases first
    # --------------------------------------------------------

    for index, phrase in enumerate(phrases):

        pattern = (
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)"
        )

        if not re.search(
            pattern,
            placeholder_text
        ):
            continue

        keywords.add(phrase)

        placeholder = (
            f"zzphrase{index}zz"
        )

        placeholder_text = re.sub(
            pattern,
            placeholder,
            placeholder_text
        )

    # --------------------------------------------------------
    # Extract remaining words
    # --------------------------------------------------------

    words = placeholder_text.split()

    for word in words:

        if word.startswith("zzphrase"):
            continue

        word = normalize_word(word)

        if not word:
            continue

        if len(word) <= 2:
            continue

        if word in STOP_WORDS:
            continue

        keywords.add(word)

    return keywords


# ============================================================
# GET KEYWORD WEIGHT
# ============================================================

def get_keyword_weight(keyword):
    """
    Return importance weight for a keyword.
    """

    normalized = clean_text(
        keyword
    )

    if normalized in KEYWORD_WEIGHTS:

        return KEYWORD_WEIGHTS[
            normalized
        ]

    normalized_skills = {
        clean_text(skill)
        for skill in SKILLS
    }

    if normalized in normalized_skills:
        return 3.0

    return 1.0


# ============================================================
# CALCULATE WEIGHTED KEYWORD SCORE
# ============================================================

def calculate_keyword_score(
    resume_text,
    job_description
):
    """
    Calculate weighted keyword similarity.

    High-value technical/job-specific keywords
    receive more importance.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    if not job_keywords:
        return 0.0

    total_weight = 0.0
    matched_weight = 0.0

    for keyword in job_keywords:

        weight = get_keyword_weight(
            keyword
        )

        total_weight += weight

        if keyword in resume_keywords:

            matched_weight += weight

    if total_weight <= 0:
        return 0.0

    score = (
        matched_weight /
        total_weight
    ) * 100

    return round(
        min(score, 100.0),
        2
    )


# ============================================================
# GET MATCHED KEYWORDS
# ============================================================

def get_matched_keywords(
    resume_text,
    job_description
):
    """
    Return keywords found in both resume
    and job description.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    matched = (
        resume_keywords.intersection(
            job_keywords
        )
    )

    return sorted(
        matched,
        key=lambda keyword: (
            -get_keyword_weight(keyword),
            keyword
        )
    )


# ============================================================
# GET MISSING KEYWORDS
# ============================================================

def get_missing_keywords(
    resume_text,
    job_description
):
    """
    Return meaningful keywords missing from
    the resume.

    Only keywords with weight >= 1.5
    are reported.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    missing = (
        job_keywords -
        resume_keywords
    )

    meaningful_missing = []

    for keyword in missing:

        weight = get_keyword_weight(
            keyword
        )

        if weight >= 1.5:

            meaningful_missing.append(
                keyword
            )

    return sorted(
        meaningful_missing,
        key=lambda keyword: (
            -get_keyword_weight(keyword),
            keyword
        )
    )


# ============================================================
# KEYWORD MATCH DETAILS
# ============================================================

def get_keyword_match_details(
    resume_text,
    job_description
):
    """
    Return detailed keyword matching information.

    Useful for GUI/dashboard integration.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    matched = []
    missing = []

    for keyword in job_keywords:

        weight = get_keyword_weight(
            keyword
        )

        if keyword in resume_keywords:

            matched.append({
                "keyword": keyword,
                "weight": weight
            })

        elif weight >= 1.5:

            missing.append({
                "keyword": keyword,
                "weight": weight
            })

    matched.sort(
        key=lambda item: (
            -item["weight"],
            item["keyword"]
        )
    )

    missing.sort(
        key=lambda item: (
            -item["weight"],
            item["keyword"]
        )
    )

    return {
        "matched": matched,
        "missing": missing
    }


# ============================================================
# CHECK KEYWORD PRESENCE
# ============================================================

def check_keyword_presence(
    resume_text,
    keyword
):
    """
    Check whether a normalized keyword exists
    in the resume.
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    normalized_keyword = apply_aliases(
        keyword
    )

    # If the normalized keyword is a phrase,
    # check it directly.
    if normalized_keyword in resume_keywords:
        return True

    normalized_keyword = normalize_word(
        normalized_keyword
    )

    if normalized_keyword in resume_keywords:
        return True

    return False


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Experienced Senior Process Associate with
    data annotation, image annotation and LiDAR
    annotation experience.

    Worked with AI and machine learning training data.

    Experienced with MS Excel, MS Word and PowerPoint.

    Strong communication, leadership, problem solving
    and quality assurance skills.

    Maintained productivity and accuracy benchmarks
    above 98 percent and consistently achieved
    assigned targets.
    """

    sample_job = """
    We are looking for a Data Annotation Associate.

    Required Skills:
    Data Annotation
    Quality Assurance
    Communication
    MS Excel

    Preferred Skills:
    Problem-solving
    Leadership
    Artificial Intelligence

    The candidate should have experience working with
    image annotation, LiDAR data and machine learning
    training datasets.

    The candidate should maintain high accuracy
    and meet productivity targets.
    """

    print("\n==============================")
    print("SMART KEYWORD MATCHING TEST")
    print("==============================")

    print("\nResume Keywords:")

    resume_keywords = extract_keywords(
        sample_resume
    )

    for keyword in sorted(resume_keywords):

        print(
            "✓",
            keyword,
            "(weight:",
            get_keyword_weight(keyword),
            ")"
        )

    print("\nMatched Keywords:")

    for keyword in get_matched_keywords(
        sample_resume,
        sample_job
    ):

        print(
            "✓",
            keyword,
            "(weight:",
            get_keyword_weight(keyword),
            ")"
        )

    print("\nMissing Important Keywords:")

    missing = get_missing_keywords(
        sample_resume,
        sample_job
    )

    if missing:

        for keyword in missing:

            print(
                "✗",
                keyword,
                "(weight:",
                get_keyword_weight(keyword),
                ")"
            )

    else:

        print("None")

    print(
        "\nWeighted Keyword Match Score:",
        calculate_keyword_score(
            sample_resume,
            sample_job
        ),
        "%"
    )

    print(
        "\nTarget present after normalization:",
        check_keyword_presence(
            sample_resume,
            "target"
        )
    )

    print("==============================")