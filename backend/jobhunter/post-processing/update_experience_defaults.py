import pandas as pd

def update_experience_based_on_title(input_csv, output_csv, exp_column="experience_normalized", title_column="standardized_title"):
    """
    Reads a CSV file and updates the experience information:
      - For rows with "Not specified" in the experience column:
          - If the standardized title contains managerial keywords, sets it to "5+ years".
          - Otherwise, sets it to "0-5 years".
    The updated data is saved to a new CSV file.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Define managerial keywords that indicate a higher level role.
    managerial_keywords = ["manager", "director", "executive", "tech-lead", "head",  "senior"]
    
    def update_experience(row):
        current_exp = row[exp_column]
        job_title = str(row[title_column]).lower()
        if current_exp == "Not specified":
            if any(kw in job_title for kw in managerial_keywords):
                return "5+ years"
            else:
                return "0-5 years"
        return current_exp

    # Apply the update function to each row
    df[exp_column] = df.apply(update_experience, axis=1)
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")

def main():
    input_csv = "JobHunter/data/jobs_with_experience_normalized.csv"
    output_csv = "JobHunter/data/jobs_with_experience_normalized_updated.csv"
    update_experience_based_on_title(input_csv, output_csv)

if __name__ == "__main__":
    main()
