# ============================================================
# app.py
# AI Resume Screening System
# Production ATS Interface
# ============================================================

import os
import tempfile
from io import StringIO

import streamlit as st

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from ranker import calculate_final_score
from candidate_evaluator import evaluate_candidate


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #777;
        margin-bottom: 25px;
    }

    .score-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.25);
    }

    .score-number {
        font-size: 42px;
        font-weight: 700;
    }

    .recommendation {
        font-size: 24px;
        font-weight: 700;
    }

    .related-skill {
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 6px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI Resume Screening System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'ATS-style resume analysis using skills, weighted keywords, '
    'TF-IDF, experience and education matching.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# INPUT
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX resume",
        type=["pdf", "docx"],
        help="Upload the candidate's resume."
    )

    if uploaded_file:

        st.success(
            f"Resume uploaded: {uploaded_file.name}"
        )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the complete job description",
        height=300,
        placeholder=(
            "Paste the complete job description here..."
        )
    )


# ============================================================
# SCREEN BUTTON
# ============================================================

st.divider()

screen_button = st.button(
    "🔍 SCREEN RESUME",
    type="primary",
    use_container_width=True
)


# ============================================================
# SCREENING
# ============================================================

if screen_button:

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    if uploaded_file is None:

        st.error(
            "❌ Please upload a PDF or DOCX resume."
        )

        st.stop()

    if not job_description.strip():

        st.error(
            "❌ Please enter a job description."
        )

        st.stop()

    # --------------------------------------------------------
    # TEMPORARY FILE
    # --------------------------------------------------------

    suffix = (
        ".pdf"
        if uploaded_file.name.lower().endswith(".pdf")
        else ".docx"
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp_file.write(
        uploaded_file.getbuffer()
    )

    temp_file.close()

    resume_file = temp_file.name

    try:

        # ====================================================
        # RESUME EXTRACTION
        # ====================================================

        with st.spinner(
            "📖 Reading resume..."
        ):

            resume_text = extract_resume_text(
                resume_file
            )

        if not resume_text or not resume_text.strip():

            st.error(
                "❌ Could not extract readable text from the resume."
            )

            st.stop()

        # ====================================================
        # SKILLS
        # ====================================================

        with st.spinner(
            "🧠 Detecting candidate skills..."
        ):

            resume_skills = extract_skills(
                resume_text
            )

        # ====================================================
        # RANKING
        # ====================================================

        with st.spinner(
            "📊 Calculating ATS score..."
        ):

            result = calculate_final_score(
                resume_text,
                job_description,
                resume_skills
            )

        # ====================================================
        # EVALUATION
        # ====================================================

        with st.spinner(
            "🧑‍💼 Evaluating candidate..."
        ):

            evaluation = evaluate_candidate(
                result
            )

        # ====================================================
        # SAFE EVALUATION VALUES
        # ====================================================

        if not isinstance(evaluation, dict):

            evaluation = {}

        recommendation = evaluation.get(
            "recommendation",
            "NEEDS REVIEW"
        )

        recommendation_message = evaluation.get(
            "recommendation_reason",
            "Candidate evaluation completed."
        )

        strengths = evaluation.get(
            "strengths",
            []
        )

        areas_to_improve = evaluation.get(
            "areas_to_improve",
            []
        )

        # Make sure list values are actually lists.

        if not isinstance(strengths, list):

            strengths = [str(strengths)]

        if not isinstance(areas_to_improve, list):

            areas_to_improve = [
                str(areas_to_improve)
            ]

        # ====================================================
        # RESULT
        # ====================================================

        st.divider()

        st.header(
            "📊 Screening Result"
        )

        score = float(
            result.get(
                "final_score",
                0
            )
        )

        score = max(
            0.0,
            min(
                100.0,
                score
            )
        )

        score_col, recommendation_col = st.columns(2)

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        with score_col:

            st.markdown(
                '<div class="score-box">',
                unsafe_allow_html=True
            )

            st.caption(
                "FINAL ATS SCORE"
            )

            st.markdown(
                f'<div class="score-number">'
                f'{score:.2f}%'
                f'</div>',
                unsafe_allow_html=True
            )

            st.progress(
                min(
                    max(
                        score / 100,
                        0
                    ),
                    1
                )
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        with recommendation_col:

            st.markdown(
                '<div class="score-box">',
                unsafe_allow_html=True
            )

            st.caption(
                "RECOMMENDATION"
            )

            st.markdown(
                f'<div class="recommendation">'
                f'{recommendation}'
                f'</div>',
                unsafe_allow_html=True
            )

            if "STRONGLY" in recommendation:

                st.success(
                    recommendation_message
                )

            elif recommendation == "RECOMMENDED":

                st.info(
                    recommendation_message
                )

            elif "CONDITIONALLY" in recommendation:

                st.warning(
                    recommendation_message
                )

            elif "NEEDS REVIEW" in recommendation:

                st.warning(
                    recommendation_message
                )

            else:

                st.error(
                    recommendation_message
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # ====================================================
        # SCORE BREAKDOWN
        # ====================================================

        st.divider()

        st.subheader(
            "📈 ATS Score Breakdown"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Required Skills",
                f'{result.get("required_score", 0)}%'
            )

        with c2:

            st.metric(
                "Preferred Skills",
                f'{result.get("preferred_score", 0)}%'
            )

        with c3:

            st.metric(
                "ATS Keywords",
                f'{result.get("keyword_score", 0)}%'
            )

        c4, c5, c6 = st.columns(3)

        with c4:

            st.metric(
                "TF-IDF Context",
                f'{result.get("tfidf_score", 0)}%'
            )

        with c5:

            st.metric(
                "Experience",
                f'{result.get("experience_score", 0)}%'
            )

        with c6:

            st.metric(
                "Education",
                f'{result.get("education_score", 0)}%'
            )

        # ====================================================
        # WEIGHTS
        # ====================================================

        st.caption(
            "Weights: Required Skills 40% • Preferred Skills 10% • "
            "Keywords 10% • TF-IDF 10% • Experience 20% • "
            "Education 10%"
        )

        # ====================================================
        # EXPERIENCE / EDUCATION
        # ====================================================

        st.divider()

        st.subheader(
            "🎓 Experience & Education"
        )

        e1, e2, e3 = st.columns(3)

        with e1:

            st.metric(
                "Candidate Experience",
                f'{result.get("experience_years", 0)} years'
            )

        with e2:

            st.metric(
                "Minimum Experience",
                f'{result.get("required_years", 0)} years'
            )

        with e3:

            st.metric(
                "Education",
                result.get(
                    "education_level",
                    "Not Detected"
                )
            )

        # ====================================================
        # SKILLS ANALYSIS
        # ====================================================

        st.divider()

        st.header(
            "🛠️ Skills Analysis"
        )

        skill_col1, skill_col2 = st.columns(2)

        # ====================================================
        # REQUIRED SKILLS
        # ====================================================

        with skill_col1:

            st.subheader(
                "Required Skills"
            )

            required_skills = result.get(
                "required_skills",
                []
            )

            matched_required_skills = set(
                result.get(
                    "matched_required_skills",
                    []
                )
            )

            related_required_skills = result.get(
                "related_required_skills",
                []
            )

            related_required_map = {}

            for item in related_required_skills:

                related_required_map[
                    item.get("required_skill")
                ] = item

            if required_skills:

                for skill in required_skills:

                    if skill in matched_required_skills:

                        st.success(
                            f"✓ {skill}"
                        )

                    elif skill in related_required_map:

                        item = related_required_map[
                            skill
                        ]

                        matched_skill = item.get(
                            "matched_skill",
                            "related skill"
                        )

                        partial_score = item.get(
                            "score",
                            0
                        )

                        st.warning(
                            f"~ {skill} ← {matched_skill} "
                            f"({partial_score}%)"
                        )

                    else:

                        st.error(
                            f"✗ {skill}"
                        )

            else:

                st.info(
                    "No required skills detected."
                )

        # ====================================================
        # PREFERRED SKILLS
        # ====================================================

        with skill_col2:

            st.subheader(
                "Preferred Skills"
            )

            preferred_skills = result.get(
                "preferred_skills",
                []
            )

            matched_preferred_skills = set(
                result.get(
                    "matched_preferred_skills",
                    []
                )
            )

            related_preferred_skills = result.get(
                "related_preferred_skills",
                []
            )

            related_preferred_map = {}

            for item in related_preferred_skills:

                related_preferred_map[
                    item.get("preferred_skill")
                ] = item

            if preferred_skills:

                for skill in preferred_skills:

                    if skill in matched_preferred_skills:

                        st.success(
                            f"✓ {skill}"
                        )

                    elif skill in related_preferred_map:

                        item = related_preferred_map[
                            skill
                        ]

                        matched_skill = item.get(
                            "matched_skill",
                            "related skill"
                        )

                        partial_score = item.get(
                            "score",
                            0
                        )

                        st.warning(
                            f"~ {skill} ← {matched_skill} "
                            f"({partial_score}%)"
                        )

                    else:

                        st.warning(
                            f"✗ {skill}"
                        )

            else:

                st.info(
                    "No preferred skills detected."
                )

        # ====================================================
        # RELATED SKILL EXPLANATION
        # ====================================================

        if (
            related_required_skills
            or related_preferred_skills
        ):

            st.info(
                "ℹ️ Related skill matches receive partial "
                "credit rather than being treated as exact matches."
            )

        # ====================================================
        # MISSING REQUIRED SKILLS
        # ====================================================

        missing_required = result.get(
            "missing_required_skills",
            result.get(
                "missing_skills",
                []
            )
        )

        if missing_required:

            st.subheader(
                "⚠️ Missing Required Skills"
            )

            for skill in missing_required:

                st.error(
                    f"✗ {skill}"
                )

        # ====================================================
        # KEYWORDS
        # ====================================================

        st.divider()

        st.header(
            "🔎 ATS Keyword Analysis"
        )

        k1, k2 = st.columns(2)

        with k1:

            st.subheader(
                "✅ Matched Important Keywords"
            )

            matched_keywords = result.get(
                "matched_keywords",
                []
            )

            if matched_keywords:

                for keyword in matched_keywords:

                    st.write(
                        f"✓ {keyword}"
                    )

            else:

                st.write(
                    "None"
                )

        with k2:

            st.subheader(
                "⚠️ Missing Important Keywords"
            )

            missing_keywords = result.get(
                "missing_keywords",
                []
            )

            if missing_keywords:

                for keyword in missing_keywords:

                    st.write(
                        f"✗ {keyword}"
                    )

            else:

                st.write(
                    "None"
                )

        # ====================================================
        # CANDIDATE EVALUATION
        # ====================================================

        st.divider()

        st.header(
            "🧑‍💼 Candidate Evaluation"
        )

        st.subheader(
            "💪 Strengths"
        )

        if strengths:

            for strength in strengths:

                st.success(
                    f"✓ {strength}"
                )

        else:

            st.info(
                "No specific strengths identified."
            )

        st.subheader(
            "📌 Areas to Improve"
        )

        if areas_to_improve:

            for area in areas_to_improve:

                st.warning(
                    f"• {area}"
                )

        else:

            st.info(
                "No major improvement areas identified."
            )

        # ====================================================
        # REPORT
        # ====================================================

        st.divider()

        st.header(
            "📄 Screening Report"
        )

        report = StringIO()

        report.write(
            "AI RESUME SCREENING SYSTEM\n"
        )

        report.write(
            "====================================\n\n"
        )

        report.write(
            f"Resume: {uploaded_file.name}\n\n"
        )

        report.write(
            f"FINAL ATS SCORE: {score:.2f}%\n"
        )

        report.write(
            f"RECOMMENDATION: {recommendation}\n"
        )

        report.write(
            f"ASSESSMENT: {recommendation_message}\n\n"
        )

        # ====================================================
        # SCORE BREAKDOWN
        # ====================================================

        report.write(
            "SCORE BREAKDOWN\n"
        )

        report.write(
            "------------------------------------\n"
        )

        report.write(
            f'Required Skills: '
            f'{result.get("required_score", 0)}%\n'
        )

        report.write(
            f'Preferred Skills: '
            f'{result.get("preferred_score", 0)}%\n'
        )

        report.write(
            f'ATS Keywords: '
            f'{result.get("keyword_score", 0)}%\n'
        )

        report.write(
            f'TF-IDF Context: '
            f'{result.get("tfidf_score", 0)}%\n'
        )

        report.write(
            f'Experience: '
            f'{result.get("experience_score", 0)}%\n'
        )

        report.write(
            f'Education: '
            f'{result.get("education_score", 0)}%\n\n'
        )

        # ====================================================
        # EXPERIENCE / EDUCATION
        # ====================================================

        report.write(
            "EXPERIENCE & EDUCATION\n"
        )

        report.write(
            "------------------------------------\n"
        )

        report.write(
            f'Candidate Experience: '
            f'{result.get("experience_years", 0)} years\n'
        )

        report.write(
            f'Minimum Experience: '
            f'{result.get("required_years", 0)} years\n'
        )

        maximum_years = result.get(
            "required_maximum_years"
        )

        if maximum_years is not None:

            report.write(
                f'Maximum Experience: '
                f'{maximum_years} years\n'
            )

        report.write(
            f'Education: '
            f'{result.get("education_level", "Not Detected")}\n\n'
        )

        # ====================================================
        # REQUIRED SKILLS
        # ====================================================

        report.write(
            "REQUIRED SKILLS\n"
        )

        report.write(
            "------------------------------------\n"
        )

        for skill in result.get(
            "required_skills",
            []
        ):

            if skill in matched_required_skills:

                status = "MATCHED"

            elif skill in related_required_map:

                item = related_required_map[
                    skill
                ]

                matched_skill = item.get(
                    "matched_skill",
                    "related skill"
                )

                partial_score = item.get(
                    "score",
                    0
                )

                status = (
                    f"RELATED MATCH "
                    f"({matched_skill}, "
                    f"{partial_score}%)"
                )

            else:

                status = "MISSING"

            report.write(
                f"{status}: {skill}\n"
            )

        report.write(
            "\n"
        )

        # ====================================================
        # PREFERRED SKILLS
        # ====================================================

        report.write(
            "PREFERRED SKILLS\n"
        )

        report.write(
            "------------------------------------\n"
        )

        for skill in result.get(
            "preferred_skills",
            []
        ):

            if skill in matched_preferred_skills:

                status = "MATCHED"

            elif skill in related_preferred_map:

                item = related_preferred_map[
                    skill
                ]

                matched_skill = item.get(
                    "matched_skill",
                    "related skill"
                )

                partial_score = item.get(
                    "score",
                    0
                )

                status = (
                    f"RELATED MATCH "
                    f"({matched_skill}, "
                    f"{partial_score}%)"
                )

            else:

                status = "MISSING"

            report.write(
                f"{status}: {skill}\n"
            )

        report.write(
            "\n"
        )

        # ====================================================
        # RELATED REQUIRED SKILLS
        # ====================================================

        if related_required_skills:

            report.write(
                "RELATED REQUIRED SKILL MATCHES\n"
            )

            report.write(
                "------------------------------------\n"
            )

            for item in related_required_skills:

                report.write(
                    f'{item.get("required_skill")}'
                    f' <- '
                    f'{item.get("matched_skill")}'
                    f' '
                    f'({item.get("score")}%)\n'
                )

            report.write(
                "\n"
            )

        # ====================================================
        # RELATED PREFERRED SKILLS
        # ====================================================

        if related_preferred_skills:

            report.write(
                "RELATED PREFERRED SKILL MATCHES\n"
            )

            report.write(
                "------------------------------------\n"
            )

            for item in related_preferred_skills:

                report.write(
                    f'{item.get("preferred_skill")}'
                    f' <- '
                    f'{item.get("matched_skill")}'
                    f' '
                    f'({item.get("score")}%)\n'
                )

            report.write(
                "\n"
            )

        # ====================================================
        # MATCHED KEYWORDS
        # ====================================================

        report.write(
            "MATCHED KEYWORDS\n"
        )

        report.write(
            "------------------------------------\n"
        )

        for keyword in matched_keywords:

            report.write(
                f"MATCHED: {keyword}\n"
            )

        report.write(
            "\n"
        )

        # ====================================================
        # MISSING KEYWORDS
        # ====================================================

        report.write(
            "MISSING IMPORTANT KEYWORDS\n"
        )

        report.write(
            "------------------------------------\n"
        )

        for keyword in missing_keywords:

            report.write(
                f"MISSING: {keyword}\n"
            )

        report.write(
            "\n"
        )

        # ====================================================
        # STRENGTHS
        # ====================================================

        report.write(
            "STRENGTHS\n"
        )

        report.write(
            "------------------------------------\n"
        )

        for strength in strengths:

            report.write(
                f"- {strength}\n"
            )

        report.write(
            "\n"
        )

        # ====================================================
        # AREAS TO IMPROVE
        # ====================================================

        report.write(
            "AREAS TO IMPROVE\n"
        )

        report.write(
            "------------------------------------\n"
        )

        for area in areas_to_improve:

            report.write(
                f"- {area}\n"
            )

        report.write(
            "\n"
        )

        # ====================================================
        # FOOTER
        # ====================================================

        report.write(
            "====================================\n"
        )

        report.write(
            "Screening completed successfully.\n"
        )

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.download_button(
            label="⬇️ Download Screening Report",
            data=report.getvalue(),
            file_name="resume_screening_report.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.success(
            "✅ Resume screening completed successfully."
        )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "❌ An error occurred while analyzing the resume."
        )

        st.exception(
            error
        )

    # ========================================================
    # CLEANUP
    # ========================================================

    finally:

        if os.path.exists(
            resume_file
        ):

            os.remove(
                resume_file
            )