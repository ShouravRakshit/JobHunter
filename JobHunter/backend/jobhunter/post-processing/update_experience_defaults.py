import pandas as pd

def update_not_specified(input_csv, output_csv, column_name="experience_normalized", default_value="0-5 years"):
    """
    Reads a CSV file, replaces all occurrences of "Not specified" in the specified column
    with a default value ("0-5 years"), and saves the updated DataFrame to a new CSV file.

    Parameters:
      - input_csv (str): Path to the input CSV file.
      - output_csv (str): Path where the updated CSV will be saved.
      - column_name (str): Name of the column to update (default: "experience_normalized").
      - default_value (str): The default value to use (default: "0-5 years").
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Count rows with "Not specified" before the update (for logging)
    count_before = df[df[column_name] == "Not specified"].shape[0]
    print(f"Rows with 'Not specified' before update: {count_before}")
    
    # Replace "Not specified" with the default value
    df.loc[df[column_name] == "Not specified", column_name] = default_value
    
    # Count how many rows now have the default value
    count_after = df[df[column_name] == default_value].shape[0]
    print(f"Rows updated to '{default_value}': {count_after}")
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")

def main():
    input_csv = "JobHunter/data/jobs_with_experience_normalized.csv"  # Your current CSV file
    output_csv = "JobHunter/data/jobs_with_experience_normalized_updated.csv"  # New file with defaults updated
    update_not_specified(input_csv, output_csv)

if __name__ == "__main__":
    main()
