import pandas as pd
import re

def extract_experience(text):
    """
    Extract the required years of experience from a job description.
    
    This function finds all instances of either a range (e.g., "3-5 years" or "3–5 years")
    or a single number (e.g., "5 years"). If one or more ranges are found, it returns 
    the range with the highest upper bound (e.g., if "3-5 years" and "2-3 years" are found, 
    it returns "3-5 years"). If no range is found but one or more single numbers are found, 
    it returns the maximum value as "X years". If nothing is found, it returns "0 years".
    
    Examples:
      - "We require 3-5 years of experience" → "3-5 years"
      - "Candidates must have 1 year in Python and 3 years overall" → "3 years"
      - If nothing is mentioned, returns "0 years".
    """
    text = text.strip()
    
    # Find all range matches (e.g., "3-5 years" or "3–5 years")
    # Each match is a tuple (min, max)
    pattern_range = r'(\d+)\s*[-–]\s*(\d+)\s*years?'
    ranges = re.findall(pattern_range, text, re.IGNORECASE)
    
    if ranges:
        # Convert upper bounds to integer and pick the range with the highest upper bound
        max_range = max(ranges, key=lambda x: int(x[1]))
        return f"{max_range[0]}-{max_range[1]} years"
    
    # If no range is found, look for single numbers (e.g., "5 years")
    pattern_single = r'(\d+)\s*years?'
    singles = re.findall(pattern_single, text, re.IGNORECASE)
    if singles:
        max_single = max(map(int, singles))
        return f"{max_single} years"
    
    return "0 years"

def main():
    input_csv = "JobHunter/data/jobs_with_experience_normalized_updated.csv" 
    output_csv = "JobHunter/data/rule_based_experience.csv"
    
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Apply the extraction function on the "cleaned_description" column
    df["rule_based_experience"] = df["cleaned_description"].fillna("").apply(extract_experience)
    
    # Save the DataFrame with the new column into a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Rule-based experience extraction complete. Results saved to {output_csv}")

if __name__ == "__main__":
    main()
