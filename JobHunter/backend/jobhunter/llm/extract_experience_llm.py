import csv
import subprocess
import re

def extract_experience_llm(job_description, model="llama3.1:8b"):
    """
    Uses the locally installed LLaMA model (via Ollama) to extract the required experience from a job posting.
    It sends the job description to the model with a prompt that asks for the years of experience required.
    """
    prompt = f"""

You are an expert at reading job postings and finding the required experience.
I'd like you to read the following job posting and extract the required years of experience for the role.
If the job description explicitly mentions a number (e.g., '3 years', '1-2 years'), output that.
If it does not explicitly state a number, please provide a reasonable estimate based on the responsibilities and
required skills mentioned in the posting. Your answer should be a short response formatted as 'X years'
or 'Not specified' if no estimate can be made. Let's make it thorough and accurate.

Job Description:
\"\"\"
{job_description}
\"\"\"
"""
    # Print the prompt for debugging (optional)
    print("\n=== PROMPT DEBUG ===")
    print(prompt)
    print("=== END PROMPT ===\n")
    
    # Call the model using ollama, sending the prompt via standard input.
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
    
    # If the model returns extra text, we take the first non-empty line.
    experience = re.split(r'[\r\n]', response_text)[0].strip()
    return experience

def main():
    input_csv = "JobHunter/data/jobs_with_summary.csv"  # CSV with job postings and cleaned_description column
    output_csv = "JobHunter/data/jobs_with_experience.csv"
    
    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:
        
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["experience_required"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            job_desc = row.get("cleaned_description", "")
            exp_required = extract_experience_llm(job_desc)
            row["experience_required"] = exp_required
            writer.writerow(row)
    
    print(f"\nExperience extraction complete. Results written to {output_csv}")

if __name__ == "__main__":
    main()

