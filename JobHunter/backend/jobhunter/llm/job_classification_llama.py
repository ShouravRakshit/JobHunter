import csv
import subprocess
import re

def classify_job_posting_llama(job_description, model="llama3.1:8b"):
    """
        Uses the LLaMA model to classify the job description.
    """
    # categories llm going to choose from.
    categories = [
        "Software Development",
        "Data Science & Analytics",
        "Healthcare & Nursing",
        "Construction & Infrastructure",
        "Marketing & Sales",
        "Finance & Accounting",
        "Operations & Logistics",
        "Human Resources",
        "Customer Service",
        "Manufacturing & Production",
        "Legal & Compliance",
        "Education & Training",
        "Administrative & Office Support",
        "Research & Development",
        "Information Technology",
        "Project Management",
        "Consulting",
        "Real Estate",
        "Arts & Entertainment",
        "Media & Communications",
        "Hospitality & Tourism",
        "Retail & Wholesale",
        "Telecommunications",
        "Transportation & Warehousing",
        "Insurance",
        "Energy & Utilities",
        "Agriculture & Farming",
        "Pharmaceuticals & Biotechnology",
        "Government & Public Sector",
        "Security & Protective Services",
        "Environmental & Sustainability",
        "Personal Care & Services",
        "Sports & Recreation",
        "Automotive & Transportation",
        "Other"
    ]
    
    # prompt
    prompt = f"""
You are an expert job classifier. I will provide a job posting description.
You must classify it into exactly ONE of the following categories:

{', '.join(categories)}

If none fits perfectly, pick the closest.
Reply ONLY with the category name, nothing else.

Job Description:
\"\"\"
{job_description}
\"\"\"
"""

    print("\n=== PROMPT DEBUG ===")
    print(prompt)
    print("=== END PROMPT ===\n")
    
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8"
    )
    
    print("Return code:", result.returncode)
    print("STDERR:", result.stderr)
    response_text = result.stdout.strip()
    print("STDOUT:", response_text)
    
    classification = re.split(r'[\r\n]', response_text)[0].strip()
    return classification

def main():
    input_csv = "JobHunter/data/jobs_with_tfidf_keywords.csv"
    output_csv = "JobHunter/data/unclean_jobs_with_llm_categories.csv"

    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["llm_category"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            desc = row.get("cleaned_description", "")
            category = classify_job_posting_llama(desc)
            row["llm_category"] = category
            writer.writerow(row)

    print(f"\nLLM-based classification complete. Results written to {output_csv}")

if __name__ == "__main__":
    main()