from keyword_matcher import (
    calculate_keyword_score,
    get_matched_keywords,
    get_missing_keywords
)


resume_text = """
Experienced Senior Process Associate skilled in
data annotation, image annotation and LiDAR annotation.

Worked with AI and machine learning training data.
Experienced with MS Excel, MS Word and PowerPoint.

Strong communication, leadership, problem solving
and quality assurance skills.

Maintained productivity and accuracy benchmarks
above 98 percent.
"""


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
Artificial Intelligence

The candidate should have experience with
image annotation, LiDAR data and machine learning
training datasets.
"""


score = calculate_keyword_score(
    resume_text,
    job_description
)

matched = get_matched_keywords(
    resume_text,
    job_description
)

missing = get_missing_keywords(
    resume_text,
    job_description
)


print("\n==============================")
print("KEYWORD MATCHING TEST")
print("==============================")

print("\nMatched Keywords:")

for keyword in matched:
    print("✓", keyword)


print("\nMissing Keywords:")

for keyword in missing:
    print("✗", keyword)


print("\nKeyword Match Score:", score, "%")

print("==============================")