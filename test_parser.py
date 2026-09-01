from resume_parser import extract_resume_text


resume_file = "SHIFA_SAREEN_CV_4 (3).pdf"

try:
    text = extract_resume_text(resume_file)

    print("\n========== EXTRACTED RESUME TEXT ==========\n")
    print(text)

    print("\n============================================")
    print("SUCCESS: Resume was read correctly!")

except Exception as e:
    print("ERROR:", e)