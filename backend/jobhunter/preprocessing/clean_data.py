import csv
import re

from bs4 import BeautifulSoup

# NLTK imports
import nltk
from nltk.corpus import stopwords

# spaCy imports
import spacy

nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words("english"))

# remove the html tags from the text
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text

# remove boilerplate text
def remove_disclaimers(text, disclaimers):
    for phrase in disclaimers:
        text = text.replace(phrase, "")
    return text

# remove special characters, excessive whitespace
def clean_special_chars(text):
    text = re.sub(r"[^a-zA-Z0-9.,!?;:\s]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# remove stopwords
def remove_stopwords(text):
    tokens = nltk.word_tokenize(text)
    filtered_tokens = [t for t in tokens if t.lower() not in STOPWORDS]
    return " ".join(filtered_tokens)

# tokenize text
def spacy_cleanup(text):
 
    doc = nlp(text)
    tokens = []
    for token in doc:
        if not token.is_stop:  # spaCy's built-in stop check
            tokens.append(token.lemma_.lower())
    return " ".join(tokens)

def clean_job_data(input_csv, output_csv):

    # Example disclaimers
    disclaimers = [
        "EEO Statement",
        "We are an equal opportunity employer",
        "At Ledcor we believe diversity, equity, and inclusion should be part of everything we do."
        " We are proud to be an equal-opportunity employer. All qualified individuals, regardless of"
        " race, color, religion, sex, national origin, sexual orientation, age, citizenship, marital status,"
        " disability, gender identity, Veteran status or any other identifying characteristic are encouraged to apply.",
    ]

    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:
        
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["cleaned_description"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            raw_desc = row.get("description", "") or ""

            #  remove HTML
            text = remove_html_tags(raw_desc)

            # remove disclaimers
            text = remove_disclaimers(text, disclaimers)

            # remove special chars, excessive whitespace
            text = clean_special_chars(text)

            # convert to lowercase
            text = text.lower()

            # remove NLTK stopwords
            text = remove_stopwords(text)

            row["cleaned_description"] = text
            writer.writerow(row)


def main():
    
    input_csv = "JobHunter/data/raw_jobs.csv"
    output_csv = "JobHunter/data/cleaned_jobs.csv"

    clean_job_data(input_csv, output_csv)
    print(f"Done! Cleaned data written to {output_csv}.")


if __name__ == "__main__":
    main()
