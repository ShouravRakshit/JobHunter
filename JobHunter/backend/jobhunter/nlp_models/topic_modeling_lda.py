import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

def run_lda_topic_modeling(input_csv,output_csv,text_column="cleaned_description",n_topics=5,max_features=5000,top_n_words=10):


    # Load the data
    df = pd.read_csv(input_csv)
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in {input_csv}. Please provide the correct column name.")

    # Replace NaNs with empty strings
    documents = df[text_column].fillna("").astype(str)

    # Convert text to a bag-of-words representation
    #    - CountVectorizer counts how many times each word appears in each doc
    #    - max_features limits vocabulary size to the most frequent words
    vectorizer = CountVectorizer(max_features=max_features, stop_words='english')
    X = vectorizer.fit_transform(documents)
    vocab = vectorizer.get_feature_names_out()

    # Fit the LDA model
    lda_model = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        learning_method="batch"
    )
    lda_model.fit(X)

    #    The 'components_' array has shape (n_topics, vocabulary_size).
    #    For each topic, we sort the words by their importance to that topic.
    print("\n=== TOP WORDS PER TOPIC ===")
    for topic_idx, topic_weights in enumerate(lda_model.components_):
        # Sort the words by descending weight
        top_indices = topic_weights.argsort()[-top_n_words:][::-1]
        top_terms = [vocab[i] for i in top_indices]
        print(f"Topic {topic_idx}: {', '.join(top_terms)}")

    # Transform each doc to get the topic distribution
    #    doc_topic_distr is an array of shape (n_docs, n_topics),
    #    indicating the probability that each doc belongs to each topic.
    doc_topic_distr = lda_model.transform(X)

    # Identify the dominant topic for each doc
    dominant_topics = doc_topic_distr.argmax(axis=1)
    df["dominant_topic"] = dominant_topics

    topic_labels = {
        0: "Topic0",
        1: "Topic1",
        2: "Topic2",
        3: "Topic3",
        4: "Topic4"
    }

    df["dominant_topic_label"] = df["dominant_topic"].map(topic_labels)

    # Write results to CSV
    df.to_csv(output_csv, index=False)
    print(f"\nLDA topic modeling complete. Results written to '{output_csv}'.")
    print("Each posting now has a 'dominant_topic' and 'dominant_topic_label' (if assigned).")


def main():
    input_csv = "JobHunter/data/jobs_with_tfidf_keywords.csv"  
    output_csv = "JobHunter/data/topic_modeling_lda.csv"

    run_lda_topic_modeling(
        input_csv="JobHunter/data/jobs_with_tfidf_keywords.csv",
        output_csv="JobHunter/data/topic_modeling_lda.csv",
        text_column="cleaned_description",
        n_topics=5,           # number of topics to discover
        max_features=5000,    
        top_n_words=10        # number of top words to display per topic
    )

if __name__ == "__main__":
    main()
