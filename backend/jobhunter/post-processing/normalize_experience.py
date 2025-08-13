import pandas as pd
import re

def normalize_experience(text):
    """
    Normalize the experience text to a standard format.
    
    This function looks for a range pattern (e.g., "3-5 years" or "3–5 years")
    and returns a standardized string like "3-5 years".
    If a range is not found but a single number is present (e.g., "5 years"),
    it returns "5 years". If no number is found, it returns "Not specified".
    
    For example:
      Input: "Based on the job posting, I estimate that 5-7 years of experience is required."
      Output: "5-7 years"
    """
    text = text.strip()
    
    # Try to find a range pattern: e.g., "3-5 years" or "3–5 years"
    pattern_range = r'(\d+)\s*[-–]\s*(\d+)\s*years?'
    match_range = re.search(pattern_range, text, re.IGNORECASE)
    if match_range:
        min_years = match_range.group(1)
        max_years = match_range.group(2)
        return f"{min_years}-{max_years} years"
    
    # If no range is found, look for a single number (e.g., "5 years")
    pattern_single = r'(\d+)\s*years?'
    match_single = re.search(pattern_single, text, re.IGNORECASE)
    if match_single:
        years = match_single.group(1)
        return f"{years} years"
    
    # If no experience number is found, return a default string.
    return "Not specified"

def main():
    # Define input and output CSV paths.
    input_csv = "JobHunter/data/jobs_with_experience.csv"  # This file should be produced by extract_experience_llm.py
    output_csv = "JobHunter/data/jobs_with_experience_normalized.csv"
    
    # Read the CSV into a DataFrame.
    df = pd.read_csv(input_csv)
    
    # Check if the column 'experience_required' exists.
    if "experience_required" not in df.columns:
        print("Column 'experience_required' not found in the CSV.")
        return
    
    # Apply the normalization function to the 'experience_required' column.
    df["experience_normalized"] = df["experience_required"].fillna("").apply(normalize_experience)
    
    # Save the updated DataFrame to a new CSV file.
    df.to_csv(output_csv, index=False)
    print(f"Normalized experience data saved to {output_csv}")

if __name__ == "__main__":
    main()
