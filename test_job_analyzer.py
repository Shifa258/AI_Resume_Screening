from job_analyzer import analyze_job_description


job_description = """
We are looking for a Python Developer.

Required Skills:
Python
SQL
MySQL

Preferred Skills:
Pandas
Git
AWS
"""


result = analyze_job_description(job_description)


print("\n==============================")
print("JOB ANALYSIS")
print("==============================")

print("\nRequired Skills:")

for skill in result["required_skills"]:
    print("✓", skill)

print("\nPreferred Skills:")

for skill in result["preferred_skills"]:
    print("✓", skill)

print("==============================")