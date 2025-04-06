import csv
import subprocess
import re

def summarize_job_description(job_description, model="llama3.1:8b"):
    """
    Uses the LLaMA model to summarize a job posting.
    
    Parameters:
      job_description (str): The cleaned job description text.
      
    Returns:
      str: A concise summary (2-3 sentences) of the job posting.
    """
    # Build the prompt.
    # the model to produce a concise summary that captures key details.
    prompt = f"""
You are an expert job summarizer. Given the following job posting description,
produce a concise summary (3-4 sentences) that highlights the main responsibilities, 
requirements, and essential details of the job posting.

Job Posting Description:
\"\"\"
{job_description}
\"\"\"

Provide ONLY the summary, with no extra commentary.
"""
    print("\n=== PROMPT DEBUG ===")
    print(prompt)
    print("=== END PROMPT ===\n")
    

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8"  # utf-8 to handle any special characters
        )
    except Exception as e:
        print("Error calling Ollama:", e)
        return ""
    
    print("Return code:", result.returncode)
    print("STDERR:", result.stderr)
    
    response_text = result.stdout.strip()
    print("STDOUT:", response_text)
    
    summary = re.split(r'[\r\n]', response_text)[0].strip()
    return summary

def main():
    # input and output CSV paths.
    input_csv = "JobHunter/data/jobs_with_llm_categories.csv"  
    output_csv = "JobHunter/data/jobs_with_summary.csv"

    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)
        # Add a new column "summary"
        fieldnames = reader.fieldnames + ["summary"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Get the cleaned job description; if not present, use an empty string.
            job_desc = row.get("cleaned_description", "")
            summary = summarize_job_description(job_desc)
            row["summary"] = summary
            writer.writerow(row)

    print(f"\nSummarization complete. Results written to {output_csv}")

if __name__ == "__main__":
    main()