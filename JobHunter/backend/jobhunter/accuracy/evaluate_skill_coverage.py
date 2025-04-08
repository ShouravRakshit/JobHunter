import pandas as pd

def evaluate_skill_coverage(input_csv, output_csv, text_col="cleaned_description", skill_col="extracted_skills"):
    """
    Reads a CSV file with columns for job text (e.g. 'cleaned_description') and 
    extracted skills (e.g. 'extracted_skills').
    
    For each row:
      1) Splits the 'extracted_skills' into a list of skills.
      2) Checks how many of those skills literally appear in the job's text.
      3) Calculates coverage = (# of found skills) / (total extracted skills).
    
    Writes a new CSV with a 'skill_coverage' column for each row,
    and prints the average coverage across all rows.
    """
    df = pd.read_csv(input_csv)
    
    # We'll create a new column 'skill_coverage' to store the ratio
    coverage_list = []
    
    for idx, row in df.iterrows():
        job_text = str(row.get(text_col, "")).lower()
        skills_str = str(row.get(skill_col, ""))
        

        skill_list = [s.strip().lower() for s in skills_str.split(",") if s.strip()]
        
        if not skill_list:
            # If no extracted skills, coverage is 0 (or we can define it as None)
            coverage_list.append(0.0)
            continue
        
        found_count = 0
        for skill in skill_list:
            # Check if the skill is a substring in the job text
            if skill and skill in job_text:
                found_count += 1
        
        coverage = found_count / len(skill_list)
        coverage_list.append(coverage)
    
    df["skill_coverage"] = coverage_list
    # Save to CSV
    df.to_csv(output_csv, index=False)
    
    # Compute average coverage across all postings
    avg_coverage = sum(coverage_list) / len(coverage_list) if coverage_list else 0
    print(f"Average skill coverage: {avg_coverage:.2%} (0 to 1 means 0% to 100%)")
    print(f"Updated file with skill coverage: {output_csv}")

def main():
    input_csv = "JobHunter/data/rule_based_experience.csv"  
    output_csv = "JobHunter/data/jobs_with_skills_coverage.csv"
    
    evaluate_skill_coverage(input_csv, output_csv)

if __name__ == "__main__":
    main()