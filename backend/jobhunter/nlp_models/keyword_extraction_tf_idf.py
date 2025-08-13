import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_tfidf(input_csv, output_csv, top_n=10):

    # load the data into a DataFrame
    df = pd.read_csv(input_csv)
    
    # create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    
    # Fit the vectorizer on the 'cleaned_description' and transform
    X = vectorizer.fit_transform(df['cleaned_description'].fillna(''))
    
    # 4) Get the list of all terms from the vectorizer
    terms = vectorizer.get_feature_names_out()
    
    # We'll store the top N keywords for each job here
    top_keywords = []
    
    # 5) For each document (row), find the top N TF-IDF terms
    for i in range(X.shape[0]):
        # Convert row i's TF-IDF vector to a 1D array
        row_data = X[i].toarray().flatten()
        
        # Get indices of the top N TF-IDF scores in descending order
        top_indices = row_data.argsort()[-top_n:][::-1]
        
        # Build a list of terms, ignoring any with zero TF-IDF
        top_terms = [terms[idx] for idx in top_indices if row_data[idx] > 0]
        
        # Join them into a comma-separated string
        top_keywords.append(", ".join(top_terms))
    
    # 6) Add a new column for the extracted keywords
    df['keywords_tfidf'] = top_keywords
    
    # 7) Write the updated DataFrame to a new CSV
    df.to_csv(output_csv, index=False)
    print(f"TF-IDF keyword extraction complete. Results written to {output_csv}.")

def main():
    
    input_csv = "JobHunter/data/jobs_with_skills.csv"
    output_csv = "JobHunter/data/jobs_with_tfidf_keywords.csv"
    
    extract_keywords_tfidf(input_csv, output_csv, top_n=10)

if __name__ == "__main__":
    main()
