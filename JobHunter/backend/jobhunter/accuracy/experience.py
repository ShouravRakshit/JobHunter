import pandas as pd
import re

def parse_experience_string(exp_str):
    """
    Converts a string like "3-5 years", "5 years", or "0 years" into a tuple (min_years, max_years).
    Examples:
      "3-5 years" -> (3, 5)
      "5 years"   -> (5, 5)
      "0 years"   -> (0, 0)
      "5+ years"  -> (5, 99)  # or some upper bound if you used "5+" in your dataset
      If the string is "Not specified", treat as (0, 0) or None, up to your preference.
    """
    exp_str = exp_str.strip().lower()
    
    if exp_str in ["not specified", "0 years"]:
        return (0, 0)
    
    # If something like "5+ years" exists in your data, define how to interpret it
    match_plus = re.match(r'(\d+)\+?\s*years', exp_str)
    if match_plus:
        val = int(match_plus.group(1))
        return (val, 99)  # 99 as a big number representing "or more"
    
    # Range pattern, e.g. "3-5 years"
    match_range = re.match(r'(\d+)\s*-\s*(\d+)\s*years', exp_str)
    if match_range:
        min_yr = int(match_range.group(1))
        max_yr = int(match_range.group(2))
        return (min_yr, max_yr)
    
    # Single number pattern, e.g. "5 years"
    match_single = re.match(r'(\d+)\s*years', exp_str)
    if match_single:
        val = int(match_single.group(1))
        return (val, val)
    
    # If nothing matches, assume 0 years
    return (0, 0)

def experience_match(llm_str, parser_str):
    """
    Returns True if the parser's extracted experience is considered a match with the LLM's
    based on whether the numeric ranges overlap or if a single number is within a range.
    
    Examples:
      LLM: "3-5 years", Parser: "4 years"  -> True
      LLM: "5-7 years", Parser: "5 years"  -> True
      LLM: "1-3 years", Parser: "3 years"  -> True
      LLM: "3-5 years", Parser: "6 years"  -> False
      LLM: "3 years", Parser: "5 years"    -> False
    """
    llm_range = parse_experience_string(llm_str)
    parser_range = parse_experience_string(parser_str)
    # Each is a tuple (min, max)
    llm_min, llm_max = llm_range
    par_min, par_max = parser_range
    
    # Two main scenarios:
    # 1) Single values are just min=val, max=val, so we check if they match exactly or
    #    if the single value is in the other's range
    # 2) Ranges: we check if there's any overlap
    
    # For them to match, let's define a simple rule:
    # "They match if par_min..par_max is at least partially within llm_min..llm_max"
    # or vice versa. That is, the intervals intersect.
    
    # Intersection check:
    # intersection exists if the start of one is <= the end of the other AND
    # the end of one is >= the start of the other
    if (par_min <= llm_max) and (par_max >= llm_min):
        return True
    else:
        return False

def evaluate_experience_range(csv_file, llm_col="experience_required", parser_col="rule_based_experience"):
    """
    Reads a CSV file containing LLM experience values and rule-based experience values.
    Compares them with the experience_match function to see if they "match" based on overlap.
    
    Returns:
      - match_percentage (float)
      - total_matches (int)
      - total_rows (int)
    """
    df = pd.read_csv(csv_file)
    total_rows = df.shape[0]
    if total_rows == 0:
        return 0.0, 0, 0
    
    match_count = 0
    for _, row in df.iterrows():
        llm_val = str(row.get(llm_col, "0 years"))
        parser_val = str(row.get(parser_col, "0 years"))
        if experience_match(llm_val, parser_val):
            match_count += 1
    
    match_pct = (match_count / total_rows) * 100 if total_rows else 0
    return match_pct, match_count, total_rows

def main():
    csv_file = "JobHunter/data/rule_based_experience.csv"
    llm_col = "experience_normalized"
    parser_col = "rule_based_experience"
    
    match_pct, match_count, total_rows = evaluate_experience_range(csv_file, llm_col, parser_col)
    print(f"Experience match: {match_pct:.2f}% ")

if __name__ == "__main__":
    main()
