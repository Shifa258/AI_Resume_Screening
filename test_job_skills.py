from job_skill_extractor import extract_job_skills


job_description = """
We are looking for a Python Developer.

The candidate should have experience with Python,
SQL, MySQL, Pandas, Machine Learning and Git.

Knowledge of Microsoft Excel is also preferred.
"""


skills = extract_job_skills(job_description)

print("\nDetected Job Skills:")

for skill in skills:
    print("✓", skill)