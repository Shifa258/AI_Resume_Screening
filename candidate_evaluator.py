# ============================================================
# candidate_evaluator.py
# Human-readable ATS candidate evaluation
# ============================================================


def evaluate_candidate(result):
    """
    Convert ranking information into an understandable
    recruiter-style evaluation.

    This evaluator uses the actual experience years and
    required range instead of assuming that any experience
    score below 100 means the candidate is underqualified.
    """

    score = float(
        result.get(
            "final_score",
            0
        )
    )

    required_score = float(
        result.get(
            "required_score",
            0
        )
    )

    preferred_score = float(
        result.get(
            "preferred_score",
            0
        )
    )

    keyword_score = float(
        result.get(
            "keyword_score",
            0
        )
    )

    tfidf_score = float(
        result.get(
            "tfidf_score",
            0
        )
    )

    experience_score = float(
        result.get(
            "experience_score",
            0
        )
    )

    education_score = float(
        result.get(
            "education_score",
            0
        )
    )

    candidate_years = float(
        result.get(
            "experience_years",
            0
        )
    )

    required_years = float(
        result.get(
            "required_years",
            0
        )
    )

    maximum_years = result.get(
        "required_maximum_years",
        None
    )

    if maximum_years is not None:

        try:
            maximum_years = float(
                maximum_years
            )
        except Exception:
            maximum_years = None

    missing_required = result.get(
        "missing_skills",
        []
    )

    matched_skills = result.get(
        "matched_skills",
        []
    )

    strengths = []
    areas = []

    # ========================================================
    # EXPERIENCE STATUS
    # ========================================================

    experience_required = (
        required_years > 0
    )

    experience_meets_minimum = (
        candidate_years >= required_years
        if experience_required
        else True
    )

    experience_within_range = True

    if (
        experience_meets_minimum
        and maximum_years is not None
    ):

        experience_within_range = (
            candidate_years <= maximum_years
        )

    # ========================================================
    # STRENGTHS
    # ========================================================

    if education_score >= 100:

        strengths.append(
            "Required education level satisfied"
        )

    if experience_required:

        if experience_within_range:

            strengths.append(
                "Experience requirement satisfied and falls within the requested range"
            )

        elif experience_meets_minimum:

            strengths.append(
                "Candidate meets the minimum experience requirement"
            )

    else:

        strengths.append(
            "No specific experience requirement was detected"
        )

    if required_score >= 80:

        strengths.append(
            "Strong match for required skills"
        )

    elif required_score >= 60:

        strengths.append(
            "Good coverage of required skills"
        )

    elif required_score >= 40:

        strengths.append(
            "Relevant required skills detected in the resume"
        )

    if preferred_score >= 70:

        strengths.append(
            "Strong coverage of preferred skills"
        )

    elif preferred_score >= 40:

        strengths.append(
            "Some preferred skills are present"
        )

    if keyword_score >= 60:

        strengths.append(
            "Good alignment with important ATS keywords"
        )

    elif keyword_score >= 40:

        strengths.append(
            "Moderate alignment with important ATS keywords"
        )

    if tfidf_score >= 25:

        strengths.append(
            "Good contextual similarity with the job description"
        )

    elif tfidf_score >= 15:

        strengths.append(
            "Moderate contextual similarity with the job description"
        )

    if matched_skills:

        strengths.append(
            "Relevant technical/professional skills detected in the resume"
        )

    # ========================================================
    # AREAS TO IMPROVE
    # ========================================================

    if missing_required:

        important_missing = ", ".join(
            missing_required[:8]
        )

        areas.append(
            "Missing required skills: "
            + important_missing
        )

    # --------------------------------------------------------
    # Preferred skills
    # --------------------------------------------------------

    preferred = result.get(
        "preferred_skills",
        []
    )

    matched_preferred = set(
        result.get(
            "matched_preferred_skills",
            []
        )
    )

    missing_preferred = []

    for skill in preferred:

        if skill not in matched_preferred:

            missing_preferred.append(
                skill
            )

    if missing_preferred:

        areas.append(
            "Missing preferred skills: "
            + ", ".join(
                missing_preferred[:6]
            )
        )

    # --------------------------------------------------------
    # Keywords
    # --------------------------------------------------------

    if keyword_score < 50:

        areas.append(
            "Low alignment with important ATS keywords"
        )

    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    if tfidf_score < 15:

        areas.append(
            "Low contextual similarity between the resume and job description"
        )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    if experience_required:

        # Candidate is actually below the minimum.
        if not experience_meets_minimum:

            areas.append(
                "Experience is below the stated minimum requirement"
            )

        # Candidate meets minimum but exceeds maximum.
        elif (
            maximum_years is not None
            and candidate_years > maximum_years
        ):

            areas.append(
                "Experience exceeds the preferred maximum range"
            )

    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    if education_score < 100:

        areas.append(
            "Education does not fully match the stated requirement"
        )

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    # Strong recommendation requires both overall score
    # and adequate required-skill coverage.

    if (
        score >= 80
        and required_score >= 80
        and education_score >= 100
        and (
            not experience_required
            or experience_meets_minimum
        )
    ):

        recommendation = "STRONGLY RECOMMENDED"

        reason = (
            "Candidate demonstrates strong alignment "
            "with the required skills and overall job "
            "requirements."
        )

    elif (
        score >= 65
        and required_score >= 60
        and education_score >= 100
        and (
            not experience_required
            or experience_meets_minimum
        )
    ):

        recommendation = "RECOMMENDED"

        reason = (
            "Candidate shows good overall alignment "
            "with the role and satisfies most important "
            "requirements."
        )

    elif (
        score >= 50
        and required_score >= 40
        and (
            not experience_required
            or experience_meets_minimum
        )
    ):

        recommendation = "CONDITIONALLY RECOMMENDED"

        reason = (
            "Candidate has relevant qualifications, "
            "but some important requirements or skills "
            "are missing."
        )

    elif (
        score >= 35
        or required_score >= 30
    ):

        recommendation = "NEEDS REVIEW"

        reason = (
            "Candidate has some relevant qualifications, "
            "but the match is not strong enough for an "
            "automatic recommendation."
        )

    else:

        recommendation = "NOT RECOMMENDED"

        reason = (
            "Candidate is missing a significant portion "
            "of the required qualifications."
        )

    # ========================================================
    # FALLBACKS
    # ========================================================

    if not strengths:

        strengths.append(
            "Candidate evaluation completed"
        )

    if not areas:

        areas.append(
            "No major improvement areas detected"
        )

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "recommendation":
            recommendation,

        "recommendation_reason":
            reason,

        "strengths":
            strengths,

        "areas_to_improve":
            areas,

        "score":
            score
    }